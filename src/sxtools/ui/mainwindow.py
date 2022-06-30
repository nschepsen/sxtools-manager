from os import scandir, unlink
from subprocess import call
from typing import Tuple
from PySide6.QtCore import QSortFilterProxyModel, Qt
from PySide6.QtWidgets import QFileDialog, QMainWindow, QMessageBox, QProgressDialog, QRadioButton
from sxtools.core.manager import Manager
from sxtools.core.rfcode import RFCode
from sxtools.core.videoscene import Scene
from sxtools.logging import get_basic_logger
logger = get_basic_logger()  # see ~/.config/sxtools/sXtools.log
# re-build .ui-files as the case may be, use pyside6-uic
from sxtools.ui.compiled.mainwindow import Ui_MainWindow
from sxtools.ui.decisiondialog import DecisionDialog
from sxtools.ui.scenefilter import SceneFilter
from sxtools.ui.scenelistdelegate import SceneDelegate
from sxtools.ui.scenelistmodel import SceneModel
from sxtools.utils import bview, cache, cache_size, fview, human_readable


class MainWindow(QMainWindow):
    '''
    MainWindow is the SxTools!MANAGER's main window (GUI)
    '''
    def __init__(self, m: Manager) -> None:

        super(MainWindow, self).__init__()
        self.manager = m # load manager
        self.manager.ui, self.ui = self, Ui_MainWindow()
        self.ui.setupUi(self) # load UI
        self.setWindowTitle(f'{m.caption}')
        self.ui.sceneView.setModel(
            SceneModel(self.manager.queue, self))
        self.ui.sceneView.setItemDelegate(
            SceneDelegate(self.ui.sceneView))
        # connect UI slots
        self.ui.sceneView.doubleClicked.connect(self.openVideo)
        # connect UI actions [FILE]
        self.ui.aImport.triggered.connect(self.load)
        self.ui.aRelocate.triggered.connect(self.relocate)
        self.ui.aSave.triggered.connect(self.save)
        # connect UI actions [EDIT]
        # self.ui.aSettings.triggered.connect(self.save)
        # connect UI actions [VIEW]
        self.ui.aScan.triggered.connect(self.deepScan)
        self.ui.aClearCache.triggered.connect(self.clearCache)
        # connect UI actions [HELP]
        # self.ui.aAbout.triggered.connect(self.save)
        # self.ui.aAboutQt.triggered.connect(self.save)
        # self.ui.aGitHub.triggered.connect(self.save)
        self.ui.aClearCache.setText(f'Clear Cache [{human_readable(cache_size())}]')

    def relocate(self) -> None:
        '''
        '''
        for s in self.ui.sceneView.model().scenelist:
            self.manager.relocate(s)
        # TODO: relocate selected scene(s) item-wise, otherwise all at once

    def openVideo(self, index):
        '''
        '''
        # TODO: internal video player
        call(['mpv', index.model().scenelist[index.row()].path])

    def deepScan(self):
        '''
        '''
        scenelist = self.ui.sceneView.model().scenelist
        progress = QProgressDialog(
            "Scanning Files", "Cancel", 0, len(scenelist), self)
        progress.setMinimumWidth(400)
        progress.setCancelButton(None)
        progress.setWindowModality(Qt.WindowModal)
        progress.setWindowTitle('SxTools!MANAGER')
        i = 0
        for s in scenelist:
            if progress.wasCanceled():
                break
            s.scan()
            i += 1
            progress.setValue(i)
        self.ui.aClearCache.setText(f'Clear Cache [{human_readable(cache_size())}]')

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

    def load(self) -> None:
        '''
        Look for scene(s), analyse and load 'em into a View
        '''
        self.manager.queue.clear() # reset the queue
        path = QFileDialog.getExistingDirectory(
            self, 'Select a directory', self.manager.src)
        self.manager.fetch(path)
        n = len(self.manager.queue) # scenes number
        ret = 0
        for x in self.manager.queue:
            ret += self.manager.analyse(x)
        self.ui.sceneView.model().sync(self.manager.queue)
        self.ui.statusbar.showMessage(f'Imported {ret} of {n} scene(s) matched to the regex')

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

    def changeFilterKeyColumn(self, btn: QRadioButton, checked: bool):
        '''
        '''
        if checked and type(self.ui.sceneTableView.model()) == QSortFilterProxyModel:
            self.ui.sceneTableView.model().setFilterKeyColumn({
                'rbPerformer': 1,
                'rbSite': 2,
                'rbTitle': 4}.get(btn.objectName(), 1))
        logger.debug(f'Change FilterKeyColumn to "{btn.objectName()[2:]}"')
