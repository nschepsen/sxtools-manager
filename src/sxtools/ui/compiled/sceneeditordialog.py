# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sceneeditordialog.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QDateEdit, QDialog,
    QFrame, QGridLayout, QGroupBox, QLabel,
    QLayout, QLineEdit, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QSpacerItem, QWidget)

class Ui_SceneEditor(object):
    def setupUi(self, SceneEditor):
        if not SceneEditor.objectName():
            SceneEditor.setObjectName(u"SceneEditor")
        SceneEditor.setWindowModality(Qt.WindowModal)
        SceneEditor.resize(628, 364)
        SceneEditor.setMinimumSize(QSize(0, 0))
        SceneEditor.setModal(True)
        self.gridLayout_3 = QGridLayout(SceneEditor)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setSizeConstraint(QLayout.SetFixedSize)
        self.path = QGroupBox(SceneEditor)
        self.path.setObjectName(u"path")
        self.gridLayout_4 = QGridLayout(self.path)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.basename = QLabel(self.path)
        self.basename.setObjectName(u"basename")
        self.basename.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.basename, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.path, 0, 0, 1, 2)

        self.metadata = QGroupBox(SceneEditor)
        self.metadata.setObjectName(u"metadata")
        self.gridLayout_2 = QGridLayout(self.metadata)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.lblTitle = QLabel(self.metadata)
        self.lblTitle.setObjectName(u"lblTitle")
        self.lblTitle.setMinimumSize(QSize(0, 30))
        self.lblTitle.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.lblTitle, 2, 0, 1, 1)

        self.btnFetchDate = QPushButton(self.metadata)
        self.btnFetchDate.setObjectName(u"btnFetchDate")
        self.btnFetchDate.setMinimumSize(QSize(0, 30))
        self.btnFetchDate.setMaximumSize(QSize(80, 16777215))
        self.btnFetchDate.setCheckable(False)
        self.btnFetchDate.setFlat(False)

        self.gridLayout_2.addWidget(self.btnFetchDate, 0, 2, 1, 1)

        self.lblPaysite = QLabel(self.metadata)
        self.lblPaysite.setObjectName(u"lblPaysite")
        self.lblPaysite.setMinimumSize(QSize(0, 30))
        self.lblPaysite.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.lblPaysite, 1, 0, 1, 1)

        self.iReleaseDate = QDateEdit(self.metadata)
        self.iReleaseDate.setObjectName(u"iReleaseDate")
        self.iReleaseDate.setMinimumSize(QSize(0, 30))
        self.iReleaseDate.setAlignment(Qt.AlignCenter)
        self.iReleaseDate.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.iReleaseDate.setProperty("showGroupSeparator", False)
        self.iReleaseDate.setCalendarPopup(False)

        self.gridLayout_2.addWidget(self.iReleaseDate, 0, 1, 1, 1)

        self.iTitle = QLineEdit(self.metadata)
        self.iTitle.setObjectName(u"iTitle")
        self.iTitle.setMinimumSize(QSize(250, 30))
        self.iTitle.setStyleSheet(u"padding-left: 5px;")

        self.gridLayout_2.addWidget(self.iTitle, 2, 1, 1, 2)

        self.iPaysite = QLineEdit(self.metadata)
        self.iPaysite.setObjectName(u"iPaysite")
        self.iPaysite.setMinimumSize(QSize(250, 30))
        self.iPaysite.setStyleSheet(u"padding-left: 5px;")

        self.gridLayout_2.addWidget(self.iPaysite, 1, 1, 1, 2)

        self.lblDate = QLabel(self.metadata)
        self.lblDate.setObjectName(u"lblDate")
        self.lblDate.setMinimumSize(QSize(0, 30))
        self.lblDate.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.lblDate, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.metadata, 1, 0, 1, 1)

        self.performers = QGroupBox(SceneEditor)
        self.performers.setObjectName(u"performers")
        self.gridLayout = QGridLayout(self.performers)
        self.gridLayout.setObjectName(u"gridLayout")
        self.vSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.vSpacer, 4, 1, 1, 1)

        self.performerList = QListWidget(self.performers)
        QListWidgetItem(self.performerList)
        QListWidgetItem(self.performerList)
        self.performerList.setObjectName(u"performerList")
        self.performerList.setMaximumSize(QSize(150, 16777215))
        self.performerList.setStyleSheet(u"QListWidget::item {padding: 5px 0 5px 0;}")
        self.performerList.setFrameShape(QFrame.StyledPanel)
        self.performerList.setAlternatingRowColors(True)
        self.performerList.setSpacing(3)
        self.performerList.setSortingEnabled(True)

        self.gridLayout.addWidget(self.performerList, 1, 0, 4, 1)

        self.iPerformer = QLineEdit(self.performers)
        self.iPerformer.setObjectName(u"iPerformer")
        self.iPerformer.setMinimumSize(QSize(150, 30))
        self.iPerformer.setStyleSheet(u"padding-left: 5px;")

        self.gridLayout.addWidget(self.iPerformer, 0, 0, 1, 1)

        self.btnAdd = QPushButton(self.performers)
        self.btnAdd.setObjectName(u"btnAdd")
        self.btnAdd.setMinimumSize(QSize(0, 30))

        self.gridLayout.addWidget(self.btnAdd, 0, 1, 1, 1)

        self.btnDelete = QPushButton(self.performers)
        self.btnDelete.setObjectName(u"btnDelete")
        self.btnDelete.setMinimumSize(QSize(0, 30))

        self.gridLayout.addWidget(self.btnDelete, 1, 1, 1, 1)


        self.gridLayout_3.addWidget(self.performers, 1, 1, 2, 1)

        self.verticalSpacer = QSpacerItem(20, 112, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer, 2, 0, 1, 1)

        QWidget.setTabOrder(self.performerList, self.btnFetchDate)
        QWidget.setTabOrder(self.btnFetchDate, self.iReleaseDate)
        QWidget.setTabOrder(self.iReleaseDate, self.iPaysite)
        QWidget.setTabOrder(self.iPaysite, self.iTitle)

        self.retranslateUi(SceneEditor)

        self.btnFetchDate.setDefault(False)


        QMetaObject.connectSlotsByName(SceneEditor)
    # setupUi

    def retranslateUi(self, SceneEditor):
        SceneEditor.setWindowTitle(QCoreApplication.translate("SceneEditor", u"Dialog", None))
        self.path.setTitle(QCoreApplication.translate("SceneEditor", u"Scenename:", None))
        self.basename.setText(QCoreApplication.translate("SceneEditor", u"PLACEHOLDER", None))
        self.metadata.setTitle(QCoreApplication.translate("SceneEditor", u"Metadata:", None))
        self.lblTitle.setText(QCoreApplication.translate("SceneEditor", u"Scene Title:", None))
        self.btnFetchDate.setText(QCoreApplication.translate("SceneEditor", u"Fetch", None))
        self.lblPaysite.setText(QCoreApplication.translate("SceneEditor", u"Paysite:", None))
        self.iReleaseDate.setSpecialValueText("")
        self.iReleaseDate.setDisplayFormat(QCoreApplication.translate("SceneEditor", u"yyyy-MM-dd", None))
        self.lblDate.setText(QCoreApplication.translate("SceneEditor", u"Released:", None))
        self.performers.setTitle(QCoreApplication.translate("SceneEditor", u"Performers:", None))

        __sortingEnabled = self.performerList.isSortingEnabled()
        self.performerList.setSortingEnabled(False)
        ___qlistwidgetitem = self.performerList.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("SceneEditor", u"Nicole Aniston", None));
        ___qlistwidgetitem1 = self.performerList.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("SceneEditor", u"Sara Jay Syren", None));
        self.performerList.setSortingEnabled(__sortingEnabled)

        self.btnAdd.setText(QCoreApplication.translate("SceneEditor", u"Add", None))
        self.btnDelete.setText(QCoreApplication.translate("SceneEditor", u"Delete", None))
    # retranslateUi

