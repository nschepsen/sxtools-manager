# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sceneeditor.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QDateEdit, QFrame,
    QGridLayout, QGroupBox, QLabel, QLayout,
    QLineEdit, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_SceneEditor(object):
    def setupUi(self, SceneEditor):
        if not SceneEditor.objectName():
            SceneEditor.setObjectName(u"SceneEditor")
        SceneEditor.setProperty("modal", False)
        SceneEditor.setWindowModality(Qt.WindowModal)
        SceneEditor.resize(652, 352)
        SceneEditor.setMinimumSize(QSize(0, 0))
        self.gridLayout_3 = QGridLayout(SceneEditor)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setSizeConstraint(QLayout.SetFixedSize)
        self.performers = QGroupBox(SceneEditor)
        self.performers.setObjectName(u"performers")
        self.gridLayout_6 = QGridLayout(self.performers)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.iPerformer = QLineEdit(self.performers)
        self.iPerformer.setObjectName(u"iPerformer")
        self.iPerformer.setMinimumSize(QSize(150, 30))
        self.iPerformer.setStyleSheet(u"padding-left: 5px;")

        self.verticalLayout.addWidget(self.iPerformer)

        self.performerList = QListWidget(self.performers)
        self.performerList.setObjectName(u"performerList")
        self.performerList.setMaximumSize(QSize(150, 16777215))
        self.performerList.setStyleSheet(u"QListWidget::item {padding: 5px 0 5px 0;}")
        self.performerList.setFrameShape(QFrame.StyledPanel)
        self.performerList.setAlternatingRowColors(True)
        self.performerList.setSpacing(3)
        self.performerList.setSortingEnabled(True)

        self.verticalLayout.addWidget(self.performerList)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.btnAdd = QPushButton(self.performers)
        self.btnAdd.setObjectName(u"btnAdd")
        self.btnAdd.setMinimumSize(QSize(0, 30))

        self.verticalLayout_2.addWidget(self.btnAdd)

        self.btnDelete = QPushButton(self.performers)
        self.btnDelete.setObjectName(u"btnDelete")
        self.btnDelete.setMinimumSize(QSize(0, 30))

        self.verticalLayout_2.addWidget(self.btnDelete)

        self.vSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.vSpacer)

        self.btnClear = QPushButton(self.performers)
        self.btnClear.setObjectName(u"btnClear")
        self.btnClear.setMinimumSize(QSize(0, 30))

        self.verticalLayout_2.addWidget(self.btnClear)


        self.gridLayout.addLayout(self.verticalLayout_2, 0, 1, 1, 1)


        self.gridLayout_6.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.performers, 1, 1, 2, 1)

        self.path = QGroupBox(SceneEditor)
        self.path.setObjectName(u"path")
        self.path.setFlat(False)
        self.gridLayout_4 = QGridLayout(self.path)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.lblBaseName = QLabel(self.path)
        self.lblBaseName.setObjectName(u"lblBaseName")

        self.gridLayout_4.addWidget(self.lblBaseName, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.path, 0, 0, 1, 2)

        self.metadata = QGroupBox(SceneEditor)
        self.metadata.setObjectName(u"metadata")
        self.gridLayout_2 = QGridLayout(self.metadata)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.iTitle = QLineEdit(self.metadata)
        self.iTitle.setObjectName(u"iTitle")
        self.iTitle.setMinimumSize(QSize(250, 30))
        self.iTitle.setStyleSheet(u"padding-left: 5px;")

        self.gridLayout_2.addWidget(self.iTitle, 2, 1, 1, 3)

        self.lblDate = QLabel(self.metadata)
        self.lblDate.setObjectName(u"lblDate")
        self.lblDate.setMinimumSize(QSize(0, 30))
        self.lblDate.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.lblDate, 0, 0, 1, 1)

        self.lblTitle = QLabel(self.metadata)
        self.lblTitle.setObjectName(u"lblTitle")
        self.lblTitle.setMinimumSize(QSize(0, 30))
        self.lblTitle.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.lblTitle, 2, 0, 1, 1)

        self.lblPaysite = QLabel(self.metadata)
        self.lblPaysite.setObjectName(u"lblPaysite")
        self.lblPaysite.setMinimumSize(QSize(0, 30))
        self.lblPaysite.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.lblPaysite, 1, 0, 1, 1)

        self.pushButton = QPushButton(self.metadata)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(0, 30))
        self.pushButton.setMaximumSize(QSize(80, 16777215))

        self.gridLayout_2.addWidget(self.pushButton, 0, 2, 1, 1)

        self.btnResetDate = QPushButton(self.metadata)
        self.btnResetDate.setObjectName(u"btnResetDate")
        self.btnResetDate.setMinimumSize(QSize(0, 30))
        self.btnResetDate.setMaximumSize(QSize(80, 16777215))
        self.btnResetDate.setCheckable(False)
        self.btnResetDate.setFlat(False)

        self.gridLayout_2.addWidget(self.btnResetDate, 0, 3, 1, 1)

        self.iReleaseDate = QDateEdit(self.metadata)
        self.iReleaseDate.setObjectName(u"iReleaseDate")
        self.iReleaseDate.setMinimumSize(QSize(0, 30))
        self.iReleaseDate.setStyleSheet(u"padding-left: 5px;")
        self.iReleaseDate.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.iReleaseDate.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.iReleaseDate.setProperty("showGroupSeparator", False)
        self.iReleaseDate.setDateTime(QDateTime(QDate(2000, 1, 1), QTime(0, 0, 0)))
        self.iReleaseDate.setCalendarPopup(False)

        self.gridLayout_2.addWidget(self.iReleaseDate, 0, 1, 1, 1)

        self.iPaysite = QLineEdit(self.metadata)
        self.iPaysite.setObjectName(u"iPaysite")
        self.iPaysite.setMinimumSize(QSize(250, 30))
        self.iPaysite.setStyleSheet(u"padding-left: 5px;")

        self.gridLayout_2.addWidget(self.iPaysite, 1, 1, 1, 3)


        self.gridLayout_3.addWidget(self.metadata, 1, 0, 1, 1)

        self.groupBox = QGroupBox(SceneEditor)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_5 = QGridLayout(self.groupBox)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.thumbnail = QLabel(self.groupBox)
        self.thumbnail.setObjectName(u"thumbnail")
        self.thumbnail.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.thumbnail, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.groupBox, 2, 0, 1, 1)

        QWidget.setTabOrder(self.performerList, self.btnResetDate)
        QWidget.setTabOrder(self.btnResetDate, self.iReleaseDate)
        QWidget.setTabOrder(self.iReleaseDate, self.iPaysite)
        QWidget.setTabOrder(self.iPaysite, self.iTitle)

        self.retranslateUi(SceneEditor)
        self.btnClear.clicked.connect(self.performerList.clear)

        self.btnResetDate.setDefault(False)


        QMetaObject.connectSlotsByName(SceneEditor)
    # setupUi

    def retranslateUi(self, SceneEditor):
        SceneEditor.setWindowTitle(QCoreApplication.translate("SceneEditor", u"SxTools!MANAGER <Editor>", None))
        self.performers.setTitle(QCoreApplication.translate("SceneEditor", u"Performers", None))
        self.iPerformer.setPlaceholderText(QCoreApplication.translate("SceneEditor", u"Performer's Name", None))
        self.btnAdd.setText(QCoreApplication.translate("SceneEditor", u"Add", None))
        self.btnDelete.setText(QCoreApplication.translate("SceneEditor", u"Delete", None))
        self.btnClear.setText(QCoreApplication.translate("SceneEditor", u"Clear", None))
        self.path.setTitle(QCoreApplication.translate("SceneEditor", u"Basename", None))
        self.lblBaseName.setText("")
        self.metadata.setTitle(QCoreApplication.translate("SceneEditor", u"Metadata", None))
        self.lblDate.setText(QCoreApplication.translate("SceneEditor", u"Released:", None))
        self.lblTitle.setText(QCoreApplication.translate("SceneEditor", u"Scene Title:", None))
        self.lblPaysite.setText(QCoreApplication.translate("SceneEditor", u"Paysite:", None))
        self.pushButton.setText(QCoreApplication.translate("SceneEditor", u"Fetch", None))
        self.btnResetDate.setText(QCoreApplication.translate("SceneEditor", u"Reset", None))
        self.iReleaseDate.setSpecialValueText("")
        self.iReleaseDate.setDisplayFormat(QCoreApplication.translate("SceneEditor", u"yyyy-MM-dd", None))
        self.groupBox.setTitle(QCoreApplication.translate("SceneEditor", u"Thumbnails", None))
        self.thumbnail.setText(QCoreApplication.translate("SceneEditor", u"ICON", None))
    # retranslateUi

