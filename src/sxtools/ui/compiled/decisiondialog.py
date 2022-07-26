# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'decisiondialog.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
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
from PySide6.QtWidgets import (QApplication, QButtonGroup, QDialog, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)
import sxtools.ui.compiled.icons

class Ui_DecisionDialog(object):
    def setupUi(self, DecisionDialog):
        if not DecisionDialog.objectName():
            DecisionDialog.setObjectName(u"DecisionDialog")
        DecisionDialog.setWindowModality(Qt.NonModal)
        DecisionDialog.resize(516, 218)
        DecisionDialog.setModal(False)
        self.gridLayout = QGridLayout(DecisionDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gbContext = QGroupBox(DecisionDialog)
        self.gbContext.setObjectName(u"gbContext")
        self.horizontalLayout_3 = QHBoxLayout(self.gbContext)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lblContext = QLabel(self.gbContext)
        self.lblContext.setObjectName(u"lblContext")
        self.lblContext.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_3.addWidget(self.lblContext)


        self.gridLayout.addWidget(self.gbContext, 0, 0, 1, 1)

        self.gbOptions = QGroupBox(DecisionDialog)
        self.gbOptions.setObjectName(u"gbOptions")
        self.verticalLayout_2 = QVBoxLayout(self.gbOptions)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.loOptions = QVBoxLayout()
        self.loOptions.setObjectName(u"loOptions")
        self.loOptionO = QHBoxLayout()
        self.loOptionO.setObjectName(u"loOptionO")
        self.rbOptionOther = QRadioButton(self.gbOptions)
        self.bgOptions = QButtonGroup(DecisionDialog)
        self.bgOptions.setObjectName(u"bgOptions")
        self.bgOptions.addButton(self.rbOptionOther)
        self.rbOptionOther.setObjectName(u"rbOptionOther")

        self.loOptionO.addWidget(self.rbOptionOther)

        self.leOption = QLineEdit(self.gbOptions)
        self.leOption.setObjectName(u"leOption")
        self.leOption.setEnabled(True)
        self.leOption.setMinimumSize(QSize(0, 30))
        self.leOption.setStyleSheet(u"padding-left: 5px;")

        self.loOptionO.addWidget(self.leOption)


        self.loOptions.addLayout(self.loOptionO)

        self.rbOptionNone = QRadioButton(self.gbOptions)
        self.bgOptions.addButton(self.rbOptionNone)
        self.rbOptionNone.setObjectName(u"rbOptionNone")

        self.loOptions.addWidget(self.rbOptionNone)


        self.verticalLayout_2.addLayout(self.loOptions)


        self.gridLayout.addWidget(self.gbOptions, 1, 0, 1, 1)

        self.loActions = QHBoxLayout()
        self.loActions.setObjectName(u"loActions")
        self.lblAnnotation = QLabel(DecisionDialog)
        self.lblAnnotation.setObjectName(u"lblAnnotation")

        self.loActions.addWidget(self.lblAnnotation)

        self.spcrActions = QSpacerItem(40, 27, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.loActions.addItem(self.spcrActions)

        self.btnConfirm = QPushButton(DecisionDialog)
        self.btnConfirm.setObjectName(u"btnConfirm")
        self.btnConfirm.setMinimumSize(QSize(0, 30))
        icon = QIcon()
        icon.addFile(u":/resources/light/check-mark.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btnConfirm.setIcon(icon)

        self.loActions.addWidget(self.btnConfirm)

        self.btnSkip = QPushButton(DecisionDialog)
        self.btnSkip.setObjectName(u"btnSkip")
        self.btnSkip.setMinimumSize(QSize(0, 30))
        icon1 = QIcon()
        icon1.addFile(u":/resources/light/close.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btnSkip.setIcon(icon1)

        self.loActions.addWidget(self.btnSkip)


        self.gridLayout.addLayout(self.loActions, 3, 0, 1, 1)


        self.retranslateUi(DecisionDialog)
        self.btnConfirm.clicked.connect(DecisionDialog.accept)
        self.btnSkip.clicked.connect(DecisionDialog.reject)

        QMetaObject.connectSlotsByName(DecisionDialog)
    # setupUi

    def retranslateUi(self, DecisionDialog):
        DecisionDialog.setWindowTitle(QCoreApplication.translate("DecisionDialog", u"SxTools!MANAGER - Make your Decision", None))
        self.gbContext.setTitle(QCoreApplication.translate("DecisionDialog", u"Context:", None))
        self.lblContext.setText("")
        self.gbOptions.setTitle(QCoreApplication.translate("DecisionDialog", u"Options:", None))
        self.rbOptionOther.setText(QCoreApplication.translate("DecisionDialog", u"Other", None))
        self.rbOptionNone.setText(QCoreApplication.translate("DecisionDialog", u"None of Them", None))
        self.lblAnnotation.setText(QCoreApplication.translate("DecisionDialog", u"Select \"None\" if the tail contains a scene name only", None))
        self.btnConfirm.setText(QCoreApplication.translate("DecisionDialog", u"OK", None))
        self.btnSkip.setText(QCoreApplication.translate("DecisionDialog", u"Cancel", None))
    # retranslateUi

