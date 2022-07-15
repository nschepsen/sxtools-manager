from PySide6.QtCore import Qt, Slot, QDate
from PySide6.QtWidgets import QCompleter, QWidget
from sxtools.ui.compiled.sceneeditor import Ui_SceneEditor


class SceneEditor(QWidget):
    '''
    '''
    def __init__(self, perfs: list, paysites: list, parent = None) -> None:
        '''
        '''
        super(SceneEditor, self).__init__(parent) # inherit from parents
        self.ui = Ui_SceneEditor()
        self.ui.setupUi(self) # load UI elements
        cPerfs = QCompleter(perfs)
        # cPerfs.setCompletionMode(QCompleter.InlineCompletion)
        cPerfs.setFilterMode(Qt.MatchContains)
        cPerfs.setCaseSensitivity(Qt.CaseInsensitive)
        self.ui.iPerformer.setCompleter(cPerfs)
        cSites = QCompleter(paysites)
        cSites.setCaseSensitivity(Qt.CaseInsensitive)
        cSites.setFilterMode(Qt.MatchContains)
        self.ui.iPaysite.setCompleter(cSites)
        # connect UI elements to the existing methods
        self.ui.btnAdd.clicked.connect(self.addPerformer)
        self.ui.btnDelete.clicked.connect(self.deletePerformer)
        self.ui.btnResetDate.clicked.connect(
            lambda x: self.ui.iReleaseDate.setDate(QDate(2000, 1, 1)))
    @Slot()
    def addPerformer(self) -> None:
        '''
        '''
        perf = self.ui.iPerformer.text().strip().title()
        pl = self.ui.performerList
        if perf and not pl.findItems(perf, Qt.MatchFixedString):
            pl.addItem(perf)
        self.ui.iPerformer.setText('') # reset the QLineEdit
    @Slot()
    def deletePerformer(self) -> None:
        '''
        '''
        selected = self.ui.performerList.selectedItems()
        pl = self.ui.performerList
        for item in selected:
            self.ui.performerList.takeItem(pl.indexFromItem(item).row())
