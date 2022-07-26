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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_DecisionDialog(object):
    def setupUi(self, DecisionDialog):
        if not DecisionDialog.objectName():
            DecisionDialog.setObjectName(u"DecisionDialog")
        DecisionDialog.setWindowModality(Qt.NonModal)
        DecisionDialog.resize(516, 326)
        DecisionDialog.setModal(False)
        self.gridLayout = QGridLayout(DecisionDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gbScene = QGroupBox(DecisionDialog)
        self.gbScene.setObjectName(u"gbScene")
        self.horizontalLayout_3 = QHBoxLayout(self.gbScene)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lblScene = QLabel(self.gbScene)
        self.lblScene.setObjectName(u"lblScene")
        self.lblScene.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_3.addWidget(self.lblScene)


        self.gridLayout.addWidget(self.gbScene, 0, 0, 1, 1)

        self.gbSuggestions = QGroupBox(DecisionDialog)
        self.gbSuggestions.setObjectName(u"gbSuggestions")
        self.verticalLayout_2 = QVBoxLayout(self.gbSuggestions)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.loOptions = QVBoxLayout()
        self.loOptions.setObjectName(u"loOptions")
        self.rbOptionA = QRadioButton(self.gbSuggestions)
        self.rbOptionA.setObjectName(u"rbOptionA")
        self.rbOptionA.setEnabled(False)
        self.rbOptionA.setMinimumSize(QSize(0, 30))

        self.loOptions.addWidget(self.rbOptionA)

        self.rbOptionB = QRadioButton(self.gbSuggestions)
        self.rbOptionB.setObjectName(u"rbOptionB")
        self.rbOptionB.setEnabled(False)
        self.rbOptionB.setMinimumSize(QSize(0, 30))

        self.loOptions.addWidget(self.rbOptionB)

        self.rbOptionC = QRadioButton(self.gbSuggestions)
        self.rbOptionC.setObjectName(u"rbOptionC")
        self.rbOptionC.setEnabled(False)
        self.rbOptionC.setMinimumSize(QSize(0, 30))
        self.rbOptionC.setCheckable(True)

        self.loOptions.addWidget(self.rbOptionC)

        self.loOptionO = QHBoxLayout()
        self.loOptionO.setObjectName(u"loOptionO")
        self.rbOptionO = QRadioButton(self.gbSuggestions)
        self.rbOptionO.setObjectName(u"rbOptionO")

        self.loOptionO.addWidget(self.rbOptionO)

        self.leSuggestion = QLineEdit(self.gbSuggestions)
        self.leSuggestion.setObjectName(u"leSuggestion")
        self.leSuggestion.setMinimumSize(QSize(0, 30))
        self.leSuggestion.setStyleSheet(u"padding-left: 5px;")

        self.loOptionO.addWidget(self.leSuggestion)


        self.loOptions.addLayout(self.loOptionO)

        self.rbOptionN = QRadioButton(self.gbSuggestions)
        self.rbOptionN.setObjectName(u"rbOptionN")

        self.loOptions.addWidget(self.rbOptionN)


        self.verticalLayout_2.addLayout(self.loOptions)


        self.gridLayout.addWidget(self.gbSuggestions, 1, 0, 1, 1)

        self.loActions = QHBoxLayout()
        self.loActions.setObjectName(u"loActions")
        self.lblAttention = QLabel(DecisionDialog)
        self.lblAttention.setObjectName(u"lblAttention")

        self.loActions.addWidget(self.lblAttention)

        self.spcrActions = QSpacerItem(40, 27, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.loActions.addItem(self.spcrActions)

        self.btnConfirm = QPushButton(DecisionDialog)
        self.btnConfirm.setObjectName(u"btnConfirm")
        self.btnConfirm.setMinimumSize(QSize(0, 30))

        self.loActions.addWidget(self.btnConfirm)

        self.btnSkip = QPushButton(DecisionDialog)
        self.btnSkip.setObjectName(u"btnSkip")
        self.btnSkip.setMinimumSize(QSize(0, 30))

        self.loActions.addWidget(self.btnSkip)


        self.gridLayout.addLayout(self.loActions, 3, 0, 1, 1)


        self.retranslateUi(DecisionDialog)

        QMetaObject.connectSlotsByName(DecisionDialog)
    # setupUi

    def retranslateUi(self, DecisionDialog):
        DecisionDialog.setWindowTitle(QCoreApplication.translate("DecisionDialog", u"SxTools!MANAGER - Select a Performer", None))
        self.gbScene.setTitle(QCoreApplication.translate("DecisionDialog", u"Scene Name:", None))
        self.lblScene.setText("")
        self.gbSuggestions.setTitle(QCoreApplication.translate("DecisionDialog", u"Suggestions:", None))
        self.rbOptionA.setText(QCoreApplication.translate("DecisionDialog", u"A", None))
        self.rbOptionB.setText(QCoreApplication.translate("DecisionDialog", u"B", None))
        self.rbOptionC.setText(QCoreApplication.translate("DecisionDialog", u"C", None))
        self.rbOptionO.setText(QCoreApplication.translate("DecisionDialog", u"Type in your own option:", None))
        self.rbOptionN.setText(QCoreApplication.translate("DecisionDialog", u"None", None))
        self.lblAttention.setText(QCoreApplication.translate("DecisionDialog", u"Select \"None\" if the tail contains a scene name only", None))
        self.btnConfirm.setText(QCoreApplication.translate("DecisionDialog", u"OK", None))
        self.btnSkip.setText(QCoreApplication.translate("DecisionDialog", u"Cancel", None))
    # retranslateUi

