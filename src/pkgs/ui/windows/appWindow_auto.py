# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'appWindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ..assets import resources_auto

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1130, 904)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamily(u"Nunito SemiBold")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        MainWindow.setFont(font)
        icon = QIcon()
        icon.addFile(u":/window/icons/app-icon.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.unitMngmtFrame = QFrame(self.centralwidget)
        self.unitMngmtFrame.setObjectName(u"unitMngmtFrame")
        self.unitMngmtFrame.setFrameShape(QFrame.StyledPanel)
        self.unitMngmtFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.unitMngmtFrame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.ctrlrGroupBex = QGroupBox(self.unitMngmtFrame)
        self.ctrlrGroupBex.setObjectName(u"ctrlrGroupBex")
        self.gridLayout = QGridLayout(self.ctrlrGroupBex)
        self.gridLayout.setObjectName(u"gridLayout")
        self.ctrlrWheelIcon = QGraphicsView(self.ctrlrGroupBex)
        self.ctrlrWheelIcon.setObjectName(u"ctrlrWheelIcon")
        self.ctrlrWheelIcon.setEnabled(False)

        self.gridLayout.addWidget(self.ctrlrWheelIcon, 1, 0, 2, 1)

        self.ctrlrSelect = QComboBox(self.ctrlrGroupBex)
        self.ctrlrSelect.setObjectName(u"ctrlrSelect")

        self.gridLayout.addWidget(self.ctrlrSelect, 0, 1, 1, 1)

        self.ctrlrCalBtn = QPushButton(self.ctrlrGroupBex)
        self.ctrlrCalBtn.setObjectName(u"ctrlrCalBtn")

        self.gridLayout.addWidget(self.ctrlrCalBtn, 0, 0, 1, 1)

        self.ctrlRefreshBtn = QPushButton(self.ctrlrGroupBex)
        self.ctrlRefreshBtn.setObjectName(u"ctrlRefreshBtn")
        icon1 = QIcon()
        icon1.addFile(u":/controller/icons/reload.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.ctrlRefreshBtn.setIcon(icon1)
        self.ctrlRefreshBtn.setIconSize(QSize(20, 20))

        self.gridLayout.addWidget(self.ctrlRefreshBtn, 0, 2, 1, 1)

        self.ctrlrThrlBar = QProgressBar(self.ctrlrGroupBex)
        self.ctrlrThrlBar.setObjectName(u"ctrlrThrlBar")
        self.ctrlrThrlBar.setEnabled(False)
        self.ctrlrThrlBar.setValue(24)

        self.gridLayout.addWidget(self.ctrlrThrlBar, 1, 1, 1, 2)

        self.ctrlrBrkBar = QProgressBar(self.ctrlrGroupBex)
        self.ctrlrBrkBar.setObjectName(u"ctrlrBrkBar")
        self.ctrlrBrkBar.setEnabled(False)
        self.ctrlrBrkBar.setValue(24)

        self.gridLayout.addWidget(self.ctrlrBrkBar, 2, 1, 1, 2)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 3)

        self.verticalLayout.addWidget(self.ctrlrGroupBex)

        self.unitsGroupBox = QGroupBox(self.unitMngmtFrame)
        self.unitsGroupBox.setObjectName(u"unitsGroupBox")
        self.verticalLayout_2 = QVBoxLayout(self.unitsGroupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.unitsListView = QListView(self.unitsGroupBox)
        self.unitsListView.setObjectName(u"unitsListView")

        self.verticalLayout_2.addWidget(self.unitsListView)


        self.verticalLayout.addWidget(self.unitsGroupBox)

        self.commGroupBox = QGroupBox(self.unitMngmtFrame)
        self.commGroupBox.setObjectName(u"commGroupBox")
        self.gridLayout_2 = QGridLayout(self.commGroupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.lineEdit_2 = QLineEdit(self.commGroupBox)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.gridLayout_2.addWidget(self.lineEdit_2, 2, 1, 1, 1)

        self.brokerPortLabel = QLabel(self.commGroupBox)
        self.brokerPortLabel.setObjectName(u"brokerPortLabel")

        self.gridLayout_2.addWidget(self.brokerPortLabel, 1, 0, 1, 1)

        self.brokerHostnameLabel = QLabel(self.commGroupBox)
        self.brokerHostnameLabel.setObjectName(u"brokerHostnameLabel")

        self.gridLayout_2.addWidget(self.brokerHostnameLabel, 0, 0, 1, 1)

        self.lineEdit = QLineEdit(self.commGroupBox)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridLayout_2.addWidget(self.lineEdit, 0, 1, 1, 1)

        self.spinBox = QSpinBox(self.commGroupBox)
        self.spinBox.setObjectName(u"spinBox")

        self.gridLayout_2.addWidget(self.spinBox, 1, 1, 1, 1)

        self.lineEdit_3 = QLineEdit(self.commGroupBox)
        self.lineEdit_3.setObjectName(u"lineEdit_3")

        self.gridLayout_2.addWidget(self.lineEdit_3, 3, 1, 1, 1)

        self.connectionBtn = QPushButton(self.commGroupBox)
        self.connectionBtn.setObjectName(u"connectionBtn")
        icon2 = QIcon()
        icon2.addFile(u":/communication/icons/disconnected.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.connectionBtn.setIcon(icon2)
        self.connectionBtn.setIconSize(QSize(32, 32))

        self.gridLayout_2.addWidget(self.connectionBtn, 0, 2, 4, 1)

        self.mqttIdLabel = QLabel(self.commGroupBox)
        self.mqttIdLabel.setObjectName(u"mqttIdLabel")

        self.gridLayout_2.addWidget(self.mqttIdLabel, 2, 0, 1, 1)

        self.mqttPasswordLabel = QLabel(self.commGroupBox)
        self.mqttPasswordLabel.setObjectName(u"mqttPasswordLabel")

        self.gridLayout_2.addWidget(self.mqttPasswordLabel, 3, 0, 1, 1)

        self.gridLayout_2.setColumnStretch(0, 1)

        self.verticalLayout.addWidget(self.commGroupBox)


        self.horizontalLayout.addWidget(self.unitMngmtFrame)

        self.cmdTabs = QTabWidget(self.centralwidget)
        self.cmdTabs.setObjectName(u"cmdTabs")
        self.stateCmdTab = QWidget()
        self.stateCmdTab.setObjectName(u"stateCmdTab")
        self.cmdTabs.addTab(self.stateCmdTab, "")
        self.fpvTab = QWidget()
        self.fpvTab.setObjectName(u"fpvTab")
        self.cmdTabs.addTab(self.fpvTab, "")

        self.horizontalLayout.addWidget(self.cmdTabs)

        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 5)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QRect(0, 0, 1130, 30))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setEnabled(True)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.cmdTabs.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"RC Mission Commander", None))
        self.ctrlrGroupBex.setTitle(QCoreApplication.translate("MainWindow", u"Controller", None))
        self.ctrlrCalBtn.setText(QCoreApplication.translate("MainWindow", u"Calibrate", None))
        self.ctrlRefreshBtn.setText("")
        self.unitsGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Units", None))
        self.commGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Communication", None))
        self.brokerPortLabel.setText(QCoreApplication.translate("MainWindow", u"Port", None))
        self.brokerHostnameLabel.setText(QCoreApplication.translate("MainWindow", u"Broker", None))
        self.connectionBtn.setText("")
        self.mqttIdLabel.setText(QCoreApplication.translate("MainWindow", u"Client ID", None))
        self.mqttPasswordLabel.setText(QCoreApplication.translate("MainWindow", u"Password", None))
        self.cmdTabs.setTabText(self.cmdTabs.indexOf(self.stateCmdTab), QCoreApplication.translate("MainWindow", u"State/Cmd", None))
        self.cmdTabs.setTabText(self.cmdTabs.indexOf(self.fpvTab), QCoreApplication.translate("MainWindow", u"FPV", None))
    # retranslateUi

