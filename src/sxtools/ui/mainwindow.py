from os import scandir, unlink
from os.path import isfile
from subprocess import call
from typing import Tuple
from PySide6.QtCore import QEvent, QModelIndex, QObject, Qt, Slot
from PySide6.QtGui import QActionGroup, QCloseEvent, QIcon, QShortcut, QKeySequence
from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox, QMenu, QProgressDialog, QRadioButton, QStyle
from sxtools import __author__, __date__, __email__, __project__,__status__, __version__
from sxtools.core.manager import Manager
from sxtools.core.rfcode import RFCode
from sxtools.core.videoscene import Scene
from sxtools.logging import get_basic_logger
from sxtools.ui.scenefilter import SceneSortFilter
from sxtools.ui.sitemapeditor import SitemapEditor
logger = get_basic_logger()  # see ~/.config/sxtools/sXtools.log
from sxtools.ui.compiled.mainwindow import Ui_MainWindow
from sxtools.ui.scenedialog import DecisionDialog
from sxtools.ui.scenedelegate import SceneDelegate
from sxtools.ui.scenemodel import SceneDataRole, SceneModel
from sxtools.utils import bview, cache, cache_size, check_updates, fview, human_readable


class MainWindow(QMainWindow):
    '''
    A Qt6 and PySide6 based implementation of GUI for the app SxTools!MANAGER
    '''
    def __init__(self, manager: Manager) -> None:
        '''
        '''
        super(MainWindow, self).__init__()
        self.manager = manager # store an instance locally
        self.manager.ui, self.ui = self, Ui_MainWindow()
        self.ui.setupUi(self) # load UI
        self.dataChanged = False
        self.smeWindow = None
        self.setGeometry(QStyle.alignedRect(
            Qt.LeftToRight,
            Qt.AlignCenter,
            self.size(),
            QApplication.primaryScreen().availableGeometry()))
        self.setWindowTitle(
            f'{__project__} v{__version__} ({__date__})')
        # create proxy model, QSortFilterProxyModel
        proxy = SceneSortFilter(self)
        proxy.setSourceModel(SceneModel(self))
        self.ui.sceneView.setModel(proxy)
        self.ui.sceneView.setItemDelegate(SceneDelegate(self.ui.sceneView))
        self.ui.sceneView.installEventFilter(self)
        # shortcuts & key sequences
        QShortcut(
            QKeySequence.Delete, self.ui.sceneView).activated.connect(self.remove)
        shortcut = QShortcut(QKeySequence.Deselect, self.ui.sceneView)
        shortcut.activated.connect(
            lambda: self.ui.sceneView.clearSelection())
        # connect Qt6 signals
        self.ui.sceneView.doubleClicked.connect(self.play)
        self.ui.filterBox.textChanged.connect(
            self.onFilterTextChanged)
        self.ui.filterRoles.buttonToggled.connect(self.onFilterRoleChanged)
        # connect Qt6 actions, QMenu:@File
        self.ui.aOpen.triggered.connect(self.onOpenActionTriggered)
        self.ui.aRelocate.triggered.connect(self.onMoveActionTriggered)
        self.ui.aSave.triggered.connect(self.onSaveActionTriggered)
        # connect Qt6 actions, QMenu:@Collections
        # self.ui.aSettings.triggered.connect(self.save)
        # connect Qt6 actions, QMenu:@View
        sortModes = QActionGroup(self)
        sortModes.addAction(self.ui.actionSortByPerformers)
        sortModes.addAction(self.ui.actionSortByTitle)
        sortModes.addAction(self.ui.actionSortByPaysite)
        sortModes.addAction(self.ui.actionSortBySize)
        sortModes.addAction(self.ui.actionSortByReleaseDate)
        sortModes.triggered.connect(self.onSortModeChanged)
        self.ui.aSortOrder.triggered.connect(self.onSortOrderChanged)
        self.ui.aScan.triggered.connect(self.onScanActionTriggered)
        self.ui.aClearCache.triggered.connect(self.onClearCacheActionTriggered)
        self.ui.aClearCache.setText(
            f'Clear Cache ({human_readable(cache_size())})')
        self.ui.aFilterModeT.triggered.connect(proxy.invalidateFilter)
        self.ui.aFilterModeU.triggered.connect(proxy.invalidateFilter)
        # connect Qt6 actions, QMenu:@Help
        self.ui.aAbout.triggered.connect(self.onAboutActionTriggered)
        self.ui.aAboutQt.triggered.connect(self.onAboutQtActionTriggered)
        self.ui.aEditSiteMap.triggered.connect(self.editMapping)
        self.ui.aUpdate.triggered.connect(self.onUpdateActionTriggered) # check for a new version

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        '''
        add an additional context menu for scenes
        '''
        if not self.ui.sceneView.model().rowCount():
                return False
        if event.type() == QEvent.ContextMenu and watched is self.ui.sceneView:
            menu = QMenu() # build context menu entries
            menu.setStyleSheet('''
                QMenu {
                    padding: 3px;
                }
                QMenu::item {
                    padding: 5px 5px 5px 10px;
                }
                QMenu::icon {
                    margin-left: 15px;
                }
                QMenu::item:selected {

                    background: rgba(237, 237, 237, 237);
                }''')
            menu.addAction(QIcon.fromTheme('media-playback-start'),
                'Play scenes with "MPV"', self.play)
            menu.addAction('Move to ...', self.onMoveActionTriggered)
            menu.addAction(
                QIcon.fromTheme('delete'), 'Delete selected Scenes', self.remove, QKeySequence.Delete)
            menu.exec_(event.globalPos())
            return True
        return super().eventFilter(watched, event)

    def closeEvent(self, event: QCloseEvent) -> None:
        '''
        add an additional check before the window gets closed
        '''
        if self.dataChanged:
            ret = QMessageBox.question(
                self, # parent
                'SxTools!MANAGER',
                'Are you sure you want to exit the program?')
            if ret != QMessageBox.StandardButton.Yes:
                return event.ignore()
        return super().closeEvent(event) # calling superclass method

    @Slot(QModelIndex)
    def play(self, index: QModelIndex = None) -> None:
        '''
        open selected scenes within MPV media player and play 'em shuffled
        '''
        pl = [index] if index else self.ui.sceneView.selectedIndexes()
        model = self.ui.sceneView.model() # get proxy model
        playlist = [
            (x, model.data(x, SceneDataRole.PathRole)) for x in pl]
        call(['mpv', '--shuffle=yes', *[x[1] for x in playlist]])
        for x, path in sorted(playlist, reverse=True, key=lambda x: x[0]):
            if isfile(path):
                continue
            model.remove(x)
        self.ui.sceneView.setCurrentIndex(QModelIndex())
        self.ui.filtredValue.setText(str(model.rowCount())) # update the label

    @Slot()
    def onOpenActionTriggered(self) -> None:
        '''
        import scenes from a directory, analyse and load 'em into a View
        '''
        self.ui.sceneView.model().sourceModel().clear()
        self.manager.reset()
        src = QFileDialog.getExistingDirectory(self,
            'Open Directory',
            self.manager.src,
            QFileDialog.ShowDirsOnly)
        if not src: # no directory passed! error?! exit
            return
        self.manager.fetch(src) # populate queue w scenes
        n = len(self.manager.queue)
        ret = 0
        for x in self.manager.queue:
            ret += self.manager.analyse(x)
        self.ui.sceneView.model().sourceModel().sync(self.manager.queue)
        self.ui.statusbar.showMessage(
            f'Imported {ret} of {n} scene(s) matched to the regex')
        # update the label "Found"
        self.ui.filtredValue.setText(str(self.ui.sceneView.model().rowCount()))

    @Slot()
    def remove(self) -> None:
        '''
        delete "safely" selected scenes from the list
        '''
        indexes = self.ui.sceneView.selectedIndexes()
        model = self.ui.sceneView.model() # get proxy model
        # remove items backwards to keep index valid, be careful anyway
        for index in sorted(indexes, reverse=True):
            model.remove(index)
        self.ui.sceneView.clearSelection()
        # update the label "Found"
        self.ui.filtredValue.setText(str(model.rowCount()))

    @Slot()
    def onMoveActionTriggered(self) -> None:
        '''
        relocate selected scenes to a passed collection directory
        '''
        output = QFileDialog.getExistingDirectory(self,
            'Move scenes to Collection directory',
            self.manager.out, QFileDialog.ShowDirsOnly)
        if not output: # no directory passed! error?! exit
            return
        self.manager.out = output
        indexes = self.ui.sceneView.selectedIndexes()
        removeSelection = True
        for index in indexes:
            self.manager.relocate(index.data(SceneDataRole.SceneRole))
        self.ui.statusbar.showMessage(
            f'Moved {len(indexes)} scene(s) to "{output}"')
        if removeSelection:
            self.remove() # remove selected scenes from the list, too

    @Slot(QActionGroup)
    def onSortModeChanged(self, ag: QActionGroup) -> None:
        '''
        handle SortMode changing
        '''
        self.ui.sceneView.model().setSortRole(
            {
                'Sort by &Performers':
                    SceneDataRole.PerformersRole,
                'Sort by Title':
                    SceneDataRole.TitleRole,
                'Sort by Paysite':
                    SceneDataRole.PaysiteRole,
                'Sort by &Size':
                    SceneDataRole.SizeRole,
                'Sort by Release &Date':
                    SceneDataRole.DateRole # Release Date
            }.get(ag.text(), SceneDataRole.PerformersRole))
        self.ui.sceneView.model().sort(0, self.ui.sceneView.model().sortOrder())

    @Slot()
    def onSortOrderChanged(self) -> None:
        '''
        handle SortOrder changing
        '''
        proxy = self.ui.sceneView.model() # get proxy model
        if not proxy.sortRole(): # 0: Asc, 1: Desc
            self.ui.aSortOrder.setChecked(False)
            return
        proxy.sort(0, Qt.SortOrder(self.ui.aSortOrder.isChecked()))

    @Slot(str)
    def onFilterTextChanged(self, string: str) -> None:
        '''
        handle FilterText changing
        '''
        proxy = self.ui.sceneView.model() # get proxy model
        proxy.setFilterFixedString(string)
        # update the label "Found"
        self.ui.filtredValue.setText(str(proxy.rowCount()))

    @Slot(QRadioButton, bool)
    def onFilterRoleChanged(self, btn: QRadioButton, toggled: bool) -> None:
        '''
        handle FilterRole changing, be careful
        '''
        if not toggled:
            return
        proxy = self.ui.sceneView.model()
        # get toggled FilterRole from the group
        role = {
            'rbPaysites':
                SceneDataRole.PaysiteRole,
            'rbTitles':
                SceneDataRole.TitleRole,
            'rbPerformers':
                SceneDataRole.PerformersRole,
            }.get(btn.objectName(), SceneDataRole.PerformersRole)
        proxy.setFilterRole(role) # Qt.DisplayRole
        # update the label "Found"
        self.ui.filtredValue.setText(str(proxy.rowCount()))

    @Slot()
    def onScanActionTriggered(self) -> None:
        '''
        perform a scene video Scan using "ffprobe"
        '''
        progress = QProgressDialog(
            'Scanning Files',
            'Cancel',
            0, len(self.manager.queue), self)
        progress.setMinimumWidth(400)
        progress.setCancelButton(None)
        progress.setWindowModality(Qt.WindowModal)
        progress.setWindowTitle('SxTools!MANAGER')
        for i, scene in enumerate(self.manager.queue):
            if progress.wasCanceled():
                break
            scene.scan() # perform a scan
            progress.setValue(i)
        self.ui.aClearCache.setText(
            f'Clear Cache [{human_readable(cache_size())}]')

    @Slot()
    def onAboutActionTriggered(self) -> None:
        '''
        show "About" MessageBox
        '''
        QMessageBox.about(self, 'SxTools!MANAGER <About>',
            f'<b>SxTools!MANAGER</b> {__version__}'
            f'<br><br>'
            f'<b>Author</b>: {__author__} "{__email__}"')

    @Slot()
    def onAboutQtActionTriggered(self) -> None:
        '''
        show "About Qt6" MessageBox
        '''
        QMessageBox.aboutQt(self, 'SxTools!MANAGER <About Qt>')

    @Slot()
    def editMapping(self) -> None:
        '''
        open a sitemap editor's window (singleton)
        '''
        if not self.smeWindow:
            self.smeWindow = SitemapEditor(self.manager.cfg)
            spawnRect = QStyle.alignedRect(
                Qt.LeftToRight,
                Qt.AlignCenter,
                self.smeWindow.size(),
                self.geometry())
            self.smeWindow.setGeometry(spawnRect)
        self.smeWindow.show() # show sitemap editor window if is there one

    @Slot()
    def onUpdateActionTriggered(self) -> None:
        '''
        check the version of your app's copy for updates
        '''
        ret = QMessageBox.information(self,
            'SxTools!MANAGER <Updates>',
            f'You are using {check_updates()} build ({__version__})')
        # TODO: implement an auto-update mechanism

    @Slot()
    def onClearCacheActionTriggered(self):
        '''
        delete thumbnails from the cache directory
        '''
        with scandir(cache()) as thumbnails:
            for entry in thumbnails:
                if entry.is_file():
                    unlink(entry.path)
        self.ui.sceneView.setFocus() # FIXME: force to repaint
        self.ui.aClearCache.setText(
            f'Clear Cache ({human_readable(cache_size())})')

    def onSaveActionTriggered(self) -> None:
        '''
        save configs and other necessary informations
        '''
        if self.smeWindow: # check if sitemap window open'd
            # get acronyms
            w = self.smeWindow.ui.acronyms
            d = {}
            for row in range(w.rowCount()):
                d.update(
                    {w.item(row, 0).text(): w.item(row, 1).text()})
            self.manager.cfg['acronyms'] = d
            # get paysites
            w = self.smeWindow.ui.paysites
            self.manager.cfg['sites'] = [w.item(row).text() for row in range(w.count())]
            # get unknowns
            w = self.smeWindow.ui.unknowns
            self.manager.cfg['undefined'] = [w.item(row).text() for row in range(w.count())]
        self.manager.save() # save changes to the file

    def decision(self, tail: str, s: Scene) -> Tuple[RFCode, str]:
        '''
        client-side implementation of a decision system
        '''
        dialog = DecisionDialog(
            str(s),
            [fview('.'.join(tail.split('.')[:x])) for x in [[1], [1, 2], [3, 1, 2]][min(tail.count('.'), 2)]])
        ret = 'skip' if not dialog.exec() else bview(dialog.decision())
        opcode = {
            'skip': RFCode.SKIP_SCENE,
            'title': RFCode.TITLE
            }.get(ret, RFCode.PERFORMER)
        return opcode, ret # return a Tuple[opcode[, performer]]

    def question(self, question: str) -> int:
        '''
        client-side implementation of a question system
        '''
        ret = QMessageBox.question(
            self,
            'SxTools!MANAGER <Question>',
            question,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Discard)
        return {
            QMessageBox.StandardButton.Yes: 1,
            QMessageBox.StandardButton.No: 0,
            QMessageBox.StandardButton.Discard: 2
        }.get(ret, 0)
        return ret # assert QMessageBox.StandardButton == type(ret)
