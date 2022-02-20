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
        self.joystickGroupBex = QGroupBox(self.unitMngmtFrame)
        self.joystickGroupBex.setObjectName(u"joystickGroupBex")
        self.gridLayout = QGridLayout(self.joystickGroupBex)
        self.gridLayout.setObjectName(u"gridLayout")
        self.joystickWheelIcon = QGraphicsView(self.joystickGroupBex)
        self.joystickWheelIcon.setObjectName(u"joystickWheelIcon")
        self.joystickWheelIcon.setEnabled(False)

        self.gridLayout.addWidget(self.joystickWheelIcon, 1, 0, 2, 1)

        self.joystickSelect = QComboBox(self.joystickGroupBex)
        self.joystickSelect.setObjectName(u"joystickSelect")

        self.gridLayout.addWidget(self.joystickSelect, 0, 1, 1, 1)

        self.joystickCalBtn = QPushButton(self.joystickGroupBex)
        self.joystickCalBtn.setObjectName(u"joystickCalBtn")
        self.joystickCalBtn.setEnabled(False)

        self.gridLayout.addWidget(self.joystickCalBtn, 0, 0, 1, 1)

        self.joystickThrlBar = QProgressBar(self.joystickGroupBex)
        self.joystickThrlBar.setObjectName(u"joystickThrlBar")
        self.joystickThrlBar.setEnabled(False)
        self.joystickThrlBar.setValue(24)

        self.gridLayout.addWidget(self.joystickThrlBar, 1, 1, 1, 2)

        self.joystickBrkBar = QProgressBar(self.joystickGroupBex)
        self.joystickBrkBar.setObjectName(u"joystickBrkBar")
        self.joystickBrkBar.setEnabled(False)
        self.joystickBrkBar.setValue(24)

        self.gridLayout.addWidget(self.joystickBrkBar, 2, 1, 1, 2)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 3)

        self.verticalLayout.addWidget(self.joystickGroupBex)

        self.unitsGroupBox = QGroupBox(self.unitMngmtFrame)
        self.unitsGroupBox.setObjectName(u"unitsGroupBox")
        self.verticalLayout_2 = QVBoxLayout(self.unitsGroupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.treeView = QTreeView(self.unitsGroupBox)
        self.treeView.setObjectName(u"treeView")

        self.verticalLayout_2.addWidget(self.treeView)


        self.verticalLayout.addWidget(self.unitsGroupBox)

        self.commGroupBox = QGroupBox(self.unitMngmtFrame)
        self.commGroupBox.setObjectName(u"commGroupBox")
        self.gridLayout_2 = QGridLayout(self.commGroupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.brokerHostnameLabel = QLabel(self.commGroupBox)
        self.brokerHostnameLabel.setObjectName(u"brokerHostnameLabel")

        self.gridLayout_2.addWidget(self.brokerHostnameLabel, 0, 0, 1, 1)

        self.brokerPortLabel = QLabel(self.commGroupBox)
        self.brokerPortLabel.setObjectName(u"brokerPortLabel")

        self.gridLayout_2.addWidget(self.brokerPortLabel, 1, 0, 1, 1)

        self.spinBox = QSpinBox(self.commGroupBox)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMaximum(65535)
        self.spinBox.setValue(1883)

        self.gridLayout_2.addWidget(self.spinBox, 1, 1, 1, 1)

        self.lineEdit = QLineEdit(self.commGroupBox)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridLayout_2.addWidget(self.lineEdit, 0, 1, 1, 1)

        self.connectionBtn = QPushButton(self.commGroupBox)
        self.connectionBtn.setObjectName(u"connectionBtn")
        icon1 = QIcon()
        icon1.addFile(u":/communication/icons/disconnected.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.connectionBtn.setIcon(icon1)
        self.connectionBtn.setIconSize(QSize(32, 32))

        self.gridLayout_2.addWidget(self.connectionBtn, 0, 3, 2, 1)

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

        self.cmdTabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"RC Mission Commander", None))
        self.joystickGroupBex.setTitle(QCoreApplication.translate("MainWindow", u"Joystick", None))
        self.joystickCalBtn.setText(QCoreApplication.translate("MainWindow", u"Calibrate", None))
        self.unitsGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Units", None))
        self.commGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Communication", None))
        self.brokerHostnameLabel.setText(QCoreApplication.translate("MainWindow", u"Broker", None))
        self.brokerPortLabel.setText(QCoreApplication.translate("MainWindow", u"Port", None))
        self.connectionBtn.setText("")
        self.cmdTabs.setTabText(self.cmdTabs.indexOf(self.stateCmdTab), QCoreApplication.translate("MainWindow", u"State/Cmd", None))
        self.cmdTabs.setTabText(self.cmdTabs.indexOf(self.fpvTab), QCoreApplication.translate("MainWindow", u"FPV", None))
    # retranslateUi

