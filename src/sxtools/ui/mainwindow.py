from os import scandir, unlink
from subprocess import call
from typing import Tuple

from PySide6.QtCore import QModelIndex, QSortFilterProxyModel, Qt, Slot
from PySide6.QtGui import QActionGroup
from PySide6.QtWidgets import QFileDialog, QMainWindow, QMessageBox,QProgressDialog, QRadioButton

from sxtools import __date__, __author__, __email__, __status__, __version__
from sxtools.core.manager import Manager
from sxtools.core.rfcode import RFCode
from sxtools.core.videoscene import Scene
from sxtools.logging import get_basic_logger
from sxtools.ui.scenefilter import SceneSortFilter
logger = get_basic_logger()  # see ~/.config/sxtools/sXtools.log
# re-build .ui-files as the case may be, use pyside6-uic
from sxtools.ui.compiled.mainwindow import Ui_MainWindow
from sxtools.ui.decisiondialog import DecisionDialog
from sxtools.ui.scenelistdelegate import SceneDelegate
from sxtools.ui.scenelistmodel import SceneDataRole, SceneModel
from sxtools.utils import bview, cache, cache_size, check_updates, fview, human_readable


class MainWindow(QMainWindow):
    '''
    MainWindow is the SxTools!MANAGER's main window (GUI)
    '''
    def __init__(self, m: Manager) -> None:

        super(MainWindow, self).__init__()
        self.manager = m # load manager
        self.manager.ui, self.ui = self, Ui_MainWindow()
        # default preference definition
        self.prefs = {
            'sort': {
                'order': Qt.AscendingOrder
            }
        }
        self.ui.setupUi(self) # load UI
        self.setWindowTitle(f'{m.caption}')
        baseModel = SceneModel(self.manager.queue, self)
        proxy = SceneSortFilter(self)
        proxy.setSourceModel(baseModel)
        self.ui.sceneView.setModel(proxy)
        self.ui.sceneView.setItemDelegate(SceneDelegate(self.ui.sceneView))
        self.ui.sceneView.verticalScrollBar().setSingleStep(5)
        # crete action group [SortMode]
        sortModes = QActionGroup(self)
        sortModes.addAction(self.ui.actionSortByPerformers)
        sortModes.addAction(self.ui.actionSortByTitle)
        sortModes.addAction(self.ui.actionSortByPaysite)
        sortModes.addAction(self.ui.actionSortBySize)
        sortModes.addAction(self.ui.actionSortByReleaseDate)
        # connect UI slots
        self.ui.sceneView.doubleClicked.connect(self.play)
        self.ui.leSearchField.textChanged.connect(self.onFilterTextChanged)
        self.ui.bgFilterRoles.buttonToggled.connect(self.onFilterRoleChanged)
        # connect UI actions [FILE]
        self.ui.aOpen.triggered.connect(self.open)
        self.ui.aRelocate.triggered.connect(self.relocate)
        self.ui.aSave.triggered.connect(self.save)
        # connect UI actions [EDIT]
        # self.ui.aSettings.triggered.connect(self.save)
        # connect UI actions [VIEW]
        sortModes.triggered.connect(self.onSortModeChanged)
        self.ui.actionSortOrder.triggered.connect(self.onSortOrderChanged)
        self.ui.aScan.triggered.connect(self.scan)
        self.ui.aClearCache.triggered.connect(self.clearCache)
        # connect UI actions [HELP]
        self.ui.aAbout.triggered.connect(self.about)
        self.ui.aAboutQt.triggered.connect(self.aboutQt)
        self.ui.aUpdate.triggered.connect(self.update)
        self.ui.aClearCache.setText(f'Clear Cache [{human_readable(cache_size())}]')
    @Slot(QModelIndex)
    def play(self, index) -> None:
        '''
        '''
        # TODO: internal video player
        baseIndex = index.model().mapToSource(index) # get base index
        call(['mpv', baseIndex.model().scenelist[baseIndex.row()].path])
    @Slot()
    def open(self) -> None:
        '''
        Look for scene(s), analyse and load 'em into a View
        '''
        self.ui.sceneView.model().sourceModel().clear() # reset
        src = QFileDialog.getExistingDirectory(self,
            'Open Directory',
            self.manager.src,
            QFileDialog.ShowDirsOnly)
        if not src:
            return
        self.manager.fetch(src) # populate queue w scenes
        n = len(self.manager.queue)
        ret = 0
        for x in self.manager.queue:
            ret += self.manager.analyse(x)
        self.ui.sceneView.model().sourceModel().sync(self.manager.queue)
        self.ui.statusbar.showMessage(
            f'Imported {ret} of {n} scene(s) matched to the regex')
    @Slot()
    def relocate(self) -> None:
        '''
        '''
        output = QFileDialog.getExistingDirectory(self,
            'Save to Collection',
            self.manager.out,
            QFileDialog.ShowDirsOnly)
        if not output:
            return
        self.manager.out = output
        for s in self.manager.queue:
            self.manager.relocate(s)
        # TODO: relocate selected scene(s) item-wise, otherwise all at once
    @Slot(QActionGroup)
    def onSortModeChanged(self, ag: QActionGroup) -> None:
        '''
        '''
        self.ui.sceneView.model().setSortRole(
            {
                'Sort by Performers':
                    SceneDataRole.PerformersRole,
                'Sort by Title':
                    SceneDataRole.TitleRole,
                'Sort by Paysite':
                    SceneDataRole.PaysiteRole,
                'Sort by Size':
                    SceneDataRole.SizeRole,
                'Sort by Release Date':
                    SceneDataRole.DateRole # Release Date
            }.get(ag.text(), SceneDataRole.PerformersRole))
        self.ui.sceneView.model().sort(0, self.ui.sceneView.model().sortOrder())
    @Slot()
    def onSortOrderChanged(self) -> None:
        '''
        '''
        self.ui.sceneView.model().sort(
            0, Qt.SortOrder(self.ui.actionSortOrder.isChecked()))
    @Slot(str)
    def onFilterTextChanged(self, string: str) -> None:
        '''
        '''
        self.ui.sceneView.model().setFilterFixedString(string)
    @Slot(QRadioButton, bool)
    def onFilterRoleChanged(self, btn: QRadioButton, toggled: bool) -> None:
        '''
        '''
        if not toggled:
            return
        # get SceneDataRole as FilterRole
        role = {
            'rbPaysites':
                SceneDataRole.PaysiteRole,
            'rbTitles':
                SceneDataRole.TitleRole,
            'rbPerformers':
                SceneDataRole.PerformersRole,
            }.get(btn.objectName(), SceneDataRole.PerformersRole)
        self.ui.sceneView.model().setFilterRole(role) # Qt.DisplayRole
    @Slot()
    def scan(self) -> None:
        '''
        '''
        scenelist = self.manager.queue # self.ui.sceneView.model().scenelist
        progress = QProgressDialog(
            'Scanning Files',
            'Cancel',
            0, len(scenelist), self)
        progress.setMinimumWidth(400)
        progress.setCancelButton(None)
        progress.setWindowModality(Qt.WindowModal)
        progress.setWindowTitle('SxTools!MANAGER')
        i = 0
        for s in scenelist:
            if progress.wasCanceled():
                break
            s.scan() # perform a scan
            i += 1
            progress.setValue(i)
        self.ui.aClearCache.setText(
            f'Clear Cache [{human_readable(cache_size())}]')
    @Slot()
    def about(self) -> None:
        '''
        '''
        QMessageBox.about(self, 'SxTools!MANAGER <About>',
            f'<b>SxTools!MANAGER</b> {__version__}'
            f'<br><br>'
            f'<b>Author</b>: {__author__} "{__email__}"')
    @Slot()
    def aboutQt(self) -> None:
        '''
        '''
        QMessageBox.aboutQt(self, 'SxTools!MANAGER <About Qt>')
    @Slot()
    def update(self) -> None:
        '''
        '''
        ret = QMessageBox.information(self,
            'SxTools!MANAGER <Updates>',
            f'You are using {check_updates()} build ({__version__})')
    @Slot()
    def clearCache(self):
        '''
        Remove thumbnails from the Cache
        '''
        with scandir(cache()) as it:
            for entry in it:
                if entry.is_file():
                    unlink(entry.path)
        self.ui.sceneView.setFocus() # TODO: force to repaint
        self.ui.aClearCache.setText(f'Clear Cache [{human_readable(cache_size())}]')

    def save(self) -> None: self.manager.save()

    def decision(self, tail: str, s: Scene) -> Tuple[RFCode, str]:
        '''
        Let user decide whether X performs in S or doesn't
        '''
        dialog = DecisionDialog(
            str(s),
            [fview('.'.join(tail.split('.')[:x])) for x in [[1], [1, 2], [3, 1, 2]][min(tail.count('.'), 2)]])
        ret = 'skip' if not dialog.exec() else bview(dialog.decision())
        opcode = {
            'skip': RFCode.SKIP_SCENE,
            'title': RFCode.TITLE
            }.get(ret, RFCode.PERFORMER)
        print(f'opcode: {opcode} -> ret: {ret}')
        return opcode, ret # return a Tuple[opcode[, performer]]

    def question(self, msg: str) -> bool:
        '''
        '''
        ret = QMessageBox.question(self, 'Make your Decision', msg)
        return ret == QMessageBox.StandardButton.Yes
