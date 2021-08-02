from os import fdopen
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel

import dlgMenu
import connectDB
import global_var

class NotificationWindow(QWidget):
    switch_menu = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        mainLayout = QGridLayout()
        notification = connectDB.getNotification()

        toplayout = QVBoxLayout()
        timeEdit = QLineEdit(notification['duration'])
        timeEdit.setFixedHeight(32)
        timeEdit.setStyleSheet("font-size: 18px;")
        timeEdit.editingFinished.connect(lambda: self.changeSetting(timeEdit.text(), 'duration'))
        urlLabel = QLabel("Notification Duration[s]:")
        urlLabel.setStyleSheet("font-size: 16px;")
        urlLabel.setBuddy(timeEdit)
        toplayout.addWidget(urlLabel)
        toplayout.addWidget(timeEdit)
        mainLayout.addLayout(toplayout, 0, 0, 1, 2)
        
        toolbarLayout = QHBoxLayout()
        menuBtn = QPushButton("&Save And Back")
        menuBtn.setFixedHeight(32)
        menuBtn.setStyleSheet("background-color : {color}; color: #FFF; font-weight: bold; font-size: 18px;".format(color=global_var.color_blue))
        self.switch_menu.connect(lambda:self.toMenu())
        menuBtn.clicked.connect(self.switch_menu.emit)
        toolbarLayout.addWidget(menuBtn)
        mainLayout.addLayout(toolbarLayout, 3, 1, 1, 1)

        self.setLayout(mainLayout)
        self.resize(400, 160)
        self.setWindowTitle("TRADE COPIER - NOTIFICATION")
    
    def changeSetting(self, text, col):
        connectDB.updateNotification(col, text)
    
    def toMenu(self):
        self.tgt = dlgMenu.MenuWindow()
        self.hide()
        self.tgt.show()

    def closeEvent(self, event):
        self.hide()
        global_var.opendDlg = False
        event.ignore()



