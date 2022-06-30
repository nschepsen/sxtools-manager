# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'itemdeligate.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QSizePolicy,
    QSpacerItem, QWidget)
import icons_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(433, 82)
        self.gridLayout_3 = QGridLayout(Form)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalSpacer = QSpacerItem(86, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 1, 1, 1)

        self.dateLabel = QLabel(Form)
        self.dateLabel.setObjectName(u"dateLabel")
        self.dateLabel.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.dateLabel, 0, 2, 1, 1)

        self.paysite = QLabel(Form)
        self.paysite.setObjectName(u"paysite")

        self.gridLayout.addWidget(self.paysite, 1, 0, 1, 1)

        self.performers = QLabel(Form)
        self.performers.setObjectName(u"performers")

        self.gridLayout.addWidget(self.performers, 0, 0, 1, 1)

        self.size = QLabel(Form)
        self.size.setObjectName(u"size")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.size.setFont(font)
        self.size.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.size, 1, 2, 1, 1)

        self.title = QLabel(Form)
        self.title.setObjectName(u"title")

        self.gridLayout.addWidget(self.title, 3, 0, 1, 1)

        self.resolution = QLabel(Form)
        self.resolution.setObjectName(u"resolution")
        self.resolution.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.resolution, 3, 2, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 1, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.dateLabel.setText(QCoreApplication.translate("Form", u"None", None))
        self.paysite.setText(QCoreApplication.translate("Form", u"paysite", None))
        self.performers.setText(QCoreApplication.translate("Form", u"performers", None))
        self.size.setText(QCoreApplication.translate("Form", u"0,0 GiB", None))
        self.title.setText(QCoreApplication.translate("Form", u"title", None))
        self.resolution.setText(QCoreApplication.translate("Form", u"not yet scanned", None))
    # retranslateUi

