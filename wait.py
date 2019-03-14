# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wait.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!
import tkinter as tk
from tkinter import *
from PyQt5 import QtCore, QtGui, QtWidgets
from GUI import Main_Game
from Score import Ui_Form
from squarcle_data import squarcle_data

class Ui_MainWindow(object):
    s_data = 0
    def open_game(self):
        
        MainWindow.hide()
        maingui=Main_Game(self.s_data)
        self.Window=QtWidgets.QMainWindow()
        self.ui=Ui_Form()
        self.ui.setupUi(self.Window)
        self.Window.show()

        MainWindow.close()
        


    def setupUi(self, MainWindow, s_data):
        self.s_data = s_data
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(508, 357)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(330, 220, 121, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.open_game)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(170, 60, 191, 71))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 508, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Start"))
        self.label.setText(_translate("MainWindow", "Wait Please"))




if __name__ == "__main__":
    import sys
    s_data = squarcle_data()
    s_data.set_parameters(3, 1)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, s_data)
    MainWindow.show()
    sys.exit(app.exec_())
