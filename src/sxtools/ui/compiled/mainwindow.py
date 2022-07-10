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
        self.aOpen = QAction(MainWindow)
        self.aOpen.setObjectName(u"aOpen")
        icon1 = QIcon()
        iconThemeName = u"folder-open"
        if QIcon.hasThemeIcon(iconThemeName):
            icon1 = QIcon.fromTheme(iconThemeName)
        else:
            icon1.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.aOpen.setIcon(icon1)
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
        self.aAboutQt.setMenuRole(QAction.AboutQtRole)
        self.aUpdate = QAction(MainWindow)
        self.aUpdate.setObjectName(u"aUpdate")
        icon4 = QIcon()
        iconThemeName = u"view-refresh"
        if QIcon.hasThemeIcon(iconThemeName):
            icon4 = QIcon.fromTheme(iconThemeName)
        else:
            icon4.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.aUpdate.setIcon(icon4)
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
        self.actionSortByTitle = QAction(MainWindow)
        self.actionSortByTitle.setObjectName(u"actionSortByTitle")
        self.actionSortByTitle.setCheckable(True)
        self.actionSortByPerformers = QAction(MainWindow)
        self.actionSortByPerformers.setObjectName(u"actionSortByPerformers")
        self.actionSortByPerformers.setCheckable(True)
        self.actionSortByPaysite = QAction(MainWindow)
        self.actionSortByPaysite.setObjectName(u"actionSortByPaysite")
        self.actionSortByPaysite.setCheckable(True)
        self.actionSortOrder = QAction(MainWindow)
        self.actionSortOrder.setObjectName(u"actionSortOrder")
        self.actionSortOrder.setCheckable(True)
        icon7 = QIcon()
        iconThemeName = u"reverse"
        if QIcon.hasThemeIcon(iconThemeName):
            icon7 = QIcon.fromTheme(iconThemeName)
        else:
            icon7.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.actionSortOrder.setIcon(icon7)
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
        icon8 = QIcon()
        iconThemeName = u"delete"
        if QIcon.hasThemeIcon(iconThemeName):
            icon8 = QIcon.fromTheme(iconThemeName)
        else:
            icon8.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.aClearCache.setIcon(icon8)
        self.actionAdd_a_Collection = QAction(MainWindow)
        self.actionAdd_a_Collection.setObjectName(u"actionAdd_a_Collection")
        self.actionSortBySize = QAction(MainWindow)
        self.actionSortBySize.setObjectName(u"actionSortBySize")
        self.actionSortBySize.setCheckable(True)
        self.actionSortByReleaseDate = QAction(MainWindow)
        self.actionSortByReleaseDate.setObjectName(u"actionSortByReleaseDate")
        self.actionSortByReleaseDate.setCheckable(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.loNavigation = QHBoxLayout()
        self.loNavigation.setObjectName(u"loNavigation")
        self.leSearchField = QLineEdit(self.centralwidget)
        self.leSearchField.setObjectName(u"leSearchField")
        self.leSearchField.setMinimumSize(QSize(300, 30))
        self.leSearchField.setMaximumSize(QSize(230, 16777215))
        self.leSearchField.setStyleSheet(u"letter-spacing: 1px;")
        self.leSearchField.setAlignment(Qt.AlignCenter)
        self.leSearchField.setClearButtonEnabled(True)

        self.loNavigation.addWidget(self.leSearchField)

        self.lblFiltredLabel = QLabel(self.centralwidget)
        self.lblFiltredLabel.setObjectName(u"lblFiltredLabel")
        self.lblFiltredLabel.setFont(font)

        self.loNavigation.addWidget(self.lblFiltredLabel)

        self.lblFiltredCount = QLabel(self.centralwidget)
        self.lblFiltredCount.setObjectName(u"lblFiltredCount")

        self.loNavigation.addWidget(self.lblFiltredCount)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.loNavigation.addItem(self.horizontalSpacer)

        self.lblSearch = QLabel(self.centralwidget)
        self.lblSearch.setObjectName(u"lblSearch")

        self.loNavigation.addWidget(self.lblSearch)

        self.rbPerformers = QRadioButton(self.centralwidget)
        self.bgFilterRoles = QButtonGroup(MainWindow)
        self.bgFilterRoles.setObjectName(u"bgFilterRoles")
        self.bgFilterRoles.addButton(self.rbPerformers)
        self.rbPerformers.setObjectName(u"rbPerformers")
        self.rbPerformers.setChecked(True)

        self.loNavigation.addWidget(self.rbPerformers)

        self.rbPaysites = QRadioButton(self.centralwidget)
        self.bgFilterRoles.addButton(self.rbPaysites)
        self.rbPaysites.setObjectName(u"rbPaysites")

        self.loNavigation.addWidget(self.rbPaysites)

        self.rbTitles = QRadioButton(self.centralwidget)
        self.bgFilterRoles.addButton(self.rbTitles)
        self.rbTitles.setObjectName(u"rbTitles")

        self.loNavigation.addWidget(self.rbTitles)


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
        QWidget.setTabOrder(self.leSearchField, self.rbPerformers)
        QWidget.setTabOrder(self.rbPerformers, self.rbPaysites)
        QWidget.setTabOrder(self.rbPaysites, self.rbTitles)
        QWidget.setTabOrder(self.rbTitles, self.sceneView)

        self.menubar.addAction(self.mFile.menuAction())
        self.menubar.addAction(self.mEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.mHelp.menuAction())
        self.mFile.addAction(self.aOpen)
        self.mFile.addAction(self.aRelocate)
        self.mFile.addAction(self.aSave)
        self.mFile.addSeparator()
        self.mFile.addAction(self.aQuit)
        self.mEdit.addAction(self.actionAdd_a_Collection)
        self.mEdit.addSeparator()
        self.mEdit.addAction(self.aSettings)
        self.mHelp.addAction(self.aAbout)
        self.mHelp.addAction(self.aAboutQt)
        self.mHelp.addSeparator()
        self.mHelp.addAction(self.aUpdate)
        self.menuView.addAction(self.actionSortByPerformers)
        self.menuView.addAction(self.actionSortByTitle)
        self.menuView.addAction(self.actionSortByPaysite)
        self.menuView.addAction(self.actionSortBySize)
        self.menuView.addAction(self.actionSortByReleaseDate)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionSortOrder)
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
        self.aOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
#if QT_CONFIG(shortcut)
        self.aOpen.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
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
        self.aUpdate.setText(QCoreApplication.translate("MainWindow", u"Check for Updates @ GitHub", None))
        self.aSettings.setText(QCoreApplication.translate("MainWindow", u"General Settings", None))
        self.aRelocate.setText(QCoreApplication.translate("MainWindow", u"Add to Collection", None))
        self.aSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
#if QT_CONFIG(tooltip)
        self.aSave.setToolTip(QCoreApplication.translate("MainWindow", u"Save", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.aSave.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionSortByTitle.setText(QCoreApplication.translate("MainWindow", u"Sort by Title", None))
        self.actionSortByPerformers.setText(QCoreApplication.translate("MainWindow", u"Sort by Performers", None))
        self.actionSortByPaysite.setText(QCoreApplication.translate("MainWindow", u"Sort by Paysite", None))
#if QT_CONFIG(tooltip)
        self.actionSortByPaysite.setToolTip(QCoreApplication.translate("MainWindow", u"Sort by Paysite", None))
#endif // QT_CONFIG(tooltip)
        self.actionSortOrder.setText(QCoreApplication.translate("MainWindow", u"Reverse Sort Order", None))
        self.actionFilterUntagged.setText(QCoreApplication.translate("MainWindow", u"Filter out Untagged", None))
        self.actionFilterTagged.setText(QCoreApplication.translate("MainWindow", u"Filter out Tagged", None))
        self.aScan.setText(QCoreApplication.translate("MainWindow", u"Perform Scan", None))
        self.aClearCache.setText(QCoreApplication.translate("MainWindow", u"Clear Cache [0 MiB]", None))
        self.actionAdd_a_Collection.setText(QCoreApplication.translate("MainWindow", u"Add a Collection", None))
        self.actionSortBySize.setText(QCoreApplication.translate("MainWindow", u"Sort by Size", None))
        self.actionSortByReleaseDate.setText(QCoreApplication.translate("MainWindow", u"Sort by Release Date", None))
#if QT_CONFIG(tooltip)
        self.leSearchField.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.leSearchField.setPlaceholderText(QCoreApplication.translate("MainWindow", u"SEARCH", None))
        self.lblFiltredLabel.setText(QCoreApplication.translate("MainWindow", u"Found:", None))
        self.lblFiltredCount.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lblSearch.setText(QCoreApplication.translate("MainWindow", u"Search in:", None))
        self.rbPerformers.setText(QCoreApplication.translate("MainWindow", u"Performers", None))
        self.rbPaysites.setText(QCoreApplication.translate("MainWindow", u"Paysites", None))
        self.rbTitles.setText(QCoreApplication.translate("MainWindow", u"Titles", None))
        self.mFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.mEdit.setTitle(QCoreApplication.translate("MainWindow", u"Collections", None))
        self.mHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
    # retranslateUi

