# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'splash_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QProgressBar, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Splash(object):
    def setupUi(self, Splash):
        if not Splash.objectName():
            Splash.setObjectName(u"Splash")
        Splash.resize(848, 392)
        Splash.setCursor(QCursor(Qt.CursorShape.BlankCursor))
        self.gridLayout = QGridLayout(Splash)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer = QSpacerItem(270, 22, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.welcome = QLabel(Splash)
        self.welcome.setObjectName(u"welcome")
        self.welcome.setStyleSheet(u"font: 28pt \"Times New Roman\";\n"
"border-radius:20px;\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0, stop:0 rgba(11, 151, 120, 239), stop:0.829545 rgba(85, 98, 112, 226));\n"
"color:rgba(255,255,255,255);")

        self.horizontalLayout.addWidget(self.welcome)

        self.horizontalSpacer = QSpacerItem(21, 38, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.progressBar = QProgressBar(Splash)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setStyleSheet(u"QProgressBar{\n"
"	font: 28pt \"Times New Roman\";\n"
"	color: rgb(255, 255, 255);\n"
"	border-top-right-radius:20px;\n"
"	border-bottom-left-radius:20px;\n"
"	border-bottom-right-radius:20px;\n"
"	border-top-left-radius:20px;\n"
"}\n"
"QProgressBar::chunk{\n"
"	background-color: rgb(45, 55, 69);\n"
"	border-top-right-radius:20px;\n"
"	border-bottom-left-radius:20px;\n"
"	border-bottom-right-radius:20px;\n"
"	border-top-left-radius:20px;\n"
"}")
        self.progressBar.setValue(24)

        self.verticalLayout.addWidget(self.progressBar)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(Splash)

        QMetaObject.connectSlotsByName(Splash)
    # setupUi

    def retranslateUi(self, Splash):
        Splash.setWindowTitle(QCoreApplication.translate("Splash", u"Form", None))
        self.welcome.setText(QCoreApplication.translate("Splash", u"<html><head/><body><p align=\"center\">Zero Security</p></body></html>", None))
    # retranslateUi

