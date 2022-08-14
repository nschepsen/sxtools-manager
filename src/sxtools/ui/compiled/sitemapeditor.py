# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sitemapeditor.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLineEdit,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QTableWidget, QTableWidgetItem, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

class Ui_SitemapEditor(object):
    def setupUi(self, SitemapEditor):
        if not SitemapEditor.objectName():
            SitemapEditor.setObjectName(u"SitemapEditor")
        SitemapEditor.setWindowModality(Qt.ApplicationModal)
        SitemapEditor.resize(930, 738)
        self.gridLayout_5 = QGridLayout(SitemapEditor)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gbNetworks = QGroupBox(SitemapEditor)
        self.gbNetworks.setObjectName(u"gbNetworks")
        self.gbNetworks.setMinimumSize(QSize(267, 0))
        self.gbNetworks.setMaximumSize(QSize(300, 16777215))
        self.gridLayout = QGridLayout(self.gbNetworks)
        self.gridLayout.setObjectName(u"gridLayout")
        self.networks = QTreeWidget(self.gbNetworks)
        self.networks.setObjectName(u"networks")
        self.networks.setStyleSheet(u"QTreeWidget::item {padding: 5px; }")
        self.networks.setLineWidth(1)
        self.networks.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.networks.setDragDropMode(QAbstractItemView.NoDragDrop)
        self.networks.setIndentation(20)
        self.networks.setRootIsDecorated(True)
        self.networks.setItemsExpandable(True)
        self.networks.setSortingEnabled(False)
        self.networks.setAnimated(True)
        self.networks.setColumnCount(1)
        self.networks.header().setVisible(False)

        self.gridLayout.addWidget(self.networks, 1, 0, 1, 1)

        self.fNetwork = QLineEdit(self.gbNetworks)
        self.fNetwork.setObjectName(u"fNetwork")
        self.fNetwork.setStyleSheet(u"padding: 5px;")
        self.fNetwork.setClearButtonEnabled(True)

        self.gridLayout.addWidget(self.fNetwork, 0, 0, 1, 1)

        self.btnClearNetworks = QPushButton(self.gbNetworks)
        self.btnClearNetworks.setObjectName(u"btnClearNetworks")
        self.btnClearNetworks.setStyleSheet(u"padding: 5px;")

        self.gridLayout.addWidget(self.btnClearNetworks, 2, 0, 1, 1)


        self.gridLayout_5.addWidget(self.gbNetworks, 1, 0, 1, 1)

        self.gbAcronyms = QGroupBox(SitemapEditor)
        self.gbAcronyms.setObjectName(u"gbAcronyms")
        self.gbAcronyms.setMinimumSize(QSize(300, 720))
        self.gbAcronyms.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_2 = QGridLayout(self.gbAcronyms)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.fAcronym = QLineEdit(self.gbAcronyms)
        self.fAcronym.setObjectName(u"fAcronym")
        self.fAcronym.setStyleSheet(u"padding: 5px;")
        self.fAcronym.setClearButtonEnabled(True)

        self.gridLayout_2.addWidget(self.fAcronym, 0, 0, 1, 1)

        self.btnAppendAcronym = QPushButton(self.gbAcronyms)
        self.btnAppendAcronym.setObjectName(u"btnAppendAcronym")
        self.btnAppendAcronym.setMinimumSize(QSize(80, 0))
        self.btnAppendAcronym.setMaximumSize(QSize(80, 16777215))
        self.btnAppendAcronym.setStyleSheet(u"padding: 5px;")

        self.gridLayout_2.addWidget(self.btnAppendAcronym, 0, 1, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.acronyms = QTableWidget(self.gbAcronyms)
        if (self.acronyms.columnCount() < 2):
            self.acronyms.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.acronyms.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.acronyms.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.acronyms.setObjectName(u"acronyms")
        self.acronyms.setStyleSheet(u"QTableWidget::item {padding: 5px; }")
        self.acronyms.setAutoScroll(False)
        self.acronyms.setAlternatingRowColors(False)
        self.acronyms.setSelectionMode(QAbstractItemView.SingleSelection)
        self.acronyms.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.acronyms.setShowGrid(True)
        self.acronyms.setSortingEnabled(True)
        self.acronyms.setCornerButtonEnabled(True)
        self.acronyms.horizontalHeader().setVisible(True)
        self.acronyms.horizontalHeader().setStretchLastSection(True)
        self.acronyms.verticalHeader().setVisible(False)
        self.acronyms.verticalHeader().setCascadingSectionResizes(False)
        self.acronyms.verticalHeader().setStretchLastSection(False)

        self.verticalLayout.addWidget(self.acronyms)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btnDeleteAcronym = QPushButton(self.gbAcronyms)
        self.btnDeleteAcronym.setObjectName(u"btnDeleteAcronym")
        self.btnDeleteAcronym.setMinimumSize(QSize(80, 0))
        self.btnDeleteAcronym.setMaximumSize(QSize(16777215, 16777215))
        self.btnDeleteAcronym.setStyleSheet(u"padding: 5px;")

        self.horizontalLayout.addWidget(self.btnDeleteAcronym)

        self.btnClearAcronyms = QPushButton(self.gbAcronyms)
        self.btnClearAcronyms.setObjectName(u"btnClearAcronyms")
        self.btnClearAcronyms.setMinimumSize(QSize(0, 0))
        self.btnClearAcronyms.setMaximumSize(QSize(16777215, 16777215))
        self.btnClearAcronyms.setStyleSheet(u"padding: 5px;")

        self.horizontalLayout.addWidget(self.btnClearAcronyms)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.gridLayout_2.addLayout(self.verticalLayout, 1, 0, 1, 2)


        self.gridLayout_5.addWidget(self.gbAcronyms, 0, 1, 2, 1)

        self.gbSoloPaysites = QGroupBox(SitemapEditor)
        self.gbSoloPaysites.setObjectName(u"gbSoloPaysites")
        self.gbSoloPaysites.setMinimumSize(QSize(300, 0))
        self.gbSoloPaysites.setMaximumSize(QSize(300, 16777215))
        self.gridLayout_3 = QGridLayout(self.gbSoloPaysites)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.fPaysite = QLineEdit(self.gbSoloPaysites)
        self.fPaysite.setObjectName(u"fPaysite")
        self.fPaysite.setStyleSheet(u"padding: 5px;")
        self.fPaysite.setClearButtonEnabled(True)

        self.gridLayout_3.addWidget(self.fPaysite, 0, 0, 1, 1)

        self.btnAppendPaysite = QPushButton(self.gbSoloPaysites)
        self.btnAppendPaysite.setObjectName(u"btnAppendPaysite")
        self.btnAppendPaysite.setMinimumSize(QSize(80, 0))
        self.btnAppendPaysite.setMaximumSize(QSize(80, 16777215))
        self.btnAppendPaysite.setStyleSheet(u"padding: 5px;")

        self.gridLayout_3.addWidget(self.btnAppendPaysite, 0, 1, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.paysites = QListWidget(self.gbSoloPaysites)
        self.paysites.setObjectName(u"paysites")
        self.paysites.setStyleSheet(u"QListWidget::item {padding: 5px; }")
        self.paysites.setAlternatingRowColors(True)
        self.paysites.setSpacing(3)
        self.paysites.setSortingEnabled(True)

        self.verticalLayout_2.addWidget(self.paysites)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.btnDeletePaysite = QPushButton(self.gbSoloPaysites)
        self.btnDeletePaysite.setObjectName(u"btnDeletePaysite")
        self.btnDeletePaysite.setMinimumSize(QSize(80, 0))
        self.btnDeletePaysite.setStyleSheet(u"padding: 5px;")

        self.horizontalLayout_2.addWidget(self.btnDeletePaysite)

        self.btnClearPaysites = QPushButton(self.gbSoloPaysites)
        self.btnClearPaysites.setObjectName(u"btnClearPaysites")
        self.btnClearPaysites.setMinimumSize(QSize(0, 0))
        self.btnClearPaysites.setMaximumSize(QSize(16777215, 16777215))
        self.btnClearPaysites.setStyleSheet(u"padding: 5px;")

        self.horizontalLayout_2.addWidget(self.btnClearPaysites)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.gridLayout_3.addLayout(self.verticalLayout_2, 1, 0, 1, 2)


        self.gridLayout_5.addWidget(self.gbSoloPaysites, 0, 2, 2, 1)

        self.gbUnknownPaysites = QGroupBox(SitemapEditor)
        self.gbUnknownPaysites.setObjectName(u"gbUnknownPaysites")
        self.gbUnknownPaysites.setMinimumSize(QSize(267, 0))
        self.gbUnknownPaysites.setMaximumSize(QSize(300, 16777215))
        self.gridLayout_4 = QGridLayout(self.gbUnknownPaysites)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.unknowns = QListWidget(self.gbUnknownPaysites)
        self.unknowns.setObjectName(u"unknowns")
        self.unknowns.setMinimumSize(QSize(0, 0))
        self.unknowns.setStyleSheet(u"QListWidget::item {padding: 5px; }")
        self.unknowns.setDragEnabled(False)
        self.unknowns.setAlternatingRowColors(True)
        self.unknowns.setSpacing(3)

        self.gridLayout_4.addWidget(self.unknowns, 0, 0, 2, 1)

        self.btnResolveAcronym = QPushButton(self.gbUnknownPaysites)
        self.btnResolveAcronym.setObjectName(u"btnResolveAcronym")
        self.btnResolveAcronym.setStyleSheet(u"padding: 5px;")

        self.gridLayout_4.addWidget(self.btnResolveAcronym, 0, 1, 1, 1)

        self.btnClearUnknowns = QPushButton(self.gbUnknownPaysites)
        self.btnClearUnknowns.setObjectName(u"btnClearUnknowns")
        self.btnClearUnknowns.setMaximumSize(QSize(80, 16777215))
        self.btnClearUnknowns.setStyleSheet(u"padding: 5px;")

        self.gridLayout_4.addWidget(self.btnClearUnknowns, 1, 1, 1, 1)


        self.gridLayout_5.addWidget(self.gbUnknownPaysites, 0, 0, 1, 1)


        self.retranslateUi(SitemapEditor)
        self.btnClearPaysites.clicked.connect(self.paysites.clearSelection)
        self.btnClearNetworks.clicked.connect(self.networks.clearSelection)
        self.btnClearAcronyms.clicked.connect(self.acronyms.clearSelection)
        self.btnClearUnknowns.clicked.connect(self.unknowns.clearSelection)

        QMetaObject.connectSlotsByName(SitemapEditor)
    # setupUi

    def retranslateUi(self, SitemapEditor):
        SitemapEditor.setWindowTitle(QCoreApplication.translate("SitemapEditor", u"Sitemap Editor", None))
        self.gbNetworks.setTitle(QCoreApplication.translate("SitemapEditor", u"Networks", None))
        ___qtreewidgetitem = self.networks.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("SitemapEditor", u"Key", None));
        self.fNetwork.setPlaceholderText(QCoreApplication.translate("SitemapEditor", u"Look for a network", None))
        self.btnClearNetworks.setText(QCoreApplication.translate("SitemapEditor", u"Unselect", None))
        self.gbAcronyms.setTitle(QCoreApplication.translate("SitemapEditor", u"Acronyms", None))
        self.fAcronym.setPlaceholderText(QCoreApplication.translate("SitemapEditor", u"Look for an acronym", None))
        self.btnAppendAcronym.setText(QCoreApplication.translate("SitemapEditor", u"Append", None))
        ___qtablewidgetitem = self.acronyms.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("SitemapEditor", u"Acronym", None));
        ___qtablewidgetitem1 = self.acronyms.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("SitemapEditor", u"Value", None));
        self.btnDeleteAcronym.setText(QCoreApplication.translate("SitemapEditor", u"Remove", None))
        self.btnClearAcronyms.setText(QCoreApplication.translate("SitemapEditor", u"Unselect", None))
        self.gbSoloPaysites.setTitle(QCoreApplication.translate("SitemapEditor", u"Solo Paysites", None))
        self.fPaysite.setPlaceholderText(QCoreApplication.translate("SitemapEditor", u"Look for a paysite", None))
        self.btnAppendPaysite.setText(QCoreApplication.translate("SitemapEditor", u"Append", None))
        self.btnDeletePaysite.setText(QCoreApplication.translate("SitemapEditor", u"Remove", None))
        self.btnClearPaysites.setText(QCoreApplication.translate("SitemapEditor", u"Unselect", None))
        self.gbUnknownPaysites.setTitle(QCoreApplication.translate("SitemapEditor", u"Unknown Paysites", None))
        self.btnResolveAcronym.setText(QCoreApplication.translate("SitemapEditor", u"Append", None))
        self.btnClearUnknowns.setText(QCoreApplication.translate("SitemapEditor", u"Clear", None))
    # retranslateUi

