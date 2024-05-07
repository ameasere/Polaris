# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
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
    QMainWindow, QPushButton, QSizePolicy, QStackedWidget,
    QVBoxLayout, QWidget)
from .resources_rc import *

class Ui_LoginWindow(object):
    def setupUi(self, LoginWindow):
        if not LoginWindow.objectName():
            LoginWindow.setObjectName(u"LoginWindow")
        LoginWindow.resize(370, 519)
        icon = QIcon()
        icon.addFile(u":/images/images/images/icon.png", QSize(), QIcon.Normal, QIcon.Off)
        LoginWindow.setWindowIcon(icon)
        self.styleSheet = QWidget(LoginWindow)
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
        self.bg1.setGeometry(QRect(0, 0, 31, 501))
        self.bg1.setStyleSheet(u"border-top-left-radius: 20px;\n"
"border-bottom-left-radius: 20px;\n"
"background-color: rgba(40, 27, 40, 150);\n"
"border: 1px solid rgba(128, 96, 167, 80);")
        self.logo = QLabel(self.bgApp)
        self.logo.setObjectName(u"logo")
        self.logo.setGeometry(QRect(0, -20, 171, 101))
        self.logo.setPixmap(QPixmap(u":/images/images/Polaris.png"))
        self.logo.setScaledContents(True)
        self.creditsLabel = QLabel(self.bgApp)
        self.creditsLabel.setObjectName(u"creditsLabel")
        self.creditsLabel.setGeometry(QRect(20, 680, 111, 16))
        self.creditsLabel.setMaximumSize(QSize(16777215, 16))
        font = QFont()
        font.setFamilies([u"Inter Medium"])
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
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
        font1 = QFont()
        font1.setFamilies([u"Be Vietnam Pro"])
        font1.setPointSize(9)
        font1.setBold(False)
        font1.setItalic(False)
        self.creditsLabel_2.setFont(font1)
        self.creditsLabel_2.setStyleSheet(u"background-color: transparent;\n"
"font: 500 9pt \"Be Vietnam Pro\";\n"
"color: rgba(162, 159, 159, 120);\n"
"text-align: left;")
        self.creditsLabel_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.btn_dropdown = QPushButton(self.bgApp)
        self.btn_dropdown.setObjectName(u"btn_dropdown")
        self.btn_dropdown.setGeometry(QRect(310, 10, 31, 31))
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
        self.pages.setGeometry(QRect(65, 70, 221, 381))
        self.pages.setStyleSheet(u"background: transparent;")
        self.password_login = QWidget()
        self.password_login.setObjectName(u"password_login")
        self.login_button = QPushButton(self.password_login)
        self.login_button.setObjectName(u"login_button")
        self.login_button.setGeometry(QRect(31, 260, 160, 30))
        self.login_button.setMinimumSize(QSize(150, 30))
        font3 = QFont()
        font3.setFamilies([u"Inter Medium"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.login_button.setFont(font3)
        self.login_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.login_button.setStyleSheet(u"QPushButton {\n"
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
"	icon: url(:/icons/images/icons/log-in_purple.png);\n"
"	color: #9e77ed;\n"
"	border-radius: 5px;\n"
"}")
        icon2 = QIcon()
        icon2.addFile(u":/icons/images/icons/login.png", QSize(), QIcon.Normal, QIcon.Off)
        self.login_button.setIcon(icon2)
        self.password = QLineEdit(self.password_login)
        self.password.setObjectName(u"password")
        self.password.setGeometry(QRect(30, 181, 161, 30))
        self.password.setMinimumSize(QSize(0, 30))
        self.password.setStyleSheet(u"background-color: rgb(33, 37, 43);\n"
"font: 600 10pt \"Inter Medium\";")
        self.password.setEchoMode(QLineEdit.Password)
        self.passwordLabel = QLabel(self.password_login)
        self.passwordLabel.setObjectName(u"passwordLabel")
        self.passwordLabel.setGeometry(QRect(30, 160, 151, 20))
        self.passwordLabel.setStyleSheet(u"color: #fff;\n"
"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: left;\n"
"color: #fff;\n"
"border-radius: 5px;")
        self.passwordLabel.setLineWidth(1)
        self.passwordLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.register_button = QPushButton(self.password_login)
        self.register_button.setObjectName(u"register_button")
        self.register_button.setGeometry(QRect(30, 300, 160, 30))
        self.register_button.setMinimumSize(QSize(150, 30))
        self.register_button.setFont(font3)
        self.register_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.register_button.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(44, 49, 58);\n"
"	font: 10pt \"Inter Medium\";\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgba(222, 222, 222, 150);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: #47505e;\n"
"	border-radius: 4px;\n"
"	border: 2px solid rgba(222, 222, 222, 150);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(255, 243, 239);\n"
"	font: 10pt \"Inter Medium\";\n"
"	icon: url(:/icons/images/icons/register_purple.png);\n"
"	color: #9e77ed;\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgba(222, 222, 222, 150);\n"
"}")
        icon3 = QIcon()
        icon3.addFile(u":/icons/images/icons/register.png", QSize(), QIcon.Normal, QIcon.Off)
        self.register_button.setIcon(icon3)
        self.icon_2 = QLabel(self.password_login)
        self.icon_2.setObjectName(u"icon_2")
        self.icon_2.setGeometry(QRect(40, 12, 20, 20))
        self.icon_2.setStyleSheet(u"")
        self.icon_2.setPixmap(QPixmap(u":/icons/images/icons/italic_purple.png"))
        self.icon_2.setScaledContents(False)
        self.btn_dashboard_2 = QPushButton(self.password_login)
        self.btn_dashboard_2.setObjectName(u"btn_dashboard_2")
        self.btn_dashboard_2.setGeometry(QRect(60, 10, 120, 21))
        self.btn_dashboard_2.setMinimumSize(QSize(120, 15))
        self.btn_dashboard_2.setFont(font)
        self.btn_dashboard_2.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_dashboard_2.setStyleSheet(u"#btn_dashboard_2 {\n"
"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: left;\n"
"color: #fff;\n"
"border-radius: 5px;\n"
"}\n"
"#btn_dashboard_2:hover {\n"
"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: left;\n"
"color: #fff;\n"
"border-radius: 5px;\n"
"}\n"
"#btn_dashboard_2:pressed {\n"
"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: left;\n"
"color: #9e77ed;\n"
"border-radius: 5px;\n"
"}")
        self.username = QLineEdit(self.password_login)
        self.username.setObjectName(u"username")
        self.username.setGeometry(QRect(30, 110, 161, 30))
        self.username.setMinimumSize(QSize(0, 30))
        self.username.setStyleSheet(u"background-color: rgb(33, 37, 43);\n"
"font: 600 10pt \"Inter Medium\";")
        self.usernameLabel = QLabel(self.password_login)
        self.usernameLabel.setObjectName(u"usernameLabel")
        self.usernameLabel.setGeometry(QRect(30, 90, 151, 20))
        self.usernameLabel.setStyleSheet(u"color: #fff;\n"
"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: left;\n"
"color: #fff;\n"
"border-radius: 5px;")
        self.usernameLabel.setLineWidth(1)
        self.usernameLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.pages.addWidget(self.password_login)
        self.token_login = QWidget()
        self.token_login.setObjectName(u"token_login")
        self.passwordLabel_3 = QLabel(self.token_login)
        self.passwordLabel_3.setObjectName(u"passwordLabel_3")
        self.passwordLabel_3.setGeometry(QRect(30, 100, 151, 20))
        self.passwordLabel_3.setStyleSheet(u"color: #fff;\n"
"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: left;\n"
"color: #fff;\n"
"border-radius: 5px;")
        self.passwordLabel_3.setLineWidth(1)
        self.passwordLabel_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.password_token = QLineEdit(self.token_login)
        self.password_token.setObjectName(u"password_token")
        self.password_token.setGeometry(QRect(30, 121, 161, 30))
        self.password_token.setMinimumSize(QSize(0, 30))
        self.password_token.setStyleSheet(u"background-color: rgb(33, 37, 43);\n"
"font: 600 10pt \"Inter Medium\";")
        self.password_token.setEchoMode(QLineEdit.Password)
        self.btn_dashboard_3 = QPushButton(self.token_login)
        self.btn_dashboard_3.setObjectName(u"btn_dashboard_3")
        self.btn_dashboard_3.setGeometry(QRect(60, 10, 120, 21))
        self.btn_dashboard_3.setMinimumSize(QSize(120, 15))
        self.btn_dashboard_3.setFont(font)
        self.btn_dashboard_3.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_dashboard_3.setStyleSheet(u"#btn_dashboard_3 {\n"
"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: left;\n"
"color: #fff;\n"
"border-radius: 5px;\n"
"}\n"
"#btn_dashboard_3:hover {\n"
"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: left;\n"
"color: #fff;\n"
"border-radius: 5px;\n"
"}\n"
"#btn_dashboard_3:pressed {\n"
"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: left;\n"
"color: #9e77ed;\n"
"border-radius: 5px;\n"
"}")
        self.loginTokenButton = QPushButton(self.token_login)
        self.loginTokenButton.setObjectName(u"loginTokenButton")
        self.loginTokenButton.setGeometry(QRect(31, 260, 160, 30))
        self.loginTokenButton.setMinimumSize(QSize(150, 30))
        self.loginTokenButton.setFont(font3)
        self.loginTokenButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.loginTokenButton.setStyleSheet(u"QPushButton {\n"
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
"	icon: url(:/icons/images/icons/log-in_purple.png);\n"
"	color: #9e77ed;\n"
"	border-radius: 5px;\n"
"}")
        self.loginTokenButton.setIcon(icon2)
        self.loginNormalButton = QPushButton(self.token_login)
        self.loginNormalButton.setObjectName(u"loginNormalButton")
        self.loginNormalButton.setGeometry(QRect(29, 300, 161, 30))
        self.loginNormalButton.setMinimumSize(QSize(150, 30))
        self.loginNormalButton.setFont(font3)
        self.loginNormalButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.loginNormalButton.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(44, 49, 58);\n"
"	font: 10pt \"Inter Medium\";\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgba(222, 222, 222, 150);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: #47505e;\n"
"	border-radius: 4px;\n"
"	border: 2px solid rgba(222, 222, 222, 150);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(255, 243, 239);\n"
"	font: 10pt \"Inter Medium\";\n"
"	icon: url(:/icons/images/icons/italic_purple.png);\n"
"	color: #9e77ed;\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgba(222, 222, 222, 150);\n"
"}")
        icon4 = QIcon()
        icon4.addFile(u":/icons/images/icons/italic.png", QSize(), QIcon.Normal, QIcon.Off)
        self.loginNormalButton.setIcon(icon4)
        self.icon_3 = QLabel(self.token_login)
        self.icon_3.setObjectName(u"icon_3")
        self.icon_3.setGeometry(QRect(40, 11, 20, 20))
        self.icon_3.setStyleSheet(u"")
        self.icon_3.setPixmap(QPixmap(u":/icons/images/icons/key.png"))
        self.icon_3.setScaledContents(False)
        self.pages.addWidget(self.token_login)
        self.twofactor = QWidget()
        self.twofactor.setObjectName(u"twofactor")
        self.passwordLabel_2 = QLabel(self.twofactor)
        self.passwordLabel_2.setObjectName(u"passwordLabel_2")
        self.passwordLabel_2.setGeometry(QRect(30, 100, 151, 20))
        self.passwordLabel_2.setStyleSheet(u"background-color: transparent;\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: left;\n"
"color: #fff;\n"
"border-radius: 5px;")
        self.passwordLabel_2.setLineWidth(1)
        self.passwordLabel_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.twofactor_field = QLineEdit(self.twofactor)
        self.twofactor_field.setObjectName(u"twofactor_field")
        self.twofactor_field.setGeometry(QRect(30, 121, 161, 30))
        self.twofactor_field.setMinimumSize(QSize(0, 30))
        self.twofactor_field.setStyleSheet(u"background-color: rgb(33, 37, 43);\n"
"font: 600 10pt \"Inter Medium\";")
        self.twofactor_field.setEchoMode(QLineEdit.Normal)
        self.twofactor_button = QPushButton(self.twofactor)
        self.twofactor_button.setObjectName(u"twofactor_button")
        self.twofactor_button.setGeometry(QRect(30, 260, 160, 30))
        self.twofactor_button.setMinimumSize(QSize(150, 30))
        self.twofactor_button.setFont(font)
        self.twofactor_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.twofactor_button.setStyleSheet(u"QPushButton {\n"
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
        self.twofactor_button.setIcon(icon2)
        self.btn_dashboard = QPushButton(self.twofactor)
        self.btn_dashboard.setObjectName(u"btn_dashboard")
        self.btn_dashboard.setGeometry(QRect(60, 10, 120, 21))
        self.btn_dashboard.setMinimumSize(QSize(120, 15))
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
        self.icon_1 = QLabel(self.twofactor)
        self.icon_1.setObjectName(u"icon_1")
        self.icon_1.setGeometry(QRect(40, 11, 20, 20))
        self.icon_1.setStyleSheet(u"")
        self.icon_1.setPixmap(QPixmap(u":/icons/images/icons/message-square.png"))
        self.icon_1.setScaledContents(False)
        self.pages.addWidget(self.twofactor)
        self.dragBar = QFrame(self.bgApp)
        self.dragBar.setObjectName(u"dragBar")
        self.dragBar.setGeometry(QRect(4, 0, 350, 51))
        self.dragBar.setStyleSheet(u"border: none;\n"
"background: transparent;")
        self.dragBar.setFrameShape(QFrame.StyledPanel)
        self.dragBar.setFrameShadow(QFrame.Raised)
        self.ctx_btns = QFrame(self.bgApp)
        self.ctx_btns.setObjectName(u"ctx_btns")
        self.ctx_btns.setGeometry(QRect(230, 10, 111, 31))
        self.ctx_btns.setStyleSheet(u"QFrame  {\n"
"	background-color: rgba(94, 76, 154, 150);\n"
"	border: 2px solid rgb(181, 181, 181);\n"
"	border-radius: 15px;\n"
"}")
        self.ctx_btns.setFrameShape(QFrame.StyledPanel)
        self.ctx_btns.setFrameShadow(QFrame.Raised)
        self.btn_minimize = QPushButton(self.ctx_btns)
        self.btn_minimize.setObjectName(u"btn_minimize")
        self.btn_minimize.setGeometry(QRect(10, 0, 31, 31))
        self.btn_minimize.setMinimumSize(QSize(10, 10))
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
        self.btn_close.setGeometry(QRect(43, 0, 31, 31))
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
        self.responseLabel = QLabel(self.bgApp)
        self.responseLabel.setObjectName(u"responseLabel")
        self.responseLabel.setGeometry(QRect(0, 460, 351, 41))
        self.responseLabel.setStyleSheet(u"color: rgb(113, 126, 149);\n"
"border-bottom-left-radius: 20px;\n"
"border-bottom-right-radius: 20px;")
        self.responseLabel.setLineWidth(1)
        self.responseLabel.setAlignment(Qt.AlignCenter)
        self.twofactor_responselabel = QLabel(self.bgApp)
        self.twofactor_responselabel.setObjectName(u"twofactor_responselabel")
        self.twofactor_responselabel.setGeometry(QRect(0, 460, 351, 41))
        self.twofactor_responselabel.setStyleSheet(u"color: rgb(113, 126, 149);")
        self.twofactor_responselabel.setLineWidth(1)
        self.twofactor_responselabel.setAlignment(Qt.AlignCenter)
        self.bg1.raise_()
        self.logo.raise_()
        self.creditsLabel.raise_()
        self.creditsLabel_2.raise_()
        self.pages.raise_()
        self.dragBar.raise_()
        self.responseLabel.raise_()
        self.ctx_btns.raise_()
        self.btn_dropdown.raise_()
        self.twofactor_responselabel.raise_()

        self.verticalLayout_2.addWidget(self.bgApp)

        LoginWindow.setCentralWidget(self.styleSheet)

        self.retranslateUi(LoginWindow)

        self.pages.setCurrentIndex(2)
        self.btn_minimize.setDefault(False)


        QMetaObject.connectSlotsByName(LoginWindow)
    # setupUi

    def retranslateUi(self, LoginWindow):
        LoginWindow.setWindowTitle(QCoreApplication.translate("LoginWindow", u"Polaris", None))
        self.bg1.setText("")
        self.logo.setText("")
        self.creditsLabel.setText(QCoreApplication.translate("LoginWindow", u"Milestone 3 Build", None))
        self.creditsLabel_2.setText(QCoreApplication.translate("LoginWindow", u"1.0.0", None))
        self.btn_dropdown.setText("")
        self.login_button.setText(QCoreApplication.translate("LoginWindow", u" Log In", None))
        self.password.setInputMask("")
        self.password.setText("")
        self.password.setPlaceholderText(QCoreApplication.translate("LoginWindow", u"...", None))
        self.passwordLabel.setText(QCoreApplication.translate("LoginWindow", u"Password", None))
#if QT_CONFIG(tooltip)
        self.register_button.setToolTip(QCoreApplication.translate("LoginWindow", u"<html><head/><body><p>This will take you to our website.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.register_button.setText(QCoreApplication.translate("LoginWindow", u"  Register", None))
        self.icon_2.setText("")
        self.btn_dashboard_2.setText(QCoreApplication.translate("LoginWindow", u"  Password Login", None))
        self.username.setText("")
        self.username.setPlaceholderText(QCoreApplication.translate("LoginWindow", u"...", None))
        self.usernameLabel.setText(QCoreApplication.translate("LoginWindow", u"Username", None))
        self.passwordLabel_3.setText(QCoreApplication.translate("LoginWindow", u"Password", None))
        self.password_token.setInputMask("")
        self.password_token.setText("")
        self.password_token.setPlaceholderText(QCoreApplication.translate("LoginWindow", u"...", None))
        self.btn_dashboard_3.setText(QCoreApplication.translate("LoginWindow", u"  Token Login", None))
        self.loginTokenButton.setText(QCoreApplication.translate("LoginWindow", u" Log In", None))
#if QT_CONFIG(tooltip)
        self.loginNormalButton.setToolTip(QCoreApplication.translate("LoginWindow", u"<html><head/><body><p>This will take you to our website.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.loginNormalButton.setText(QCoreApplication.translate("LoginWindow", u"Log In Without Token", None))
        self.icon_3.setText("")
        self.passwordLabel_2.setText(QCoreApplication.translate("LoginWindow", u"Authenticator code", None))
        self.twofactor_field.setInputMask("")
        self.twofactor_field.setText("")
        self.twofactor_field.setPlaceholderText(QCoreApplication.translate("LoginWindow", u"...", None))
        self.twofactor_button.setText(QCoreApplication.translate("LoginWindow", u" Log In", None))
        self.btn_dashboard.setText(QCoreApplication.translate("LoginWindow", u"  2-Factor Auth", None))
        self.icon_1.setText("")
        self.btn_minimize.setText("")
        self.btn_close.setText("")
        self.responseLabel.setText("")
        self.twofactor_responselabel.setText("")
    # retranslateUi

