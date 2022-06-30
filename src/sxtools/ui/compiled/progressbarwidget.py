# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'progressbarwidget.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QProgressBar, QSizePolicy,
    QWidget)

class Ui_ProgressWidget(object):
    def setupUi(self, ProgressWidget):
        if not ProgressWidget.objectName():
            ProgressWidget.setObjectName(u"ProgressWidget")
        ProgressWidget.resize(400, 45)
        self.gridLayout = QGridLayout(ProgressWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.progressBar = QProgressBar(ProgressWidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.gridLayout.addWidget(self.progressBar, 0, 0, 1, 1)


        self.retranslateUi(ProgressWidget)

        QMetaObject.connectSlotsByName(ProgressWidget)
    # setupUi

    def retranslateUi(self, ProgressWidget):
        ProgressWidget.setWindowTitle(QCoreApplication.translate("ProgressWidget", u"Processing", None))
        self.progressBar.setFormat(QCoreApplication.translate("ProgressWidget", u"%p %", None))
    # retranslateUi

