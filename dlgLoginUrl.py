from os import fdopen
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox

import connectDB
import global_var

#import websockets.legacy.server
#import websockets.legacy.client
from td.client import TDClient

class LoginUrlWindow(QWidget):
    switch_menu = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        mainLayout = QGridLayout()

        toplayout = QVBoxLayout()
        self.urlEdit = QLineEdit()
        self.urlEdit.setFixedHeight(32)
        self.urlEdit.setStyleSheet("font-size: 18px;")
        urlLabel = QLabel("Please type the callback url:")
        urlLabel.setStyleSheet("font-size: 16px;")
        urlLabel.setBuddy(self.urlEdit)
        toplayout.addWidget(urlLabel)
        toplayout.addWidget(self.urlEdit)
        mainLayout.addLayout(toplayout, 0, 0, 1, 2)
        
        toolbarLayout = QHBoxLayout()
        registerBtn = QPushButton("&Register")
        registerBtn.setFixedHeight(32)
        registerBtn.setStyleSheet("background-color : {color}; color: #FFF; font-weight: bold; font-size: 18px;".format(color=global_var.color_blue))
        registerBtn.clicked.connect(lambda: self.register())
        toolbarLayout.addWidget(registerBtn)
        cancelBtn = QPushButton("&Cancel")
        cancelBtn.setFixedHeight(32)
        cancelBtn.setStyleSheet("background-color : {color}; color: #FFF; font-weight: bold; font-size: 18px;".format(color=global_var.color_red))
        cancelBtn.clicked.connect(lambda: self.hide())
        toolbarLayout.addWidget(cancelBtn)
        mainLayout.addLayout(toolbarLayout, 3, 1, 1, 1)

        self.setLayout(mainLayout)
        self.resize(400, 160)
        self.setWindowTitle("TRADE COPIER - Login")
    
    def register(self):
        url = self.urlEdit.text()
        user = connectDB.getUser(global_var.current_login_userid)
        client_id = user['client_id']
        TDSession = TDClient(
            client_id=client_id,
            redirect_uri='http://127.0.0.1:3000',
            credentials_path='./token/'+client_id+'.json'
        )
        TDSession.code = url
        TDSession.exchange_code_for_token(
            code=TDSession.code,
            return_refresh_token=True
        )
        self.hide()
        QMessageBox.about(self, "Status", "You are registered.")

    def closeEvent(self, event):
        self.hide()
        event.ignore()



