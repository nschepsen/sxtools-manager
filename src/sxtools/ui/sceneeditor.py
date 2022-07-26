from dateutil import parser as QDateParser
from PySide6.QtCore import QDate, Qt, Slot
from PySide6.QtWidgets import QCompleter, QWidget
from sxtools.core.manager import Manager
from sxtools.ui.compiled.sceneeditor import Ui_SceneEditor
from sxtools.utils import bview, fview

CSS = 'QAbstractItemView { padding: 0 0 0 4px; } QAbstractItemView::item { padding: 5px; }'

from sxtools.logging import get_basic_logger

logger = get_basic_logger()  # see ~/.config/sxtools/sXtools.log


class SceneEditor(QWidget):
    '''
    '''
    def __init__(self, mgr: Manager, parent = None) -> None:
        '''
        '''
        super(SceneEditor, self).__init__(parent) # inherit from parents
        self.ui = Ui_SceneEditor()
        self.ui.setupUi(self) # load UI elements
        pComp = QCompleter(
            fview(x) for x in mgr.performers.keys())
        pComp.setFilterMode(Qt.MatchContains)
        pComp.setCaseSensitivity(Qt.CaseInsensitive)
        pComp.popup().setStyleSheet(CSS)
# pComp.setCompletionMode(QCompleter.InlineCompletion)
        self.ui.iPerformer.setCompleter(pComp)
        sComp = QCompleter(set(mgr.sitemap.values()))
        sComp.setCaseSensitivity(Qt.CaseInsensitive)
        sComp.setFilterMode(Qt.MatchContains)
        sComp.popup().setStyleSheet(CSS)
        sComp.popup().setAlternatingRowColors(True)
        self.ui.iPaysite.setCompleter(sComp)
        # connect UI elements to the existing methods
        self.ui.btnAdd.clicked.connect(self.add)
        self.ui.btnDelete.clicked.connect(self.delete)
        self.ui.btnResetDate.clicked.connect(
            lambda x: self.ui.iReleaseDate.setDate(QDate(1752, 9, 14)))
        self.ui.btnParseDate.clicked.connect(self.parse)
    @Slot()
    def add(self) -> None:
        '''
        append an artist to the always sorted QListWidget
        '''
        perf = self.ui.iPerformer.text().strip().title()
        pl = self.ui.performerList
        if perf and not pl.findItems(perf, Qt.MatchFixedString):
            pl.addItem(perf)
            logger.debug(f'Added a performer "{perf}"')
        self.ui.iPerformer.setText('') # reset the QLineEdit
    @Slot()
    def delete(self) -> None:
        '''
        take off selected performer(s) from the QListWidget
        '''
        selected = self.ui.performerList.selectedItems()
        pl = self.ui.performerList
        for item in selected:
            logger.debug(
                f'Removed "{item.text()}"')
            self.ui.performerList.takeItem(pl.indexFromItem(item).row())
    @Slot()
    def parse(self) -> None:
        '''
        try to get a date from the sanitized scene's basename
        '''
        fn = self.ui.lblBaseName.text() # sanitized filename
        date = None
        fn = ' '.join(
            ''.join(x if x.isalnum() else ' ' for x in fn).split())
        for token in ['(', ')', '-', '720p', '1080p', '2160p']:
            fn = fn.replace(token, ' ')
        try:
            date = QDateParser.parse(fn, fuzzy=True)
        except Exception as e:
            logger.info(e)
        if date is not None:
            self.ui.iReleaseDate.setDate(date) # set the parsed release date
