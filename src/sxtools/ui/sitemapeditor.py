from re import S
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHeaderView, QListWidgetItem, QTableWidgetItem, QTreeWidgetItem, QWidget
from sxtools.ui.compiled.sitemapeditor import Ui_SitemapEditor


class SitemapEditor(QWidget):

    def __init__(self, sitemap, parent = None) -> None:
        '''
        '''
        super(SitemapEditor, self).__init__(parent)
        self.ui = Ui_SitemapEditor()
        self.ui.setupUi(self) # load UI elements
        self.ui.unknowns.addItems(
            sitemap.get('undefined', []))
        self.populateTree(sitemap.get('networks'), self.ui.networks)
        self.ui.paysites.addItems(sitemap.get('sites', []))
        self.populateTable(sitemap.get('acronyms', []))
        self.ui.acronyms.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # connect UI elements, QLineEdit:@Networks
        self.ui.fNetwork.textChanged.connect(self.onNetworkFilterChanged)
        # connect UI elements, QLineEdit:@Paysites
        self.ui.fPaysite.textChanged.connect(self.onPaysiteFilterChanged)
        # connect UI elements, QLineEdit:@Acronyms
        self.ui.fAcronym.textChanged.connect(self.onAcronymFilterChanged)
        # connect UI elements, QPushButton:@Unknowns
        self.ui.btnResolveAcronym.clicked.connect(self.onResolveAcronymClicked)
        # connect UI elements, QPushButton:@Networks
        # connect UI elements, QPushButton:@Paysites
        self.ui.btnAppendPaysite.clicked.connect(self.onAppendPaysiteClicked)
        self.ui.btnDeletePaysite.clicked.connect(self.onDeletePaysiteClicked)
        # connect UI elements, QPushButton:@Acronyms
        self.ui.btnAppendAcronym.clicked.connect(self.onAppendAcronymClicked)
        self.ui.btnDeleteAcronym.clicked.connect(self.onDeleteAcronymClicked)

    def populateTable(self, value) -> None:
        '''
        populate acronym table with known acronyms
        '''
        for row, data in enumerate(value.items()):
            self.ui.acronyms.insertRow(row)
            for col, x in enumerate(data):
                item = QTableWidgetItem(x)
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.acronyms.setItem(row, col, item)
        # self.ui.statusbar.showMessage(f'{len(value)} acronym(s) loaded')

    def populateTree(self, value, parent = None):
        '''
        populate network tree with known networks
        '''
        if isinstance(value, dict):
            for k, v in value.items():
                item = QTreeWidgetItem(parent)
                item.setText(0, k)
                self.populateTree(v, item)
        elif isinstance(value, list):
            for i in value:
                item = QTreeWidgetItem(parent); item.setText(0, i)
        else:
            parent.setText(1, value)
        # self.ui.statusbar.showMessage(f'{len(value)} networks(s) loaded')

    def onAcronymFilterChanged(self, s: str) -> None:
        '''
        handle AcronymFilter changing
        '''
        table = self.ui.acronyms # acronyms widget
        for row in range(table.rowCount()):
            item = table.item(row, 0)
            table.setRowHidden(
                row, s.lower() not in item.text().lower())
        # TODO: update filter'd items count label

    def onPaysiteFilterChanged(self, s: str) -> None:
        '''
        handle PaysiteFilter changing
        '''
        list = self.ui.paysites # paysite widget
        for row in range(list.count()):
            item = list.item(row)
            item.setHidden(s.lower() not in item.text().lower())
        # TODO: update filter'd items count label

    def onNetworkFilterChanged(self, s: str) -> None:
        '''
        handle NetworkFilter changing
        '''
        tree = self.ui.networks # network widget
        for row in range(tree.topLevelItemCount()):
            network = tree.topLevelItem(row)
            hidden = 0
            for i in range(network.childCount()):
                b = s.lower() not in network.child(i).text(0).lower()
                network.child(i).setHidden(b)
                hidden += b # track hidden
            network.setHidden(hidden == network.childCount())
        # TODO: update filter'd items count label, but implement it first

    def onResolveAcronymClicked(self) -> None:
        '''
        assign undefined paysites to their definitions
        '''
        row = self.ui.unknowns.currentRow()
        if row == -1:
            return
        self.onAppendAcronymClicked()
        self.ui.acronyms.item(0, 0).setText(
            self.ui.unknowns.item(row).text())
        value = self.ui.paysites.selectedItems() or self.ui.networks.selectedItems()
        if value:
            value = value[0]
            self.ui.acronyms.item(0, 1).setText(
                (value.text() if isinstance(value, QListWidgetItem) else value.text(0)).lower())
        self.ui.unknowns.takeItem(row)
        self.ui.unknowns.clearSelection() # clear selection

    def onAppendAcronymClicked(self) -> None:
        '''
        append an empty acronym assignment to the table
        '''
        self.ui.acronyms.insertRow(0)
        for c in range(self.ui.acronyms.columnCount()):
            item = QTableWidgetItem()
            item.setTextAlignment(
                Qt.AlignCenter)
            self.ui.acronyms.setItem(0, c, item)
        # WARN: Don't let an empty Item be stored into database

    def onDeleteAcronymClicked(self) -> None:
        '''
        remove a selected acronym from the table
        '''
        row = self.ui.acronyms.currentRow()
        if row != -1:
            self.ui.acronyms.removeRow(row)
        self.ui.acronyms.clearSelection() # unselect

    def onAppendPaysiteClicked(self) -> None:
        '''
        append a pre-defined paysite to the list
        '''
        paysite = self.ui.fPaysite.text().strip()
        if paysite:
            self.ui.paysites.insertItem(0, QListWidgetItem(paysite))
        self.ui.fPaysite.setText('') # clear fPaysite

    def onDeletePaysiteClicked(self) -> None:
        '''
        remove a selected paysite from the list
        '''
        row = self.ui.paysites.currentRow()
        if row != -1:
            self.ui.paysites.takeItem(row)
        self.ui.acronyms.clearSelection() # clear selection
