# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QButtonGroup,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QListView, QMainWindow, QMenu, QMenuBar,
    QRadioButton, QSizePolicy, QSpacerItem, QStatusBar,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(927, 517)
        font = QFont()
        font.setBold(False)
        MainWindow.setFont(font)
        icon = QIcon()
        icon.addFile(u":/resources/light/video-camera.svg", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.aImport = QAction(MainWindow)
        self.aImport.setObjectName(u"aImport")
        icon1 = QIcon()
        iconThemeName = u"folder-open"
        if QIcon.hasThemeIcon(iconThemeName):
            icon1 = QIcon.fromTheme(iconThemeName)
        else:
            icon1.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.aImport.setIcon(icon1)
        self.aQuit = QAction(MainWindow)
        self.aQuit.setObjectName(u"aQuit")
        icon2 = QIcon()
        iconThemeName = u"application-exit"
        if QIcon.hasThemeIcon(iconThemeName):
            icon2 = QIcon.fromTheme(iconThemeName)
        else:
            icon2.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.aQuit.setIcon(icon2)
        self.aAbout = QAction(MainWindow)
        self.aAbout.setObjectName(u"aAbout")
        icon3 = QIcon()
        iconThemeName = u"help-about"
        if QIcon.hasThemeIcon(iconThemeName):
            icon3 = QIcon.fromTheme(iconThemeName)
        else:
            icon3.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.aAbout.setIcon(icon3)
        self.aAboutQt = QAction(MainWindow)
        self.aAboutQt.setObjectName(u"aAboutQt")
        self.aGitHub = QAction(MainWindow)
        self.aGitHub.setObjectName(u"aGitHub")
        icon4 = QIcon()
        iconThemeName = u"view-refresh"
        if QIcon.hasThemeIcon(iconThemeName):
            icon4 = QIcon.fromTheme(iconThemeName)
        else:
            icon4.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.aGitHub.setIcon(icon4)
        self.aSettings = QAction(MainWindow)
        self.aSettings.setObjectName(u"aSettings")
        icon5 = QIcon()
        iconThemeName = u"preferences-desktop"
        if QIcon.hasThemeIcon(iconThemeName):
            icon5 = QIcon.fromTheme(iconThemeName)
        else:
            icon5.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.aSettings.setIcon(icon5)
        self.aRelocate = QAction(MainWindow)
        self.aRelocate.setObjectName(u"aRelocate")
        self.aSave = QAction(MainWindow)
        self.aSave.setObjectName(u"aSave")
        icon6 = QIcon()
        iconThemeName = u"document-save"
        if QIcon.hasThemeIcon(iconThemeName):
            icon6 = QIcon.fromTheme(iconThemeName)
        else:
            icon6.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.aSave.setIcon(icon6)
        self.actionSortByName = QAction(MainWindow)
        self.actionSortByName.setObjectName(u"actionSortByName")
        self.actionSortByPerformers = QAction(MainWindow)
        self.actionSortByPerformers.setObjectName(u"actionSortByPerformers")
        self.actionSortByPaysite = QAction(MainWindow)
        self.actionSortByPaysite.setObjectName(u"actionSortByPaysite")
        self.actionReverseOrder = QAction(MainWindow)
        self.actionReverseOrder.setObjectName(u"actionReverseOrder")
        self.actionReverseOrder.setCheckable(True)
        self.actionFilterUntagged = QAction(MainWindow)
        self.actionFilterUntagged.setObjectName(u"actionFilterUntagged")
        self.actionFilterUntagged.setCheckable(True)
        self.actionFilterUntagged.setChecked(True)
        self.actionFilterTagged = QAction(MainWindow)
        self.actionFilterTagged.setObjectName(u"actionFilterTagged")
        self.actionFilterTagged.setCheckable(True)
        self.aScan = QAction(MainWindow)
        self.aScan.setObjectName(u"aScan")
        self.aClearCache = QAction(MainWindow)
        self.aClearCache.setObjectName(u"aClearCache")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.loNavigation = QHBoxLayout()
        self.loNavigation.setObjectName(u"loNavigation")
        self.leSearchField = QLineEdit(self.centralwidget)
        self.leSearchField.setObjectName(u"leSearchField")
        self.leSearchField.setMinimumSize(QSize(0, 30))
        self.leSearchField.setMaximumSize(QSize(230, 16777215))
        self.leSearchField.setStyleSheet(u"letter-spacing: 1px;")
        self.leSearchField.setAlignment(Qt.AlignCenter)
        self.leSearchField.setClearButtonEnabled(True)

        self.loNavigation.addWidget(self.leSearchField)

        self.lblFoundA = QLabel(self.centralwidget)
        self.lblFoundA.setObjectName(u"lblFoundA")
        self.lblFoundA.setFont(font)

        self.loNavigation.addWidget(self.lblFoundA)

        self.lblFoundB = QLabel(self.centralwidget)
        self.lblFoundB.setObjectName(u"lblFoundB")

        self.loNavigation.addWidget(self.lblFoundB)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.loNavigation.addItem(self.horizontalSpacer)

        self.lblSearch = QLabel(self.centralwidget)
        self.lblSearch.setObjectName(u"lblSearch")

        self.loNavigation.addWidget(self.lblSearch)

        self.rbPerformer = QRadioButton(self.centralwidget)
        self.bgFilterKeyColumns = QButtonGroup(MainWindow)
        self.bgFilterKeyColumns.setObjectName(u"bgFilterKeyColumns")
        self.bgFilterKeyColumns.addButton(self.rbPerformer)
        self.rbPerformer.setObjectName(u"rbPerformer")
        self.rbPerformer.setChecked(True)

        self.loNavigation.addWidget(self.rbPerformer)

        self.rbPaySite = QRadioButton(self.centralwidget)
        self.bgFilterKeyColumns.addButton(self.rbPaySite)
        self.rbPaySite.setObjectName(u"rbPaySite")

        self.loNavigation.addWidget(self.rbPaySite)

        self.rbTitle = QRadioButton(self.centralwidget)
        self.bgFilterKeyColumns.addButton(self.rbTitle)
        self.rbTitle.setObjectName(u"rbTitle")

        self.loNavigation.addWidget(self.rbTitle)


        self.gridLayout.addLayout(self.loNavigation, 0, 0, 1, 1)

        self.sceneView = QListView(self.centralwidget)
        self.sceneView.setObjectName(u"sceneView")
        font1 = QFont()
        font1.setBold(False)
        font1.setItalic(False)
        self.sceneView.setFont(font1)
        self.sceneView.setStyleSheet(u"QTableView::item\n"
"{\n"
"  border: 0px;\n"
"  padding: 5px;\n"
"}")
        self.sceneView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.sceneView.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.sceneView.setAlternatingRowColors(True)
        self.sceneView.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.sceneView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.sceneView.setTextElideMode(Qt.ElideNone)
        self.sceneView.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.sceneView.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.sceneView.setResizeMode(QListView.Fixed)
        self.sceneView.setSpacing(0)

        self.gridLayout.addWidget(self.sceneView, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 927, 19))
        self.mFile = QMenu(self.menubar)
        self.mFile.setObjectName(u"mFile")
        self.mEdit = QMenu(self.menubar)
        self.mEdit.setObjectName(u"mEdit")
        self.mHelp = QMenu(self.menubar)
        self.mHelp.setObjectName(u"mHelp")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.rbPerformer, self.rbPaySite)
        QWidget.setTabOrder(self.rbPaySite, self.rbTitle)
        QWidget.setTabOrder(self.rbTitle, self.leSearchField)
        QWidget.setTabOrder(self.leSearchField, self.sceneView)

        self.menubar.addAction(self.mFile.menuAction())
        self.menubar.addAction(self.mEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.mHelp.menuAction())
        self.mFile.addAction(self.aImport)
        self.mFile.addAction(self.aRelocate)
        self.mFile.addAction(self.aSave)
        self.mFile.addSeparator()
        self.mFile.addAction(self.aQuit)
        self.mEdit.addAction(self.aSettings)
        self.mHelp.addAction(self.aAbout)
        self.mHelp.addAction(self.aAboutQt)
        self.mHelp.addSeparator()
        self.mHelp.addAction(self.aGitHub)
        self.menuView.addAction(self.actionSortByPerformers)
        self.menuView.addAction(self.actionSortByName)
        self.menuView.addAction(self.actionSortByPaysite)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionReverseOrder)
        self.menuView.addSeparator()
        self.menuView.addAction(self.aScan)
        self.menuView.addAction(self.aClearCache)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionFilterTagged)
        self.menuView.addAction(self.actionFilterUntagged)

        self.retranslateUi(MainWindow)
        self.aQuit.triggered.connect(MainWindow.close)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"SxTools!MANAGER", None))
        self.aImport.setText(QCoreApplication.translate("MainWindow", u"Import Scene(s)", None))
#if QT_CONFIG(shortcut)
        self.aImport.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.aQuit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
#if QT_CONFIG(shortcut)
        self.aQuit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.aAbout.setText(QCoreApplication.translate("MainWindow", u"About SxTools!MANAGER", None))
#if QT_CONFIG(shortcut)
        self.aAbout.setShortcut(QCoreApplication.translate("MainWindow", u"F1", None))
#endif // QT_CONFIG(shortcut)
        self.aAboutQt.setText(QCoreApplication.translate("MainWindow", u"About Qt", None))
        self.aGitHub.setText(QCoreApplication.translate("MainWindow", u"Check for Updates @ GitHub", None))
        self.aSettings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.aRelocate.setText(QCoreApplication.translate("MainWindow", u"Move Collection", None))
        self.aSave.setText(QCoreApplication.translate("MainWindow", u"Save \"sxtools.map.json\"", None))
#if QT_CONFIG(tooltip)
        self.aSave.setToolTip(QCoreApplication.translate("MainWindow", u"Save", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.aSave.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionSortByName.setText(QCoreApplication.translate("MainWindow", u"Sort by Title", None))
        self.actionSortByPerformers.setText(QCoreApplication.translate("MainWindow", u"Sort by Performers", None))
        self.actionSortByPaysite.setText(QCoreApplication.translate("MainWindow", u"Sort by Paysite", None))
#if QT_CONFIG(tooltip)
        self.actionSortByPaysite.setToolTip(QCoreApplication.translate("MainWindow", u"Sort by Paysite", None))
#endif // QT_CONFIG(tooltip)
        self.actionReverseOrder.setText(QCoreApplication.translate("MainWindow", u"Reverse Sort Order", None))
        self.actionFilterUntagged.setText(QCoreApplication.translate("MainWindow", u"Filter out Untagged", None))
        self.actionFilterTagged.setText(QCoreApplication.translate("MainWindow", u"Filter out Tagged", None))
        self.aScan.setText(QCoreApplication.translate("MainWindow", u"Perform Scan", None))
        self.aClearCache.setText(QCoreApplication.translate("MainWindow", u"Clear Cache [0 MiB]", None))
#if QT_CONFIG(tooltip)
        self.leSearchField.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.leSearchField.setPlaceholderText(QCoreApplication.translate("MainWindow", u"SEARCH", None))
        self.lblFoundA.setText(QCoreApplication.translate("MainWindow", u"Found:", None))
        self.lblFoundB.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lblSearch.setText(QCoreApplication.translate("MainWindow", u"Search in:", None))
        self.rbPerformer.setText(QCoreApplication.translate("MainWindow", u"Performers", None))
        self.rbPaySite.setText(QCoreApplication.translate("MainWindow", u"Sites", None))
        self.rbTitle.setText(QCoreApplication.translate("MainWindow", u"Titles", None))
        self.mFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.mEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.mHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
    # retranslateUi

