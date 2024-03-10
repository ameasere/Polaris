# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QLineEdit,
    QMainWindow, QProgressBar, QPushButton, QSizePolicy,
    QStackedWidget, QVBoxLayout, QWidget)
from .resources_rc import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 720)
        icon = QIcon()
        icon.addFile(u":/images/images/images/icon.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.styleSheet = QWidget(MainWindow)
        self.styleSheet.setObjectName(u"styleSheet")
        self.styleSheet.setStyleSheet(u"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"\n"
"SET APP STYLESHEET - FULL STYLES HERE\n"
"DARK THEME - DRACULA COLOR BASED\n"
"\n"
"///////////////////////////////////////////////////////////////////////////////////////////////// */\n"
"\n"
"QWidget{\n"
"	color: rgb(221, 221, 221);\n"
"	font: 10pt \"Inter Medium\" 400;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Tooltip */\n"
"QToolTip {\n"
"	color: #ffffff;\n"
"	background-color: rgba(33, 37, 43, 180);\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"	background-image: none;\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 2px solid rgb(189, 147, 249);\n"
"	text-align: left;\n"
"	padding-left: 8px;\n"
"	margin: 0px;\n"
"	font: 10pt \"Inter\";\n"
"}\n"
"\n"
"#home QPushButton {\n"
"	background-color: rgba(255, 255, 255, 70);\n"
"	border: 1px solid white;\n"
"}\n"
"#"
                        "home QPushButton:hover {\n"
"	background-color: rgba(255, 255, 255, 150);\n"
"	border: 1px solid white;\n"
"	image: url(:/icons/images/icons/cil-plus.png);\n"
"}\n"
"\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Bg App */\n"
"#bgApp {	\n"
"	background-color: #001010;\n"
"	border: 1px solid rgb(33,39,38);\n"
"	border-radius: 20px;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Left Menu */\n"
"#leftMenuBg {	\n"
"	background-color: rgb(4, 10, 11);\n"
"	border-radius: 10px;\n"
"}\n"
"#topLogo {\n"
"	background-color: rgb(4, 10, 11);\n"
"	background-image: url(:/images/images/images/Polaris.png);\n"
"	background-position: center center;\n"
"	background-repeat: no-repeat;\n"
"}\n"
"\n"
"#titleLeftDescription { color: rgb(189, 147, 249); }\n"
"\n"
"/* MENUS */\n"
"#topMenu .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border:"
                        " none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color: transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"	font: 10pt \"Inter Medium\";\n"
"	color: rgb(95, 106, 106);\n"
"}\n"
"#topMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"#topMenu .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	font: 10pt \"Inter SemiBold\";\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"#bottomMenu .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 20px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"	font: 10pt \"Inter Medium\";\n"
"	color: rgb(95, 106, 106);\n"
"}\n"
"#bottomMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#bottomMenu .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"	font: 10pt \"Inter SemiBold\""
                        ";\n"
"}\n"
"\n"
"#leftMenuFrame{\n"
"	border-top: 3px solid rgb(33,39,38);\n"
"}\n"
"/* Toggle Button */\n"
"#toggleButton {\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 20px solid transparent;\n"
"	background-color: rgb(37, 41, 48);\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"	color: rgb(113, 126, 149);\n"
"}\n"
"#toggleButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#toggleButton:pressed {\n"
"	background-color: rgb(189, 147, 249);\n"
"}\n"
"\n"
"/* Title Menu */\n"
"#titleRightInfo { \n"
"	padding-left: 10px; \n"
"}\n"
"\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Extra Tab */\n"
"#extraLeftBox {	\n"
"	background-color: rgb(4, 10, 11);\n"
"}\n"
"#extraTopBg{	\n"
"	background-color: rgb(189, 147, 249);\n"
"}\n"
"\n"
"/* Label */\n"
"#extraLabel { color: rgb(255, 255, 255); }\n"
"\n"
"/* Btn Close */\n"
"#extraCloseColumnBtn { background-color: rgb"
                        "a(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#extraCloseColumnBtn:hover { background-color: rgb(196, 161, 249); border-style: solid; border-radius: 4px; }\n"
"#extraCloseColumnBtn:pressed { background-color: rgb(189, 147, 249); border-style: solid; border-radius: 4px; }\n"
"\n"
"/* Extra Content */\n"
"#extraContent{\n"
"	border-top: 3px solid rgb(33,39,38);\n"
"}\n"
"\n"
"/* Extra Top Menus */\n"
"#extraTopMenu .QPushButton {\n"
"background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"	font: 10pt \"Inter SemiBold\";\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"#extraTopMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#extraTopMenu .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"	font: 10pt \"Inter SemiBold\";	\n"
"}\n"
"\n"
"/* //////////////////////////"
                        "///////////////////////////////////////////////////////////////////////\n"
"Content App */\n"
"#contentTopBg{	\n"
"	background-color: rgb(4, 10, 11);\n"
"	border-radius: 10px;\n"
"}\n"
"#contentBottom{\n"
"	border-top: 3px solid rgb(33,39,38);\n"
"}\n"
"\n"
"/* Top Buttons */\n"
"#rightButtons .QPushButton { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#rightButtons .QPushButton:hover { background-color: rgb(44, 49, 57); border-style: solid; border-radius: 4px; }\n"
"#rightButtons .QPushButton:pressed { background-color: rgb(23, 26, 30); border-style: solid; border-radius: 4px; }\n"
"\n"
"/* Theme Settings */\n"
"#extraRightBox { background-color: rgb(44, 49, 58); }\n"
"#themeSettingsTopDetail { background-color: rgb(189, 147, 249); }\n"
"\n"
"/* Bottom Bar */\n"
"#bottomBar { background-color: rgb(4, 10, 11);\n"
"	border-bottom-left-radius: 10px;\n"
"	border-bottom-right-radius: 10px;\n"
" }\n"
"#bottomBar QLabel { font-size: 11px; color: rgb(113, 126, 149); padding-left:"
                        " 10px; padding-right: 10px; padding-bottom: 2px; }\n"
"\n"
"/* CONTENT SETTINGS */\n"
"/* MENUS */\n"
"#contentSettings .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"	font: 10pt \"Inter SemiBold\";\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"#contentSettings .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#contentSettings .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"	font: 10pt \"Inter SemiBold\";\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"QTableWidget */\n"
"QTableWidget {	\n"
"	background-color: transparent;\n"
"	padding: 10px;\n"
"	border-radius: 5px;\n"
"	gridline-color: rgb(44, 49, 58);\n"
"	border-bottom: 1px solid rgb(33,39,38);\n"
"}\n"
"QTableWidget::item{\n"
""
                        "	border-color: rgb(44, 49, 60);\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"	gridline-color: rgb(33,39,38);\n"
"}\n"
"QTableWidget::item:selected{\n"
"	background-color: rgb(189, 147, 249);\n"
"}\n"
"QHeaderView::section{\n"
"	background-color: rgb(33, 37, 43);\n"
"	max-width: 30px;\n"
"	border: 1px solid rgb(33,39,38);\n"
"	border-style: none;\n"
"    border-bottom: 1px solid rgb(33,39,38);\n"
"    border-right: 1px solid rgb(33,39,38);\n"
"}\n"
"QTableWidget::horizontalHeader {	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    border: 1px solid rgb(33,39,38);\n"
"	background-color: rgb(33,39,38);\n"
"	padding: 3px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"}\n"
"QHeaderView::section:vertical\n"
"{\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"LineEdit */\n"
"QLineEdit {\n"
"	background-color: rgb(33, 37, "
                        "43);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33,39,38);\n"
"	padding-left: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: rgb(189, 147, 249);\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"PlainTextEdit */\n"
"QPlainTextEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	padding: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: rgb(189, 147, 249);\n"
"}\n"
"QPlainTextEdit  QScrollBar:vertical {\n"
"    width: 8px;\n"
" }\n"
"QPlainTextEdit  QScrollBar:horizontal {\n"
"    height: 8px;\n"
" }\n"
"QPlainTextEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QPlainTextEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* //////////////////////////////////////////////////////"
                        "///////////////////////////////////////////\n"
"ScrollBars */\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 8px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    background: rgb(189, 147, 249);\n"
"    min-width: 25px;\n"
"	border-radius: 4px\n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-right-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-bottom-left-radius: 4px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
"QScroll"
                        "Bar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 8px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
" QScrollBar::handle:vertical {	\n"
"	background: rgb(189, 147, 249);\n"
"    min-height: 25px;\n"
"	border-radius: 4px\n"
" }\n"
" QScrollBar::add-line:vertical {\n"
"     border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-bottom-left-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"     subcontrol-position: bottom;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::sub-line:vertical {\n"
"	border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    height: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"     subcontrol-position: top;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"     backgroun"
                        "d: none;\n"
" }\n"
"\n"
" QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CheckBox */\n"
"QCheckBox::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(33,39,38);\n"
"}\n"
"QCheckBox::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: 3px solid rgb(52, 59, 72);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"	background-image: url(:/icons/images/icons/cil-check-alt.png);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"RadioButton */\n"
"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButto"
                        "n::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ComboBox */\n"
"QComboBox{\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33,39,38);\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"}\n"
"QComboBox:hover{\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QComboBox::drop-down {\n"
"	subcontrol-origin: padding;\n"
"	subcontrol-position: top right;\n"
"	width: 25px; \n"
"	border-left-width: 3px;\n"
"	border-left-color: rgba(39, 44, 54, 150);\n"
"	border-left-style: solid;\n"
"	border-top-right-radius: 3px;\n"
"	border-bottom-right-radius: 3px;	\n"
"	background-image: url(:/icons/images/icons/cil-arrow-bottom.png);\n"
"	background-position: center;\n"
"	background-repeat: no-reperat;\n"
" }\n"
"QComboBox Q"
                        "AbstractItemView {\n"
"	color: rgb(189, 147, 249);	\n"
"	background-color: rgb(33, 37, 43);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Sliders */\n"
"QSlider::groove:horizontal {\n"
"    border-radius: 5px;\n"
"    height: 10px;\n"
"	margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:horizontal:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:horizontal {\n"
"    background-color: rgb(189, 147, 249);\n"
"    border: none;\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:horizontal:hover {\n"
"    background-color: rgb(195, 155, 255);\n"
"}\n"
"QSlider::handle:horizontal:pressed {\n"
"    background-color: rgb(189, 147, 249);\n"
"}\n"
"\n"
"QSlider::groove:vertical {\n"
"    border-radius: 5px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	backgroun"
                        "d-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:vertical:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:vertical {\n"
"    background-color: rgb(189, 147, 249);\n"
"	border: none;\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:vertical:hover {\n"
"    background-color: rgb(195, 155, 255);\n"
"}\n"
"QSlider::handle:vertical:pressed {\n"
"    background-color: rgb(189, 147, 249);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CommandLinkButton */\n"
"QCommandLinkButton {	\n"
"	color: rgb(189, 147, 249);\n"
"	border-radius: 5px;\n"
"	padding: 5px;\n"
"	color: rgb(255, 170, 255);\n"
"}\n"
"QCommandLinkButton:hover {	\n"
"	color: rgb(255, 170, 255);\n"
"	background-color: rgb(44, 49, 60);\n"
"}\n"
"QCommandLinkButton:pressed {	\n"
"	color: rgb(189, 147, 249);\n"
"	background-color: rgb(52, 58, 71);\n"
"}\n"
"\n"
"/* //////////////////////////////"
                        "///////////////////////////////////////////////////////////////////\n"
"Button */\n"
"#pagesContainer QPushButton {\n"
"	border: 2px solid rgb(33,39,38);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"	font: 10pt \"Inter SemiBold\";\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"#pagesContainer QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"#pagesContainer QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"	font: 10pt \"Inter SemiBold\";\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"")
        self.verticalLayout_2 = QVBoxLayout(self.styleSheet)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.bgApp = QFrame(self.styleSheet)
        self.bgApp.setObjectName(u"bgApp")
        self.bgApp.setStyleSheet(u"#btn_dropdown {\n"
"	background-color: #9e77ed;\n"
"	border-style: outset;\n"
"	border-width: 2px;\n"
"	border-radius: 15px;\n"
"	border-color: rgb(181, 181, 181);\n"
"	padding: 4px;\n"
"}\n"
"\n"
"#btn_dropdown:hover {\n"
"	background-color: #9e77ed;\n"
"	border-style: outset;\n"
"	border-width: 2px;\n"
"	border-radius: 15px;\n"
"	border-color: rgb(181, 181, 181);\n"
"	padding: 4px;\n"
"}\n"
"#btn_dropdown:pressed {\n"
"	background-color: #fff;\n"
"	border-style: outset;\n"
"	border-width: 1px;\n"
"	border-radius: 15px;\n"
"	border-color: white;\n"
"	padding: 4px;\n"
"}")
        self.bg1 = QLabel(self.bgApp)
        self.bg1.setObjectName(u"bg1")
        self.bg1.setGeometry(QRect(0, 0, 261, 701))
        self.bg1.setStyleSheet(u"border-top-left-radius: 20px;\n"
"border-bottom-left-radius: 20px;\n"
"background-color: rgba(40, 27, 40, 150);\n"
"border: 1px solid rgba(128, 96, 167, 80);")
        self.bg2 = QLabel(self.bgApp)
        self.bg2.setObjectName(u"bg2")
        self.bg2.setGeometry(QRect(261, 1, 1001, 191))
        self.bg2.setStyleSheet(u"border-top-right-radius: 20px;\n"
"background-color: rgba(40, 27, 40, 150);\n"
"border-bottom: 1px solid rgba(128, 96, 167, 80);\n"
"border-right: 1px solid rgba(128, 96, 167, 80);\n"
"border-top: 1px solid rgba(128, 96, 167, 80);")
        self.bg3 = QLabel(self.bgApp)
        self.bg3.setObjectName(u"bg3")
        self.bg3.setGeometry(QRect(311, 241, 951, 461))
        self.bg3.setStyleSheet(u"border-top-left-radius: 20px;\n"
"border-bottom-right-radius: 20px;\n"
"background-color: rgba(40, 27, 40, 150);\n"
"border: 1px solid rgba(128, 96, 167, 80);")
        self.btn_dashboard = QPushButton(self.bgApp)
        self.btn_dashboard.setObjectName(u"btn_dashboard")
        self.btn_dashboard.setGeometry(QRect(89, 80, 131, 21))
        self.btn_dashboard.setMinimumSize(QSize(120, 15))
        font = QFont()
        font.setFamilies([u"Inter Medium"])
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        self.btn_dashboard.setFont(font)
        self.btn_dashboard.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_dashboard.setStyleSheet(u"#btn_dashboard {\n"
"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: left;\n"
"color: #fff;\n"
"border-radius: 5px;\n"
"}\n"
"#btn_dashboard:hover {\n"
"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: left;\n"
"color: #fff;\n"
"border-radius: 5px;\n"
"}\n"
"#btn_dashboard:pressed {\n"
"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: left;\n"
"color: #9e77ed;\n"
"border-radius: 5px;\n"
"}")
        self.icon_1 = QLabel(self.bgApp)
        self.icon_1.setObjectName(u"icon_1")
        self.icon_1.setGeometry(QRect(40, 80, 20, 20))
        self.icon_1.setStyleSheet(u"")
        self.icon_1.setPixmap(QPixmap(u":/icons/images/icons/home_selected.png"))
        self.icon_1.setScaledContents(False)
        self.sep1 = QLabel(self.bgApp)
        self.sep1.setObjectName(u"sep1")
        self.sep1.setGeometry(QRect(70, 86, 10, 10))
        self.sep1.setStyleSheet(u"")
        self.sep1.setPixmap(QPixmap(u":/icons/images/icons/separator.png"))
        self.sep1.setScaledContents(True)
        self.btn_documentation = QPushButton(self.bgApp)
        self.btn_documentation.setObjectName(u"btn_documentation")
        self.btn_documentation.setGeometry(QRect(89, 126, 131, 21))
        self.btn_documentation.setMinimumSize(QSize(120, 15))
        self.btn_documentation.setFont(font)
        self.btn_documentation.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_documentation.setStyleSheet(u"#btn_documentation {\n"
"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: left;\n"
"color: #A29F9F;\n"
"border-radius: 5px;\n"
"}\n"
"#btn_documentation:hover {\n"
"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: left;\n"
"color: #fff;\n"
"border-radius: 5px;\n"
"}\n"
"#btn_documentation:pressed {\n"
"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: left;\n"
"color: #9e77ed;\n"
"border-radius: 5px;\n"
"}")
        self.icon_2 = QLabel(self.bgApp)
        self.icon_2.setObjectName(u"icon_2")
        self.icon_2.setGeometry(QRect(40, 126, 20, 20))
        self.icon_2.setStyleSheet(u"")
        self.icon_2.setPixmap(QPixmap(u":/icons/images/icons/edit_unselected.png"))
        self.icon_2.setScaledContents(False)
        self.sep2 = QLabel(self.bgApp)
        self.sep2.setObjectName(u"sep2")
        self.sep2.setGeometry(QRect(70, 132, 10, 10))
        self.sep2.setStyleSheet(u"")
        self.sep2.setPixmap(QPixmap(u":/icons/images/icons/separator_inactive.png"))
        self.sep2.setScaledContents(True)
        self.sep3 = QLabel(self.bgApp)
        self.sep3.setObjectName(u"sep3")
        self.sep3.setGeometry(QRect(70, 178, 10, 10))
        self.sep3.setStyleSheet(u"")
        self.sep3.setPixmap(QPixmap(u":/icons/images/icons/separator_inactive.png"))
        self.sep3.setScaledContents(True)
        self.icon_3 = QLabel(self.bgApp)
        self.icon_3.setObjectName(u"icon_3")
        self.icon_3.setGeometry(QRect(40, 172, 20, 20))
        self.icon_3.setStyleSheet(u"")
        self.icon_3.setPixmap(QPixmap(u":/icons/images/icons/user.png"))
        self.icon_3.setScaledContents(False)
        self.btn_account = QPushButton(self.bgApp)
        self.btn_account.setObjectName(u"btn_account")
        self.btn_account.setGeometry(QRect(89, 172, 131, 21))
        self.btn_account.setMinimumSize(QSize(120, 15))
        self.btn_account.setFont(font)
        self.btn_account.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_account.setStyleSheet(u"#btn_account {\n"
"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: left;\n"
"color: #A29F9F;\n"
"border-radius: 5px;\n"
"}\n"
"#btn_account:hover {\n"
"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: left;\n"
"color: #fff;\n"
"border-radius: 5px;\n"
"}\n"
"#btn_account:pressed {\n"
"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: left;\n"
"color: #9e77ed;\n"
"border-radius: 5px;\n"
"}")
        self.ctx_btns = QFrame(self.bgApp)
        self.ctx_btns.setObjectName(u"ctx_btns")
        self.ctx_btns.setGeometry(QRect(1080, 20, 161, 161))
        self.ctx_btns.setStyleSheet(u"QFrame  {\n"
"	background-color: rgb(40, 27, 40);\n"
"	background: solid;\n"
"	border: 2px solid rgb(157, 122, 222);\n"
"	border-radius: 15px;\n"
"}")
        self.ctx_btns.setFrameShape(QFrame.StyledPanel)
        self.ctx_btns.setFrameShadow(QFrame.Raised)
        self.btn_minimize = QPushButton(self.ctx_btns)
        self.btn_minimize.setObjectName(u"btn_minimize")
        self.btn_minimize.setGeometry(QRect(67, 2, 31, 31))
        self.btn_minimize.setMinimumSize(QSize(10, 10))
        font1 = QFont()
        font1.setFamilies([u"Be Vietnam Pro"])
        font1.setPointSize(9)
        font1.setBold(False)
        font1.setItalic(False)
        self.btn_minimize.setFont(font1)
        self.btn_minimize.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_minimize.setStyleSheet(u"#btn_minimize {\n"
"background-color: transparent;\n"
"font: 500 9pt \"Be Vietnam Pro\";\n"
"text-align: left;\n"
"color: #A29F9F;\n"
"background-image: url(:/icons/images/icons/minimize.png);\n"
"background-position: center center;\n"
"background-repeat: no-repeat;\n"
"background-size: cover; \n"
"padding: 0;\n"
"margin: 0;\n"
"border-radius: 5px;\n"
"}\n"
"#btn_minimize:hover {\n"
"background-color: #2e3043;\n"
"border-color: rgb(238, 238, 238);\n"
"border: 2px solid;\n"
"font: 500 9pt \"Be Vietnam Pro\";\n"
"text-align: left;\n"
"color: #A29F9F;\n"
"background-image: url(:/icons/images/icons/minimize.png);\n"
"background-position: center center;\n"
"background-repeat: no-repeat;\n"
"border-radius: 5px;\n"
"border: 1px solid rgba(40, 27, 40, 150);\n"
"}\n"
"#btn_minimize:pressed {\n"
"background-color: rgb(93, 93, 93);\n"
"border: 1px solid #2e3043;\n"
"font: 500 9pt \"Be Vietnam Pro\";\n"
"text-align: left;\n"
"color: #A29F9F;\n"
"background-image: url(:/icons/images/icons/minimize.png);\n"
"background-posi"
                        "tion: center center;\n"
"background-repeat: no-repeat;\n"
"border-radius: 5px;\n"
"}\n"
"")
        self.btn_minimize.setIconSize(QSize(21, 21))
        self.btn_close = QPushButton(self.ctx_btns)
        self.btn_close.setObjectName(u"btn_close")
        self.btn_close.setGeometry(QRect(100, 2, 31, 31))
        self.btn_close.setMinimumSize(QSize(10, 10))
        self.btn_close.setFont(font1)
        self.btn_close.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_close.setStyleSheet(u"#btn_close {\n"
"background-color: transparent;\n"
"font: 500 9pt \"Be Vietnam Pro\";\n"
"text-align: left;\n"
"color: #A29F9F;\n"
"background-image: url(:/icons/images/icons/x.png);\n"
"background-position: center center;\n"
"background-repeat: no-repeat;\n"
"background-position: center center;\n"
"background-repeat: no-repeat;\n"
"background-size: cover; \n"
"padding: 0;\n"
"margin: 0;\n"
"border-radius: 5px;\n"
"}\n"
"#btn_close:hover {\n"
"background-color: #2e3043;\n"
"border-color: rgb(238, 238, 238);\n"
"border: 2px solid;\n"
"font: 500 9pt \"Be Vietnam Pro\";\n"
"text-align: left;\n"
"color: #A29F9F;\n"
"background-image: url(:/icons/images/icons/x.png);\n"
"background-position: center center;\n"
"background-repeat: no-repeat;\n"
"border-radius: 5px;\n"
"border: 1px solid rgba(40, 27, 40, 150);\n"
"}\n"
"#btn_close:pressed {\n"
"background-color: rgb(93, 93, 93);\n"
"border: 1px solid #2e3043;\n"
"font: 500 9pt \"Be Vietnam Pro\";\n"
"text-align: left;\n"
"color: #A29F9F;\n"
"background-image: url(:/ic"
                        "ons/images/icons/x.png);\n"
"background-position: center center;\n"
"background-repeat: no-repeat;\n"
"border-radius: 5px;\n"
"}\n"
"")
        self.btn_close.setIconSize(QSize(21, 21))
        self.divider = QLabel(self.ctx_btns)
        self.divider.setObjectName(u"divider")
        self.divider.setGeometry(QRect(0, 30, 161, 1))
        self.divider.setStyleSheet(u"background-color: rgba(94, 94, 94, 250);")
        self.profilepic = QLabel(self.ctx_btns)
        self.profilepic.setObjectName(u"profilepic")
        self.profilepic.setGeometry(QRect(7, 50, 30, 30))
        self.profilepic.setStyleSheet(u"#profilepic {\n"
"	background-color: transparent;\n"
"	border-style: outset;\n"
"	border-width: 2px;\n"
"	border-radius: 15px;\n"
"	border-color: white;\n"
"	padding: 4px;\n"
"}")
        self.profilepic.setPixmap(QPixmap(u":/icons/images/icons/help.png"))
        self.profilepic.setScaledContents(True)
        self.username = QPushButton(self.ctx_btns)
        self.username.setObjectName(u"username")
        self.username.setGeometry(QRect(46, 53, 101, 21))
        self.username.setMinimumSize(QSize(10, 10))
        self.username.setFont(font)
        self.username.setCursor(QCursor(Qt.PointingHandCursor))
        self.username.setStyleSheet(u"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: left;\n"
"color: #fff;")
        self.currentlyloggedin = QLabel(self.ctx_btns)
        self.currentlyloggedin.setObjectName(u"currentlyloggedin")
        self.currentlyloggedin.setGeometry(QRect(10, 100, 141, 21))
        self.currentlyloggedin.setStyleSheet(u"border: none;\n"
"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: left;\n"
"color: #A29F9F;")
        self.currentlyloggedin.setAlignment(Qt.AlignCenter)
        self.ipaddress = QLabel(self.ctx_btns)
        self.ipaddress.setObjectName(u"ipaddress")
        self.ipaddress.setGeometry(QRect(10, 120, 141, 31))
        self.ipaddress.setStyleSheet(u"border: none;\n"
"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: left;\n"
"color: rgb(255, 255, 255)")
        self.ipaddress.setAlignment(Qt.AlignCenter)
        self.btn_website = QPushButton(self.ctx_btns)
        self.btn_website.setObjectName(u"btn_website")
        self.btn_website.setGeometry(QRect(34, 2, 31, 31))
        self.btn_website.setMinimumSize(QSize(10, 10))
        self.btn_website.setFont(font1)
        self.btn_website.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_website.setStyleSheet(u"#btn_website {\n"
"background-color: transparent;\n"
"font: 500 9pt \"Be Vietnam Pro\";\n"
"text-align: left;\n"
"color: #A29F9F;\n"
"background-image: url(:/icons/images/icons/globe.png);\n"
"background-position: center center;\n"
"background-repeat: no-repeat;\n"
"background-size: cover; \n"
"padding: 0;\n"
"margin: 0;\n"
"border-radius: 5px;\n"
"}\n"
"#btn_website:hover {\n"
"background-color: #2e3043;\n"
"border-color: rgb(238, 238, 238);\n"
"border: 2px solid;\n"
"font: 500 9pt \"Be Vietnam Pro\";\n"
"text-align: left;\n"
"color: #A29F9F;\n"
"background-image: url(:/icons/images/icons/globe.png);\n"
"background-position: center center;\n"
"background-repeat: no-repeat;\n"
"border-radius: 5px;\n"
"border: 1px solid rgba(40, 27, 40, 150);\n"
"}\n"
"#btn_website:pressed {\n"
"background-color: rgb(93, 93, 93);\n"
"border: 1px solid #2e3043;\n"
"font: 500 9pt \"Be Vietnam Pro\";\n"
"text-align: left;\n"
"color: #A29F9F;\n"
"background-image: url(:/icons/images/icons/globe.png);\n"
"background-position: center"
                        " center;\n"
"background-repeat: no-repeat;\n"
"border-radius: 5px;\n"
"}\n"
"")
        self.btn_website.setIconSize(QSize(21, 21))
        self.btn_minimize.raise_()
        self.btn_close.raise_()
        self.username.raise_()
        self.currentlyloggedin.raise_()
        self.ipaddress.raise_()
        self.btn_website.raise_()
        self.divider.raise_()
        self.profilepic.raise_()
        self.icon_4 = QLabel(self.bgApp)
        self.icon_4.setObjectName(u"icon_4")
        self.icon_4.setGeometry(QRect(40, 218, 20, 20))
        self.icon_4.setStyleSheet(u"")
        self.icon_4.setPixmap(QPixmap(u":/icons/images/icons/settings.png"))
        self.icon_4.setScaledContents(False)
        self.btn_settings = QPushButton(self.bgApp)
        self.btn_settings.setObjectName(u"btn_settings")
        self.btn_settings.setGeometry(QRect(89, 218, 131, 21))
        self.btn_settings.setMinimumSize(QSize(120, 15))
        self.btn_settings.setFont(font)
        self.btn_settings.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_settings.setStyleSheet(u"#btn_settings {\n"
"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: left;\n"
"color: #A29F9F;\n"
"border-radius: 5px;\n"
"}\n"
"#btn_settings:hover {\n"
"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: left;\n"
"color: #fff;\n"
"border-radius: 5px;\n"
"}\n"
"#btn_settings:pressed {\n"
"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: left;\n"
"color: #9e77ed;\n"
"border-radius: 5px;\n"
"}")
        self.sep4 = QLabel(self.bgApp)
        self.sep4.setObjectName(u"sep4")
        self.sep4.setGeometry(QRect(70, 224, 10, 10))
        self.sep4.setStyleSheet(u"")
        self.sep4.setPixmap(QPixmap(u":/icons/images/icons/separator_inactive.png"))
        self.sep4.setScaledContents(True)
        self.creditsLabel = QLabel(self.bgApp)
        self.creditsLabel.setObjectName(u"creditsLabel")
        self.creditsLabel.setGeometry(QRect(20, 680, 111, 16))
        self.creditsLabel.setMaximumSize(QSize(16777215, 16))
        self.creditsLabel.setFont(font)
        self.creditsLabel.setStyleSheet(u"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"color: rgba(162, 159, 159, 150);\n"
"text-align: left;")
        self.creditsLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.creditsLabel_2 = QLabel(self.bgApp)
        self.creditsLabel_2.setObjectName(u"creditsLabel_2")
        self.creditsLabel_2.setGeometry(QRect(40, 50, 41, 16))
        self.creditsLabel_2.setMaximumSize(QSize(16777215, 16))
        self.creditsLabel_2.setFont(font1)
        self.creditsLabel_2.setStyleSheet(u"background-color: transparent;\n"
"font: 500 9pt \"Be Vietnam Pro\";\n"
"color: rgba(162, 159, 159, 120);\n"
"text-align: left;")
        self.creditsLabel_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.btn_dropdown = QPushButton(self.bgApp)
        self.btn_dropdown.setObjectName(u"btn_dropdown")
        self.btn_dropdown.setGeometry(QRect(1209, 20, 31, 31))
        self.btn_dropdown.setMinimumSize(QSize(1, 1))
        font2 = QFont()
        font2.setFamilies([u"Inter Medium 400"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.btn_dropdown.setFont(font2)
        self.btn_dropdown.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_dropdown.setStyleSheet(u"")
        icon1 = QIcon()
        icon1.addFile(u":/icons/images/icons/arrow-down-left.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_dropdown.setIcon(icon1)
        self.btn_dropdown.setIconSize(QSize(21, 21))
        self.pages = QStackedWidget(self.bgApp)
        self.pages.setObjectName(u"pages")
        self.pages.setGeometry(QRect(320, 250, 931, 441))
        self.pages.setStyleSheet(u"background: transparent;")
        self.hsmlist = QWidget()
        self.hsmlist.setObjectName(u"hsmlist")
        self.hsmpages = QStackedWidget(self.hsmlist)
        self.hsmpages.setObjectName(u"hsmpages")
        self.hsmpages.setGeometry(QRect(0, 0, 931, 441))
        self.addfirst = QWidget()
        self.addfirst.setObjectName(u"addfirst")
        self.btn_addfirsthsm = QPushButton(self.addfirst)
        self.btn_addfirsthsm.setObjectName(u"btn_addfirsthsm")
        self.btn_addfirsthsm.setGeometry(QRect(370, 190, 181, 41))
        self.btn_addfirsthsm.setMinimumSize(QSize(120, 15))
        self.btn_addfirsthsm.setFont(font)
        self.btn_addfirsthsm.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_addfirsthsm.setStyleSheet(u"#btn_addfirsthsm {\n"
"background-color: rgba(222, 222, 222, 50);\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: center;\n"
"border: 1px solid rgba(255, 255, 255, 150);\n"
"border-radius: 5px;\n"
"}\n"
"#btn_addfirsthsm:hover {\n"
"background-color: rgba(222, 222, 222, 90);\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: center;\n"
"border: 1px solid rgba(255, 255, 255, 150);\n"
"border-radius: 5px;\n"
"}\n"
"#btn_addfirsthsm:pressed {\n"
"background-color: rgba(222, 222, 222, 150);\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: center;\n"
"border: 1px solid rgba(255, 255, 255, 150);\n"
"border-radius: 5px;\n"
"}")
        icon2 = QIcon()
        icon2.addFile(u":/icons/images/icons/cil-plus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_addfirsthsm.setIcon(icon2)
        self.hsmpages.addWidget(self.addfirst)
        self.hsmdetails = QWidget()
        self.hsmdetails.setObjectName(u"hsmdetails")
        self.hsm_name = QLineEdit(self.hsmdetails)
        self.hsm_name.setObjectName(u"hsm_name")
        self.hsm_name.setGeometry(QRect(330, 91, 271, 30))
        self.hsm_name.setMinimumSize(QSize(0, 30))
        self.hsm_name.setStyleSheet(u"background: solid rgb(16, 11, 16);\n"
"border: 2px solid rgb(157, 122, 222);\n"
"border-radius: 15px;\n"
"font: 600 10pt \"Inter Medium\";\n"
"color: white;")
        self.hsm_name.setMaxLength(15)
        self.hsmnamelabel = QLabel(self.hsmdetails)
        self.hsmnamelabel.setObjectName(u"hsmnamelabel")
        self.hsmnamelabel.setGeometry(QRect(340, 60, 261, 31))
        self.hsmnamelabel.setStyleSheet(u"font: 600 10pt \"Inter Medium\";")
        self.addhsmtitle = QLabel(self.hsmdetails)
        self.addhsmtitle.setObjectName(u"addhsmtitle")
        self.addhsmtitle.setGeometry(QRect(0, 0, 931, 51))
        self.addhsmtitle.setStyleSheet(u"font: 600 16pt \"Inter Medium\";")
        self.addhsmtitle.setAlignment(Qt.AlignCenter)
        self.hsmmasterpwlabel = QLabel(self.hsmdetails)
        self.hsmmasterpwlabel.setObjectName(u"hsmmasterpwlabel")
        self.hsmmasterpwlabel.setGeometry(QRect(340, 201, 141, 31))
        self.hsmmasterpwlabel.setStyleSheet(u"font: 600 10pt \"Inter Medium\";")
        self.hsm_masterpw = QLineEdit(self.hsmdetails)
        self.hsm_masterpw.setObjectName(u"hsm_masterpw")
        self.hsm_masterpw.setGeometry(QRect(330, 232, 271, 30))
        self.hsm_masterpw.setMinimumSize(QSize(0, 30))
        self.hsm_masterpw.setStyleSheet(u"background: solid rgb(16, 11, 16);\n"
"border: 2px solid rgb(157, 122, 222);\n"
"border-radius: 15px;\n"
"font: 600 10pt \"Inter Medium\";\n"
"color: white;")
        self.hsm_masterpw.setEchoMode(QLineEdit.Password)
        self.hsm_uuid = QLineEdit(self.hsmdetails)
        self.hsm_uuid.setObjectName(u"hsm_uuid")
        self.hsm_uuid.setGeometry(QRect(330, 303, 271, 30))
        self.hsm_uuid.setMinimumSize(QSize(0, 30))
        self.hsm_uuid.setStyleSheet(u"background: solid rgb(16, 11, 16);\n"
"border: 2px solid rgb(157, 122, 222);\n"
"border-radius: 15px;\n"
"font: 600 10pt \"Inter Medium\";\n"
"color: white;")
        self.hsm_uuid.setReadOnly(True)
        self.hsmuuidlabel = QLabel(self.hsmdetails)
        self.hsmuuidlabel.setObjectName(u"hsmuuidlabel")
        self.hsmuuidlabel.setGeometry(QRect(340, 272, 121, 31))
        self.hsmuuidlabel.setStyleSheet(u"font: 600 10pt \"Inter Medium\";")
        self.hsm_ip = QLineEdit(self.hsmdetails)
        self.hsm_ip.setObjectName(u"hsm_ip")
        self.hsm_ip.setGeometry(QRect(330, 161, 271, 30))
        self.hsm_ip.setMinimumSize(QSize(0, 30))
        self.hsm_ip.setStyleSheet(u"background: solid rgb(16, 11, 16);\n"
"border: 2px solid rgb(157, 122, 222);\n"
"border-radius: 15px;\n"
"font: 600 10pt \"Inter Medium\";\n"
"color: white;")
        self.hsm_ip.setMaxLength(15)
        self.hsmiplabel = QLabel(self.hsmdetails)
        self.hsmiplabel.setObjectName(u"hsmiplabel")
        self.hsmiplabel.setGeometry(QRect(340, 130, 111, 31))
        self.hsmiplabel.setStyleSheet(u"font: 600 10pt \"Inter Medium\";")
        self.add_button = QPushButton(self.hsmdetails)
        self.add_button.setObjectName(u"add_button")
        self.add_button.setGeometry(QRect(390, 360, 151, 30))
        self.add_button.setMinimumSize(QSize(150, 30))
        font3 = QFont()
        font3.setFamilies([u"Inter Medium"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.add_button.setFont(font3)
        self.add_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.add_button.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(40, 27, 40);\n"
"	border: 2px solid rgb(157, 122, 222);\n"
"	background: solid;\n"
"	border-radius: 5px;\n"
"	font: 10pt \"Inter Medium\";\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgba(40, 27, 40, 170);\n"
"	border: 2px solid rgb(157, 122, 222);\n"
"	border-radius: 5px;\n"
"	font: 10pt \"Inter Medium\";\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(255, 243, 239);\n"
"	font: 10pt \"Inter Medium\";\n"
"	icon: url(:/icons/images/icons/plus_purple.png);\n"
"	color: #9e77ed;\n"
"	border-radius: 5px;\n"
"}")
        icon3 = QIcon()
        icon3.addFile(u":/icons/images/icons/plus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.add_button.setIcon(icon3)
        self.responselabel = QLabel(self.hsmdetails)
        self.responselabel.setObjectName(u"responselabel")
        self.responselabel.setGeometry(QRect(290, 400, 351, 41))
        self.responselabel.setStyleSheet(u"color: rgb(113, 126, 149);")
        self.responselabel.setLineWidth(1)
        self.responselabel.setAlignment(Qt.AlignCenter)
        self.hsmpages.addWidget(self.hsmdetails)
        self.overview = QWidget()
        self.overview.setObjectName(u"overview")
        self.overview_icon = QLabel(self.overview)
        self.overview_icon.setObjectName(u"overview_icon")
        self.overview_icon.setGeometry(QRect(10, 10, 31, 31))
        self.overview_icon.setStyleSheet(u"")
        self.overview_icon.setPixmap(QPixmap(u":/icons/images/icons/server.png"))
        self.overview_icon.setScaledContents(False)
        self.overview_hsm_name = QLabel(self.overview)
        self.overview_hsm_name.setObjectName(u"overview_hsm_name")
        self.overview_hsm_name.setGeometry(QRect(45, 9, 171, 31))
        self.overview_hsm_name.setStyleSheet(u"font: 700 12pt \"Inter Medium\";")
        self.overview_auth_btn = QPushButton(self.overview)
        self.overview_auth_btn.setObjectName(u"overview_auth_btn")
        self.overview_auth_btn.setGeometry(QRect(10, 210, 160, 30))
        self.overview_auth_btn.setMinimumSize(QSize(150, 30))
        self.overview_auth_btn.setFont(font)
        self.overview_auth_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.overview_auth_btn.setStyleSheet(u"QPushButton {\n"
"background-color: #9e77ed;\n"
"font: 600 10pt \"Inter Medium\";\n"
"border-radius: 5px;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(168, 128, 255);\n"
"	border-radius: 4px;\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(255, 243, 239);\n"
"	font: 600 10pt \"Inter Medium\";\n"
"	icon: url(:/icons/images/icons/log-in_purple.png);\n"
"	color: #9e77ed;\n"
"	border-radius: 5px;\n"
"}\n"
"")
        icon4 = QIcon()
        icon4.addFile(u":/icons/images/icons/lock.png", QSize(), QIcon.Normal, QIcon.Off)
        self.overview_auth_btn.setIcon(icon4)
        self.overview_mp_label = QLabel(self.overview)
        self.overview_mp_label.setObjectName(u"overview_mp_label")
        self.overview_mp_label.setGeometry(QRect(10, 129, 151, 20))
        self.overview_mp_label.setStyleSheet(u"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: left;\n"
"color: #fff;\n"
"border-radius: 5px;")
        self.overview_mp_label.setLineWidth(1)
        self.overview_mp_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.overview_masterpw_field = QLineEdit(self.overview)
        self.overview_masterpw_field.setObjectName(u"overview_masterpw_field")
        self.overview_masterpw_field.setGeometry(QRect(10, 150, 161, 30))
        self.overview_masterpw_field.setMinimumSize(QSize(0, 30))
        self.overview_masterpw_field.setStyleSheet(u"background-color: rgb(33, 37, 43);\n"
"font: 600 10pt \"Inter Medium\";")
        self.overview_masterpw_field.setEchoMode(QLineEdit.Password)
        self.overview_auth_icon = QLabel(self.overview)
        self.overview_auth_icon.setObjectName(u"overview_auth_icon")
        self.overview_auth_icon.setGeometry(QRect(10, 80, 16, 16))
        self.overview_auth_icon.setStyleSheet(u"")
        self.overview_auth_icon.setPixmap(QPixmap(u":/icons/images/icons/unauthenticated.png"))
        self.overview_auth_icon.setScaledContents(False)
        self.overview_auth_label = QLabel(self.overview)
        self.overview_auth_label.setObjectName(u"overview_auth_label")
        self.overview_auth_label.setGeometry(QRect(37, 80, 121, 16))
        self.overview_auth_label.setStyleSheet(u"font: 700 10pt \"Inter Medium\";\n"
"color: #F04438;")
        self.auth_area_border = QLabel(self.overview)
        self.auth_area_border.setObjectName(u"auth_area_border")
        self.auth_area_border.setGeometry(QRect(0, 119, 181, 141))
        self.auth_area_border.setStyleSheet(u"border: 1px solid #F04438;\n"
"border-radius: 10px;")
        self.auth_area_border.setLineWidth(1)
        self.auth_area_border.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.overview_icon_3 = QLabel(self.overview)
        self.overview_icon_3.setObjectName(u"overview_icon_3")
        self.overview_icon_3.setGeometry(QRect(400, 10, 31, 31))
        self.overview_icon_3.setStyleSheet(u"")
        self.overview_icon_3.setPixmap(QPixmap(u":/icons/images/icons/cpu.png"))
        self.overview_icon_3.setScaledContents(False)
        self.overview_cpu = QLabel(self.overview)
        self.overview_cpu.setObjectName(u"overview_cpu")
        self.overview_cpu.setGeometry(QRect(435, 9, 41, 31))
        self.overview_cpu.setStyleSheet(u"font: 700 12pt \"Inter Medium\";")
        self.overview_mid = QLabel(self.overview)
        self.overview_mid.setObjectName(u"overview_mid")
        self.overview_mid.setGeometry(QRect(10, 50, 281, 16))
        self.overview_mid.setStyleSheet(u"font: 700 10pt \"Inter Medium\";\n"
"color: #fff")
        self.overview_icon_4 = QLabel(self.overview)
        self.overview_icon_4.setObjectName(u"overview_icon_4")
        self.overview_icon_4.setGeometry(QRect(130, 130, 16, 16))
        self.overview_icon_4.setStyleSheet(u"")
        self.overview_icon_4.setPixmap(QPixmap(u":/icons/images/icons/info.png"))
        self.overview_icon_4.setScaledContents(False)
        self.overview_responselabel = QLabel(self.overview)
        self.overview_responselabel.setObjectName(u"overview_responselabel")
        self.overview_responselabel.setGeometry(QRect(0, 400, 351, 41))
        self.overview_responselabel.setStyleSheet(u"color: rgb(113, 126, 149);")
        self.overview_responselabel.setLineWidth(1)
        self.overview_responselabel.setAlignment(Qt.AlignCenter)
        self.cpu_area_border = QLabel(self.overview)
        self.cpu_area_border.setObjectName(u"cpu_area_border")
        self.cpu_area_border.setGeometry(QRect(400, 50, 521, 61))
        self.cpu_area_border.setStyleSheet(u"border: 1px solid #9e77ed;\n"
"border-radius: 10px;")
        self.cpu_area_border.setLineWidth(1)
        self.cpu_area_border.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.verticalLayoutWidget = QWidget(self.overview)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(409, 60, 501, 41))
        self.cpu_layout = QVBoxLayout(self.verticalLayoutWidget)
        self.cpu_layout.setObjectName(u"cpu_layout")
        self.cpu_layout.setContentsMargins(0, 0, 0, 0)
        self.overview_cpu_current = QLabel(self.overview)
        self.overview_cpu_current.setObjectName(u"overview_cpu_current")
        self.overview_cpu_current.setGeometry(QRect(870, 10, 41, 31))
        self.overview_cpu_current.setStyleSheet(u"font: 700 12pt \"Inter Medium\";\n"
"color: #9e77ed;")
        self.overview_cpu_2 = QLabel(self.overview)
        self.overview_cpu_2.setObjectName(u"overview_cpu_2")
        self.overview_cpu_2.setGeometry(QRect(790, 10, 71, 31))
        self.overview_cpu_2.setStyleSheet(u"font: 700 12pt \"Inter Medium\";")
        self.overview_cpu_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.overview_gpu = QLabel(self.overview)
        self.overview_gpu.setObjectName(u"overview_gpu")
        self.overview_gpu.setGeometry(QRect(436, 119, 41, 31))
        self.overview_gpu.setStyleSheet(u"font: 700 12pt \"Inter Medium\";")
        self.gpu_area_border = QLabel(self.overview)
        self.gpu_area_border.setObjectName(u"gpu_area_border")
        self.gpu_area_border.setGeometry(QRect(401, 160, 521, 61))
        self.gpu_area_border.setStyleSheet(u"border: 1px solid #9e77ed;\n"
"border-radius: 10px;")
        self.gpu_area_border.setLineWidth(1)
        self.gpu_area_border.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.verticalLayoutWidget_2 = QWidget(self.overview)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(410, 170, 501, 41))
        self.gpu_layout = QVBoxLayout(self.verticalLayoutWidget_2)
        self.gpu_layout.setObjectName(u"gpu_layout")
        self.gpu_layout.setContentsMargins(0, 0, 0, 0)
        self.overview_icon_5 = QLabel(self.overview)
        self.overview_icon_5.setObjectName(u"overview_icon_5")
        self.overview_icon_5.setGeometry(QRect(401, 120, 31, 31))
        self.overview_icon_5.setStyleSheet(u"")
        self.overview_icon_5.setPixmap(QPixmap(u":/icons/images/icons/gpu.png"))
        self.overview_icon_5.setScaledContents(False)
        self.overview_cpu_4 = QLabel(self.overview)
        self.overview_cpu_4.setObjectName(u"overview_cpu_4")
        self.overview_cpu_4.setGeometry(QRect(791, 120, 71, 31))
        self.overview_cpu_4.setStyleSheet(u"font: 700 12pt \"Inter Medium\";")
        self.overview_cpu_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.overview_gpu_current = QLabel(self.overview)
        self.overview_gpu_current.setObjectName(u"overview_gpu_current")
        self.overview_gpu_current.setGeometry(QRect(871, 120, 41, 31))
        self.overview_gpu_current.setStyleSheet(u"font: 700 12pt \"Inter Medium\";\n"
"color: #9e77ed;")
        self.overview_icon_6 = QLabel(self.overview)
        self.overview_icon_6.setObjectName(u"overview_icon_6")
        self.overview_icon_6.setGeometry(QRect(400, 230, 31, 31))
        self.overview_icon_6.setStyleSheet(u"")
        self.overview_icon_6.setPixmap(QPixmap(u":/icons/images/icons/ram.png"))
        self.overview_icon_6.setScaledContents(False)
        self.overview_ram = QLabel(self.overview)
        self.overview_ram.setObjectName(u"overview_ram")
        self.overview_ram.setGeometry(QRect(435, 229, 41, 31))
        self.overview_ram.setStyleSheet(u"font: 700 12pt \"Inter Medium\";")
        self.overview_ram_2 = QLabel(self.overview)
        self.overview_ram_2.setObjectName(u"overview_ram_2")
        self.overview_ram_2.setGeometry(QRect(790, 230, 71, 31))
        self.overview_ram_2.setStyleSheet(u"font: 700 12pt \"Inter Medium\";")
        self.overview_ram_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.verticalLayoutWidget_3 = QWidget(self.overview)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(410, 280, 501, 41))
        self.ram_layout = QVBoxLayout(self.verticalLayoutWidget_3)
        self.ram_layout.setObjectName(u"ram_layout")
        self.ram_layout.setContentsMargins(0, 0, 0, 0)
        self.overview_ram_current = QLabel(self.overview)
        self.overview_ram_current.setObjectName(u"overview_ram_current")
        self.overview_ram_current.setGeometry(QRect(870, 230, 41, 31))
        self.overview_ram_current.setStyleSheet(u"font: 700 12pt \"Inter Medium\";\n"
"color: #9e77ed;")
        self.ram_area_border = QLabel(self.overview)
        self.ram_area_border.setObjectName(u"ram_area_border")
        self.ram_area_border.setGeometry(QRect(400, 270, 521, 61))
        self.ram_area_border.setStyleSheet(u"border: 1px solid #9e77ed;\n"
"border-radius: 10px;")
        self.ram_area_border.setLineWidth(1)
        self.ram_area_border.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.disk_progress_bar = QProgressBar(self.overview)
        self.disk_progress_bar.setObjectName(u"disk_progress_bar")
        self.disk_progress_bar.setGeometry(QRect(400, 380, 521, 23))
        self.disk_progress_bar.setStyleSheet(u"QProgressBar {\n"
"background-color: rgb(40, 27, 40);\n"
"border: 2px solid rgb(157, 122, 222);\n"
"color: #fff;\n"
"border-radius: 10px;\n"
"text-align: center;\n"
"font: 57 10pt \"Inter Medium\";\n"
"}\n"
"QProgressBar::chunk{\n"
"border-radius: 10px;\n"
"background-color: qlineargradient(spread:pad, x1:0.931, y1:1, x2:1, y2:1, stop:0.704545 rgba(158, 119, 237, 255), stop:1 rgba(40, 27, 40, 255))\n"
"}")
        self.disk_progress_bar.setValue(0)
        self.overview_icon_7 = QLabel(self.overview)
        self.overview_icon_7.setObjectName(u"overview_icon_7")
        self.overview_icon_7.setGeometry(QRect(400, 340, 31, 31))
        self.overview_icon_7.setStyleSheet(u"")
        self.overview_icon_7.setPixmap(QPixmap(u":/icons/images/icons/hard-drive.png"))
        self.overview_icon_7.setScaledContents(False)
        self.overview_disk_current = QLabel(self.overview)
        self.overview_disk_current.setObjectName(u"overview_disk_current")
        self.overview_disk_current.setGeometry(QRect(870, 340, 41, 31))
        self.overview_disk_current.setStyleSheet(u"font: 700 12pt \"Inter Medium\";\n"
"color: #9e77ed;")
        self.overview_ram_3 = QLabel(self.overview)
        self.overview_ram_3.setObjectName(u"overview_ram_3")
        self.overview_ram_3.setGeometry(QRect(790, 340, 71, 31))
        self.overview_ram_3.setStyleSheet(u"font: 700 12pt \"Inter Medium\";")
        self.overview_ram_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.overview_ram_4 = QLabel(self.overview)
        self.overview_ram_4.setObjectName(u"overview_ram_4")
        self.overview_ram_4.setGeometry(QRect(435, 339, 41, 31))
        self.overview_ram_4.setStyleSheet(u"font: 700 12pt \"Inter Medium\";")
        self.last_update_label = QLabel(self.overview)
        self.last_update_label.setObjectName(u"last_update_label")
        self.last_update_label.setGeometry(QRect(510, 409, 411, 31))
        self.last_update_label.setStyleSheet(u"font: 700 11pt \"Inter Medium\";\n"
"color: #9e77ed;")
        self.last_update_label_2 = QLabel(self.overview)
        self.last_update_label_2.setObjectName(u"last_update_label_2")
        self.last_update_label_2.setGeometry(QRect(400, 409, 91, 31))
        self.last_update_label_2.setStyleSheet(u"font: 700 11pt \"Inter Medium\";\n"
"color: #fff;")
        self.hsmpages.addWidget(self.overview)
        self.auth_area_border.raise_()
        self.overview_icon.raise_()
        self.overview_hsm_name.raise_()
        self.overview_auth_btn.raise_()
        self.overview_mp_label.raise_()
        self.overview_masterpw_field.raise_()
        self.overview_auth_icon.raise_()
        self.overview_auth_label.raise_()
        self.overview_icon_3.raise_()
        self.overview_cpu.raise_()
        self.overview_mid.raise_()
        self.overview_icon_4.raise_()
        self.overview_responselabel.raise_()
        self.cpu_area_border.raise_()
        self.verticalLayoutWidget.raise_()
        self.overview_cpu_current.raise_()
        self.overview_cpu_2.raise_()
        self.overview_gpu.raise_()
        self.gpu_area_border.raise_()
        self.verticalLayoutWidget_2.raise_()
        self.overview_icon_5.raise_()
        self.overview_cpu_4.raise_()
        self.overview_gpu_current.raise_()
        self.overview_icon_6.raise_()
        self.overview_ram.raise_()
        self.overview_ram_2.raise_()
        self.verticalLayoutWidget_3.raise_()
        self.overview_ram_current.raise_()
        self.ram_area_border.raise_()
        self.disk_progress_bar.raise_()
        self.overview_icon_7.raise_()
        self.overview_disk_current.raise_()
        self.overview_ram_3.raise_()
        self.overview_ram_4.raise_()
        self.last_update_label.raise_()
        self.last_update_label_2.raise_()
        self.pages.addWidget(self.hsmlist)
        self.configurator = QWidget()
        self.configurator.setObjectName(u"configurator")
        self.pages.addWidget(self.configurator)
        self.controlpanel = QWidget()
        self.controlpanel.setObjectName(u"controlpanel")
        self.pages.addWidget(self.controlpanel)
        self.dragBar = QFrame(self.bgApp)
        self.dragBar.setObjectName(u"dragBar")
        self.dragBar.setGeometry(QRect(0, 0, 1261, 51))
        self.dragBar.setStyleSheet(u"border: none;\n"
"background: transparent;")
        self.dragBar.setFrameShape(QFrame.StyledPanel)
        self.dragBar.setFrameShadow(QFrame.Raised)
        self.logo = QLabel(self.dragBar)
        self.logo.setObjectName(u"logo")
        self.logo.setGeometry(QRect(0, -20, 171, 101))
        self.logo.setPixmap(QPixmap(u":/images/images/Polaris.png"))
        self.logo.setScaledContents(True)
        self.btn_hsmlist = QPushButton(self.bgApp)
        self.btn_hsmlist.setObjectName(u"btn_hsmlist")
        self.btn_hsmlist.setGeometry(QRect(360, 140, 120, 51))
        self.btn_hsmlist.setMinimumSize(QSize(120, 15))
        self.btn_hsmlist.setFont(font)
        self.btn_hsmlist.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_hsmlist.setStyleSheet(u"#btn_hsmlist {\n"
"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: center;\n"
"color: #fff;\n"
"border: solid;\n"
"border-bottom: 2px solid #9e77ed;\n"
"}\n"
"#btn_hsmlist:hover {\n"
"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: center;\n"
"color: #fff;\n"
"border: solid;\n"
"border-bottom: 2px solid #9e77ed;\n"
"}\n"
"#btn_hsmlist:pressed {\n"
"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: center;\n"
"color: #9e77ed;\n"
"border: solid;\n"
"border-bottom: 2px solid #9e77ed;\n"
"}")
        self.hsmlist_bg = QLabel(self.bgApp)
        self.hsmlist_bg.setObjectName(u"hsmlist_bg")
        self.hsmlist_bg.setGeometry(QRect(360, 171, 121, 20))
        self.hsmlist_bg.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0.494, y1:0, x2:0.494, y2:1, stop:0 rgba(0, 9, 31, 100), stop:1 rgba(157, 122, 222, 80));")
        self.btn_controlpanel = QPushButton(self.bgApp)
        self.btn_controlpanel.setObjectName(u"btn_controlpanel")
        self.btn_controlpanel.setGeometry(QRect(540, 139, 120, 51))
        self.btn_controlpanel.setMinimumSize(QSize(120, 15))
        self.btn_controlpanel.setFont(font)
        self.btn_controlpanel.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_controlpanel.setStyleSheet(u"#btn_controlpanel {\n"
"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: center;\n"
"color: #fff;\n"
"border: solid;\n"
"border-bottom: 2px solid #9e77ed;\n"
"}\n"
"#btn_controlpanel:hover {\n"
"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: center;\n"
"color: #fff;\n"
"border: solid;\n"
"border-bottom: 2px solid #9e77ed;\n"
"}\n"
"#btn_controlpanel:pressed {\n"
"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: center;\n"
"color: #9e77ed;\n"
"border: solid;\n"
"border-bottom: 2px solid #9e77ed;\n"
"}")
        self.controlpanel_bg = QLabel(self.bgApp)
        self.controlpanel_bg.setObjectName(u"controlpanel_bg")
        self.controlpanel_bg.setGeometry(QRect(540, 170, 121, 20))
        self.controlpanel_bg.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0.494, y1:0, x2:0.494, y2:1, stop:0 rgba(0, 9, 31, 100), stop:1 rgba(157, 122, 222, 80));")
        self.btn_configurator = QPushButton(self.bgApp)
        self.btn_configurator.setObjectName(u"btn_configurator")
        self.btn_configurator.setGeometry(QRect(720, 139, 120, 51))
        self.btn_configurator.setMinimumSize(QSize(120, 15))
        self.btn_configurator.setFont(font)
        self.btn_configurator.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_configurator.setStyleSheet(u"#btn_configurator {\n"
"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: center;\n"
"color: #fff;\n"
"border: solid;\n"
"border-bottom: 2px solid #9e77ed;\n"
"}\n"
"#btn_configurator:hover {\n"
"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: center;\n"
"color: #fff;\n"
"border: solid;\n"
"border-bottom: 2px solid #9e77ed;\n"
"}\n"
"#btn_configurator:pressed {\n"
"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: center;\n"
"color: #9e77ed;\n"
"border: solid;\n"
"border-bottom: 2px solid #9e77ed;\n"
"}")
        self.configurator_bg = QLabel(self.bgApp)
        self.configurator_bg.setObjectName(u"configurator_bg")
        self.configurator_bg.setGeometry(QRect(720, 170, 121, 20))
        self.configurator_bg.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0.494, y1:0, x2:0.494, y2:1, stop:0 rgba(0, 9, 31, 100), stop:1 rgba(157, 122, 222, 80));")
        self.controlpanel_bg.raise_()
        self.configurator_bg.raise_()
        self.hsmlist_bg.raise_()
        self.bg1.raise_()
        self.bg2.raise_()
        self.bg3.raise_()
        self.btn_dashboard.raise_()
        self.icon_1.raise_()
        self.sep1.raise_()
        self.btn_documentation.raise_()
        self.icon_2.raise_()
        self.sep2.raise_()
        self.sep3.raise_()
        self.icon_3.raise_()
        self.btn_account.raise_()
        self.icon_4.raise_()
        self.btn_settings.raise_()
        self.sep4.raise_()
        self.creditsLabel.raise_()
        self.creditsLabel_2.raise_()
        self.pages.raise_()
        self.dragBar.raise_()
        self.btn_hsmlist.raise_()
        self.btn_controlpanel.raise_()
        self.btn_configurator.raise_()
        self.ctx_btns.raise_()
        self.btn_dropdown.raise_()

        self.verticalLayout_2.addWidget(self.bgApp)

        MainWindow.setCentralWidget(self.styleSheet)

        self.retranslateUi(MainWindow)

        self.btn_minimize.setDefault(False)
        self.btn_website.setDefault(False)
        self.pages.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Polaris", None))
        self.bg1.setText("")
        self.bg2.setText("")
        self.bg3.setText("")
        self.btn_dashboard.setText(QCoreApplication.translate("MainWindow", u"  Dashboard", None))
        self.icon_1.setText("")
        self.sep1.setText("")
        self.btn_documentation.setText(QCoreApplication.translate("MainWindow", u"  Documentation", None))
        self.icon_2.setText("")
        self.sep2.setText("")
        self.sep3.setText("")
        self.icon_3.setText("")
        self.btn_account.setText(QCoreApplication.translate("MainWindow", u"  Account", None))
        self.btn_minimize.setText("")
        self.btn_close.setText("")
        self.divider.setText("")
        self.profilepic.setText("")
#if QT_CONFIG(tooltip)
        self.username.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Go to web dashboard</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.username.setText(QCoreApplication.translate("MainWindow", u"Username", None))
        self.currentlyloggedin.setText(QCoreApplication.translate("MainWindow", u"Currently Logged In At", None))
        self.ipaddress.setText(QCoreApplication.translate("MainWindow", u"8.8.8.8", None))
#if QT_CONFIG(tooltip)
        self.btn_website.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Log out</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.btn_website.setText("")
        self.icon_4.setText("")
        self.btn_settings.setText(QCoreApplication.translate("MainWindow", u"  Settings", None))
        self.sep4.setText("")
        self.creditsLabel.setText(QCoreApplication.translate("MainWindow", u"Milestone 5 Build", None))
        self.creditsLabel_2.setText(QCoreApplication.translate("MainWindow", u"0.5.0", None))
        self.btn_dropdown.setText("")
        self.btn_addfirsthsm.setText(QCoreApplication.translate("MainWindow", u"Add your first HSM", None))
        self.hsm_name.setText("")
        self.hsm_name.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Give your HSM a label...", None))
        self.hsmnamelabel.setText(QCoreApplication.translate("MainWindow", u"HSM Name", None))
        self.addhsmtitle.setText(QCoreApplication.translate("MainWindow", u"Add your HSM", None))
        self.hsmmasterpwlabel.setText(QCoreApplication.translate("MainWindow", u"HSM Master Password", None))
        self.hsm_masterpw.setText("")
        self.hsm_masterpw.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Create the HSM's master password...", None))
        self.hsm_uuid.setText("")
        self.hsm_uuid.setPlaceholderText("")
        self.hsmuuidlabel.setText(QCoreApplication.translate("MainWindow", u"Machine Identifier", None))
        self.hsm_ip.setText("")
        self.hsm_ip.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter the HSM's IP address...", None))
        self.hsmiplabel.setText(QCoreApplication.translate("MainWindow", u"HSM IP Address", None))
        self.add_button.setText(QCoreApplication.translate("MainWindow", u" Add", None))
        self.responselabel.setText("")
        self.overview_icon.setText("")
        self.overview_hsm_name.setText(QCoreApplication.translate("MainWindow", u"[Placeholder]", None))
        self.overview_auth_btn.setText(QCoreApplication.translate("MainWindow", u" Set", None))
        self.overview_mp_label.setText(QCoreApplication.translate("MainWindow", u"Master Password", None))
        self.overview_masterpw_field.setInputMask("")
        self.overview_masterpw_field.setText("")
        self.overview_masterpw_field.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter your MP here...", None))
        self.overview_auth_icon.setText("")
        self.overview_auth_label.setText(QCoreApplication.translate("MainWindow", u"Offline", None))
        self.auth_area_border.setText("")
        self.overview_icon_3.setText("")
        self.overview_cpu.setText(QCoreApplication.translate("MainWindow", u"CPU", None))
        self.overview_mid.setText(QCoreApplication.translate("MainWindow", u"5d4e36bd-025e-4872-a09d-2ec3b1f31497", None))
#if QT_CONFIG(tooltip)
        self.overview_icon_4.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Upon logging in, you need to set the master password for this machine to authenticate yourself to the HSM.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.overview_icon_4.setText("")
        self.overview_responselabel.setText("")
        self.cpu_area_border.setText("")
        self.overview_cpu_current.setText("")
        self.overview_cpu_2.setText(QCoreApplication.translate("MainWindow", u"Current:", None))
        self.overview_gpu.setText(QCoreApplication.translate("MainWindow", u"GPU", None))
        self.gpu_area_border.setText("")
        self.overview_icon_5.setText("")
        self.overview_cpu_4.setText(QCoreApplication.translate("MainWindow", u"Current:", None))
        self.overview_gpu_current.setText("")
        self.overview_icon_6.setText("")
        self.overview_ram.setText(QCoreApplication.translate("MainWindow", u"RAM", None))
        self.overview_ram_2.setText(QCoreApplication.translate("MainWindow", u"Current:", None))
        self.overview_ram_current.setText("")
        self.ram_area_border.setText("")
        self.overview_icon_7.setText("")
        self.overview_disk_current.setText("")
        self.overview_ram_3.setText(QCoreApplication.translate("MainWindow", u"Current:", None))
        self.overview_ram_4.setText(QCoreApplication.translate("MainWindow", u"Disk", None))
        self.last_update_label.setText(QCoreApplication.translate("MainWindow", u"[Placeholder]", None))
        self.last_update_label_2.setText(QCoreApplication.translate("MainWindow", u"Last update:", None))
        self.logo.setText("")
        self.btn_hsmlist.setText(QCoreApplication.translate("MainWindow", u"Overview", None))
        self.hsmlist_bg.setText("")
        self.btn_controlpanel.setText(QCoreApplication.translate("MainWindow", u"Control Panel", None))
        self.controlpanel_bg.setText("")
        self.btn_configurator.setText(QCoreApplication.translate("MainWindow", u"Configurator", None))
        self.configurator_bg.setText("")
    # retranslateUi

