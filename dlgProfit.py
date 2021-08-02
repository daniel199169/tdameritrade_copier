import os
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QScrollArea, QGroupBox, QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QIcon

import dlgMenu
import dlgAlert
import connectDB
import global_var

#import websockets.legacy.server
#import websockets.legacy.client
from td.client import TDClient

class ProfitWindow(QWidget):
    switch_menu = QtCore.pyqtSignal()
    profit_group = {}
    dbids = []
    profit_index = 1
    callback_title = ''
    callback_userid = 0
    callback_orderdata = {}

    def __init__(self, target, cb_title, cb_userid, cb_orderdata):
        super().__init__()
        self.callback_title = cb_title
        self.callback_userid = cb_userid
        self.callback_orderdata = cb_orderdata
        global_var.opendDlg = True
        profits = connectDB.getProfit()
        self.mainLayout = QGridLayout()

        listBox = QVBoxLayout()
        scroll = QScrollArea()
        listBox.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)
        self.scrollLayout = QVBoxLayout(scrollContent)
        scrollContent.setLayout(self.scrollLayout)
        for x in profits:
            self.profit_group[x['id']] = self.creatOneProfit(x, self.profit_index)
            self.profit_index = self.profit_index + 1
            self.scrollLayout.addWidget(self.profit_group[x['id']])
            self.dbids.append(x['id'])
        scroll.setWidget(scrollContent)
        self.mainLayout.addLayout(listBox, 0, 0, 1, 2)
        
        toolbarLayout = QHBoxLayout()
        saveBtn = QPushButton("&Add Take Profit")
        saveBtn.clicked.connect(self.makeProfit)
        saveBtn.setStyleSheet("background-color : {color}; color: #FFF; font-weight: bold; font-size: 18px;".format(color=global_var.color_info_back))
        toolbarLayout.addWidget(saveBtn)
        menuBtn = QPushButton("&Save And Back")
        menuBtn.setFixedHeight(32)
        menuBtn.setStyleSheet("background-color : {color}; color: #FFF; font-weight: bold; font-size: 18px;".format(color=global_var.color_blue))
        self.switch_menu.connect(lambda:self.toMenu(target))
        menuBtn.clicked.connect(self.switch_menu.emit)
        toolbarLayout.addWidget(menuBtn)
        self.mainLayout.addLayout(toolbarLayout, 1, 1, 1, 1)

        self.setLayout(self.mainLayout)
        self.resize(400, 460)
        self.setWindowTitle("TRADE COPIER - PROFIT TRAILER")
    
    def creatOneProfit(self, dbmeta, pm_index):
        newProfit = QGroupBox("Profit Trailer "+str(pm_index))
        newProfit.setStyleSheet("color: #FFF; font-weight: bold; font-size: 20px;")
        profitlayout = QVBoxLayout()
        toplayout = QHBoxLayout()
        profitEdit = QLineEdit(dbmeta['profit'])
        profitEdit.setFixedHeight(32)
        profitEdit.setStyleSheet("font-size: 18px; color: #000; font-weight: normal;")
        profitEdit.editingFinished.connect(lambda: self.changedbmeta(profitEdit.text(), 'profit', dbmeta['id']))
        profitLabel = QLabel("Take Profit "+str(pm_index))
        profitLabel.setStyleSheet("font-size: 16px;")
        profitPercentLabel = QLabel("%")
        profitPercentLabel.setStyleSheet("font-size: 16px;")
        deleteBtn = QPushButton("")
        deleteBtn.setFixedHeight(32)
        deleteBtn.setStyleSheet("background-color : {color}; color: #FFF; font-weight: bold; font-size: 18px;".format(color=global_var.color_red))
        deleteBtn.setToolTip("Delete")
        deleteBtn.setIcon(QIcon('delete.png'))
        deleteBtn.clicked.connect(lambda: self.deleteTrailer(dbmeta['id']))
        toplayout.addWidget(profitLabel)
        toplayout.addWidget(profitPercentLabel)
        toplayout.addWidget(profitEdit)
        toplayout.addWidget(deleteBtn)
        toplayout.addStretch(1)
        profitlayout.addLayout(toplayout)
        bottomlayout = QHBoxLayout()
        priceEdit = QLineEdit(dbmeta['price'])
        priceEdit.setFixedHeight(32)
        priceEdit.setStyleSheet("font-size: 18px; color: #000; font-weight: normal;")
        priceEdit.editingFinished.connect(lambda: self.changedbmeta(priceEdit.text(), 'price', dbmeta['id']))
        priceLabel = QLabel("Price: ")
        priceLabel.setStyleSheet("font-size: 16px;")
        contractEdit = QLineEdit(dbmeta['contract'])
        contractEdit.setFixedHeight(32)
        contractEdit.setStyleSheet("font-size: 18px; color: #000; font-weight: normal;")
        contractEdit.editingFinished.connect(lambda: self.changedbmeta(contractEdit.text(), 'contract', dbmeta['id']))
        contractLabel = QLabel("Contract%: ")
        contractLabel.setStyleSheet("font-size: 16px;")
        bottomlayout.addWidget(priceLabel)
        bottomlayout.addWidget(priceEdit)
        bottomlayout.addWidget(contractLabel)
        bottomlayout.addWidget(contractEdit)
        profitlayout.addLayout(bottomlayout)
        newProfit.setLayout(profitlayout)
        return newProfit
    
    def toMenu(self, target):
        ret = connectDB.validateProfit()
        if len(ret) == 0:
            if target == 'menu':
                self.tgt = dlgMenu.MenuWindow()
            else :
                self.tgt = dlgAlert.AlertWindow(self.callback_title, self.callback_userid, self.callback_orderdata)
            self.hide()
            self.tgt.show()
        else:
            QMessageBox.about(self, "Error", "Input correct profit trailer.")
            for x in self.dbids:
                if ret[0]['id'] == x:
                    objs = self.profit_group[x].findChildren(QLineEdit)
                    objs[1].setFocus()

    def closeEvent(self, event):
        self.hide()
        global_var.opendDlg = False
        event.ignore()

    
    def changedbmeta(self, text, column, id):
        connectDB.updateProfit(id, column, text)
    
    def deleteTrailer(self, id):
        connectDB.deleteProfit(id)
        tmp = []
        for x in self.dbids:
            if x == id:
                self.profit_group[x].setParent(None)
            else:
                tmp.append(x)
        self.dbids = tmp
    
    def makeProfit(self):
        """x = connectDB.getUser(self.callback_userid)
        print(self.callback_userid)
        print(x)
        client_id = x['client_id']
        TDSession = TDClient(
            client_id=client_id,
            redirect_uri='http://127.0.0.1:3000',
            credentials_path='./token/'+client_id+'.json'
        )
        if(os.path.isfile(TDSession.credentials_path) and TDSession._silent_sso()):
            TDSession.login()
            accmeta = TDSession.get_accounts()
            print('$'*80)
            print(TDSession.place_order(account=accmeta[0]['securitiesAccount']['accountId'], order=self.callback_orderdata))
            print('*'*80)
            #print(accmeta)
            #print(self.callback_orderdata)
            QMessageBox.about(self, "Success", "Success!")
        else:
            QMessageBox.about(self, "Warning", "Can not use copier function.\nPlease register now.")"""
        new_id = connectDB.createProfit()
        new_obj = {
            'id' : new_id,
            'profit' : '',
            'price' : '',
            'contract' : ''
        }
        self.profit_group[new_id] = self.creatOneProfit(new_obj, self.profit_index)
        self.scrollLayout.addWidget(self.profit_group[new_id])
        self.dbids.append(new_id)
        self.profit_index = self.profit_index + 1

