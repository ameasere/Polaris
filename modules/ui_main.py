# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QStackedWidget, QVBoxLayout,
    QWidget)
from .resources_rc import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 720)
        icon = QIcon()
        icon.addFile(u":/images/images/images/Polaris.png", QSize(), QIcon.Normal, QIcon.Off)
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
        self.logo = QLabel(self.bgApp)
        self.logo.setObjectName(u"logo")
        self.logo.setGeometry(QRect(40, 30, 91, 20))
        self.logo.setPixmap(QPixmap(u":/images/images/Polaris.png"))
        self.logo.setScaledContents(True)
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
        self.ctx_btns.setGeometry(QRect(1071, 20, 161, 161))
        self.ctx_btns.setStyleSheet(u"QFrame  {\n"
"	background-color: rgba(94, 76, 154, 150);\n"
"	border: 2px solid rgb(181, 181, 181);\n"
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
"color: #A29F9F;")
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
"color: rgb(202, 202, 202)")
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
        self.creditsLabel_2.setGeometry(QRect(63, 50, 41, 16))
        self.creditsLabel_2.setMaximumSize(QSize(16777215, 16))
        self.creditsLabel_2.setFont(font1)
        self.creditsLabel_2.setStyleSheet(u"background-color: transparent;\n"
"font: 500 9pt \"Be Vietnam Pro\";\n"
"color: rgba(162, 159, 159, 120);\n"
"text-align: left;")
        self.creditsLabel_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.btn_dropdown = QPushButton(self.bgApp)
        self.btn_dropdown.setObjectName(u"btn_dropdown")
        self.btn_dropdown.setGeometry(QRect(1200, 20, 31, 31))
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
        self.btn_addfirsthsm = QPushButton(self.hsmlist)
        self.btn_addfirsthsm.setObjectName(u"btn_addfirsthsm")
        self.btn_addfirsthsm.setGeometry(QRect(10, 10, 421, 121))
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
        self.btn_addhsm_2 = QPushButton(self.hsmlist)
        self.btn_addhsm_2.setObjectName(u"btn_addhsm_2")
        self.btn_addhsm_2.setGeometry(QRect(500, 10, 421, 121))
        self.btn_addhsm_2.setMinimumSize(QSize(120, 15))
        self.btn_addhsm_2.setFont(font)
        self.btn_addhsm_2.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_addhsm_2.setStyleSheet(u"#btn_addhsm_2 {\n"
"background-color: rgba(222, 222, 222, 50);\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: center;\n"
"border: 1px solid rgba(255, 255, 255, 150);\n"
"border-radius: 5px;\n"
"}\n"
"#btn_addhsm_2:hover {\n"
"background-color: rgba(222, 222, 222, 90);\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: center;\n"
"border: 1px solid rgba(255, 255, 255, 150);\n"
"border-radius: 5px;\n"
"}\n"
"#btn_addhsm_2:pressed {\n"
"background-color: rgba(222, 222, 222, 150);\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: center;\n"
"border: 1px solid rgba(255, 255, 255, 150);\n"
"border-radius: 5px;\n"
"}")
        self.btn_addhsm_2.setIcon(icon2)
        self.btn_addhsm_3 = QPushButton(self.hsmlist)
        self.btn_addhsm_3.setObjectName(u"btn_addhsm_3")
        self.btn_addhsm_3.setGeometry(QRect(10, 160, 421, 121))
        self.btn_addhsm_3.setMinimumSize(QSize(120, 15))
        self.btn_addhsm_3.setFont(font)
        self.btn_addhsm_3.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_addhsm_3.setStyleSheet(u"#btn_addhsm_3 {\n"
"background-color: rgba(222, 222, 222, 50);\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: center;\n"
"border: 1px solid rgba(255, 255, 255, 150);\n"
"border-radius: 5px;\n"
"}\n"
"#btn_addhsm_3:hover {\n"
"background-color: rgba(222, 222, 222, 90);\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: center;\n"
"border: 1px solid rgba(255, 255, 255, 150);\n"
"border-radius: 5px;\n"
"}\n"
"#btn_addhsm_3:pressed {\n"
"background-color: rgba(222, 222, 222, 150);\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: center;\n"
"border: 1px solid rgba(255, 255, 255, 150);\n"
"border-radius: 5px;\n"
"}")
        self.btn_addhsm_3.setIcon(icon2)
        self.btn_addhsm_4 = QPushButton(self.hsmlist)
        self.btn_addhsm_4.setObjectName(u"btn_addhsm_4")
        self.btn_addhsm_4.setGeometry(QRect(500, 160, 421, 121))
        self.btn_addhsm_4.setMinimumSize(QSize(120, 15))
        self.btn_addhsm_4.setFont(font)
        self.btn_addhsm_4.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_addhsm_4.setStyleSheet(u"#btn_addhsm_4 {\n"
"background-color: rgba(222, 222, 222, 50);\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: center;\n"
"border: 1px solid rgba(255, 255, 255, 150);\n"
"border-radius: 5px;\n"
"}\n"
"#btn_addhsm_4:hover {\n"
"background-color: rgba(222, 222, 222, 90);\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: center;\n"
"border: 1px solid rgba(255, 255, 255, 150);\n"
"border-radius: 5px;\n"
"}\n"
"#btn_addhsm_4:pressed {\n"
"background-color: rgba(222, 222, 222, 150);\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: center;\n"
"border: 1px solid rgba(255, 255, 255, 150);\n"
"border-radius: 5px;\n"
"}")
        self.btn_addhsm_4.setIcon(icon2)
        self.btn_addhsm_5 = QPushButton(self.hsmlist)
        self.btn_addhsm_5.setObjectName(u"btn_addhsm_5")
        self.btn_addhsm_5.setGeometry(QRect(10, 310, 421, 121))
        self.btn_addhsm_5.setMinimumSize(QSize(120, 15))
        self.btn_addhsm_5.setFont(font)
        self.btn_addhsm_5.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_addhsm_5.setStyleSheet(u"#btn_addhsm_5 {\n"
"background-color: rgba(222, 222, 222, 50);\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: center;\n"
"border: 1px solid rgba(255, 255, 255, 150);\n"
"border-radius: 5px;\n"
"}\n"
"#btn_addhsm_5:hover {\n"
"background-color: rgba(222, 222, 222, 90);\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: center;\n"
"border: 1px solid rgba(255, 255, 255, 150);\n"
"border-radius: 5px;\n"
"}\n"
"#btn_addhsm_5:pressed {\n"
"background-color: rgba(222, 222, 222, 150);\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: center;\n"
"border: 1px solid rgba(255, 255, 255, 150);\n"
"border-radius: 5px;\n"
"}")
        self.btn_addhsm_5.setIcon(icon2)
        self.btn_addhsm_6 = QPushButton(self.hsmlist)
        self.btn_addhsm_6.setObjectName(u"btn_addhsm_6")
        self.btn_addhsm_6.setGeometry(QRect(500, 310, 421, 121))
        self.btn_addhsm_6.setMinimumSize(QSize(120, 15))
        self.btn_addhsm_6.setFont(font)
        self.btn_addhsm_6.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_addhsm_6.setStyleSheet(u"#btn_addhsm_6 {\n"
"background-color: rgba(222, 222, 222, 50);\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: center;\n"
"border: 1px solid rgba(255, 255, 255, 150);\n"
"border-radius: 5px;\n"
"}\n"
"#btn_addhsm_6:hover {\n"
"background-color: rgba(222, 222, 222, 90);\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: center;\n"
"border: 1px solid rgba(255, 255, 255, 150);\n"
"border-radius: 5px;\n"
"}\n"
"#btn_addhsm_6:pressed {\n"
"background-color: rgba(222, 222, 222, 150);\n"
"font: 600 10pt \"Inter Medium\";\n"
"text-align: center;\n"
"border: 1px solid rgba(255, 255, 255, 150);\n"
"border-radius: 5px;\n"
"}")
        self.btn_addhsm_6.setIcon(icon2)
        self.pages.addWidget(self.hsmlist)
        self.configurator = QWidget()
        self.configurator.setObjectName(u"configurator")
        self.pages.addWidget(self.configurator)
        self.controlpanel = QWidget()
        self.controlpanel.setObjectName(u"controlpanel")
        self.pages.addWidget(self.controlpanel)
        self.dragBar = QFrame(self.bgApp)
        self.dragBar.setObjectName(u"dragBar")
        self.dragBar.setGeometry(QRect(0, 0, 1255, 21))
        self.dragBar.setStyleSheet(u"border: none;\n"
"background: transparent;")
        self.dragBar.setFrameShape(QFrame.StyledPanel)
        self.dragBar.setFrameShadow(QFrame.Raised)
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
        self.logo.raise_()
        self.btn_dashboard.raise_()
        self.icon_1.raise_()
        self.sep1.raise_()
        self.btn_documentation.raise_()
        self.icon_2.raise_()
        self.sep2.raise_()
        self.sep3.raise_()
        self.icon_3.raise_()
        self.btn_account.raise_()
        self.ctx_btns.raise_()
        self.icon_4.raise_()
        self.btn_settings.raise_()
        self.sep4.raise_()
        self.creditsLabel.raise_()
        self.creditsLabel_2.raise_()
        self.btn_dropdown.raise_()
        self.pages.raise_()
        self.dragBar.raise_()
        self.btn_hsmlist.raise_()
        self.btn_controlpanel.raise_()
        self.btn_configurator.raise_()

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
        self.logo.setText("")
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
        self.creditsLabel.setText(QCoreApplication.translate("MainWindow", u"Milestone 3 Build", None))
        self.creditsLabel_2.setText(QCoreApplication.translate("MainWindow", u"0.3.0", None))
        self.btn_dropdown.setText("")
        self.btn_addfirsthsm.setText(QCoreApplication.translate("MainWindow", u"Add your first HSM", None))
        self.btn_addhsm_2.setText(QCoreApplication.translate("MainWindow", u"Add HSM", None))
        self.btn_addhsm_3.setText(QCoreApplication.translate("MainWindow", u"Add HSM", None))
        self.btn_addhsm_4.setText(QCoreApplication.translate("MainWindow", u"Add HSM", None))
        self.btn_addhsm_5.setText(QCoreApplication.translate("MainWindow", u"Add HSM", None))
        self.btn_addhsm_6.setText(QCoreApplication.translate("MainWindow", u"Add HSM", None))
        self.btn_hsmlist.setText(QCoreApplication.translate("MainWindow", u"HSM List", None))
        self.hsmlist_bg.setText("")
        self.btn_controlpanel.setText(QCoreApplication.translate("MainWindow", u"Control Panel", None))
        self.controlpanel_bg.setText("")
        self.btn_configurator.setText(QCoreApplication.translate("MainWindow", u"Configurator", None))
        self.configurator_bg.setText("")
    # retranslateUi

