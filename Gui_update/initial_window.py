# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Main.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from Gui_update.waitadmin import Wait_admin
from Gui_update.waitmember import Wait_member
from squarcle_data import squarcle_data
import threading
from ComOrchestrator import ComOrchestrator

class Ui_Form(object):
    s_data = 0
    def setupUi(self, Form, s_data):
        self.s_data = s_data
        Form.setObjectName("Form")
        Form.resize(414, 359)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(40, 220, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(260, 220, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(50, 90, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(130, 90, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 170, 46, 13))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.textEdit_2 = QtWidgets.QTextEdit(Form)
        self.textEdit_2.setGeometry(QtCore.QRect(50, 160, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.textEdit_2.setFont(font)
        self.textEdit_2.setObjectName("textEdit_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(80, 20, 251, 41))
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.pushButton.clicked.connect(self.setParameters_join)
        self.pushButton_2.clicked.connect(self.setParameters_create)
   

    def setParameters_join(self):

        orchestrator_obj = ComOrchestrator(self.s_data)
        com_thread = threading.Thread()
        com_thread = threading.Thread(name='Com_thread', target=orchestrator_obj.slave_starter)

        self.s_data.acquire()
        self.s_data.set_name(self.textEdit.toPlainText())
        self.s_data.set_creator_ID(int(self.textEdit_2.toPlainText()))
        self.s_data.release()
        print(self.textEdit.toPlainText())
        print(self.textEdit_2.toPlainText())

        com_thread.start()

        Form.hide()
        wait_guim = Wait_member(self.s_data)
    
    def setParameters_create(self):
        ##Launching the communication thread here
        # Initializing a communication orchestrator object
        orchestrator_obj = ComOrchestrator(self.s_data)
        com_thread = threading.Thread()

        # This node is a master
        com_thread = threading.Thread(name='Com_thread', target=orchestrator_obj.master_starter)


        self.s_data.acquire()
        self.s_data.set_name(self.textEdit.toPlainText())
        #self.s_data.set_com_thread(com_thread)
        self.s_data.release()
        print(self.textEdit.toPlainText())

        #com_thread.start()

        
        Form.hide()
        wait_guia = Wait_admin(self.s_data)
        






    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Join"))
        self.pushButton_2.setText(_translate("Form", "Create"))
        self.label.setText(_translate("Form", "Name"))
        self.label_2.setText(_translate("Form", "ID"))
        self.label_3.setText(_translate("Form", "Welcome to Squarcle"))




if __name__ == "__main__":
    import sys
    s_data = squarcle_data()
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form, s_data)
    Form.show()
    sys.exit(app.exec_())
