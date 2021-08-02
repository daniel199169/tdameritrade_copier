from os import fdopen
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel

import dlgMenu
import dlgAlert
import connectDB
import global_var

class StopLossWindow(QWidget):
    switch_menu = QtCore.pyqtSignal()
    callback_title = ''
    callback_userid = 0
    callback_orderdata = {}

    def __init__(self, target, cb_title, cb_userid, cb_orderdata):
        super().__init__()
        self.callback_title = cb_title
        self.callback_userid = cb_userid
        self.callback_orderdata = cb_orderdata
        global_var.opendDlg = True
        stoploss = connectDB.getStopLoss()
        mainLayout = QGridLayout()

        toplayout1 = QHBoxLayout()
        priceEdit = QLineEdit(stoploss['price'])
        priceEdit.setFixedHeight(32)
        priceEdit.setStyleSheet("font-size: 18px;")
        priceEdit.editingFinished.connect(lambda: self.changeLossMeta(priceEdit.text(), 'price'))
        priceLabel = QLabel("&Stock Price:")
        priceLabel.setBuddy(priceEdit)
        priceLabel.setStyleSheet("font-size: 16px;")
        toplayout1.addWidget(priceLabel)
        toplayout1.addWidget(priceEdit)
        mainLayout.addLayout(toplayout1, 0, 0, 1, 2)

        toplayout2 = QHBoxLayout()
        contractEdit = QLineEdit(stoploss['contract'])
        contractEdit.setFixedHeight(32)
        contractEdit.setStyleSheet("font-size: 18px;")
        contractEdit.editingFinished.connect(lambda: self.changeLossMeta(contractEdit.text(), 'contract'))
        contractLabel = QLabel("&Contract %:")
        contractLabel.setStyleSheet("font-size: 16px;")
        contractLabel.setBuddy(contractEdit)
        toplayout2.addWidget(contractLabel)
        toplayout2.addWidget(contractEdit)
        mainLayout.addLayout(toplayout2, 1, 0, 1, 2)

        toplayout3 = QHBoxLayout()
        lossEdit = QLineEdit(stoploss['stop_loss'])
        lossEdit.setFixedHeight(32)
        lossEdit.setStyleSheet("font-size: 18px;")
        lossEdit.editingFinished.connect(lambda: self.changeLossMeta(lossEdit.text(), 'stop_loss'))
        lossLabel = QLabel("Set Auto Stop &Loss:")
        lossLabel.setStyleSheet("font-size: 16px;")
        lossLabel.setBuddy(lossEdit)
        toplayout3.addWidget(lossLabel)
        toplayout3.addWidget(lossEdit)
        mainLayout.addLayout(toplayout3, 2, 0, 1, 2)
        
        toolbarLayout = QHBoxLayout()
        #addAccountBtn = QPushButton("&Save")
        #toolbarLayout.addWidget(addAccountBtn)
        menuBtn = QPushButton("&Save And Back")
        menuBtn.setFixedHeight(32)
        menuBtn.setStyleSheet("background-color : {color}; color: #FFF; font-weight: bold; font-size: 18px;".format(color=global_var.color_blue))
        self.switch_menu.connect(lambda:self.toMenu(target))
        menuBtn.clicked.connect(self.switch_menu.emit)
        toolbarLayout.addWidget(menuBtn)
        mainLayout.addLayout(toolbarLayout, 3, 1, 1, 1)

        self.setLayout(mainLayout)
        self.resize(400, 300)
        self.setWindowTitle("TRADE COPIER - STOP LOSS")
    
    def toMenu(self, target):
        if target == 'menu':
            self.tgt = dlgMenu.MenuWindow()
        else :
            self.tgt = dlgAlert.AlertWindow(self.callback_title, self.callback_userid, self.callback_orderdata)
        self.hide()
        self.tgt.show()

    def closeEvent(self, event):
        self.hide()
        global_var.opendDlg = False
        event.ignore()


    def changeLossMeta(self, text, col):
        connectDB.updateStopLoss(col, text)

