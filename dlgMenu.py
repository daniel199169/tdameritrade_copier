from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

import dlgAccount
import dlgProfit
import dlgStoploss
import dlgFriday
import dlgNotification
import global_var

class MenuWindow(QWidget):
    switch_trade = QtCore.pyqtSignal()
    switch_profit = QtCore.pyqtSignal()
    switch_stoploss = QtCore.pyqtSignal()
    switch_notification = QtCore.pyqtSignal()
    switch_friday = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        global_var.opendDlg = True
        mainLayout = QVBoxLayout()
        
        tradeBtn = QPushButton("COPY TRADES")
        self.switch_trade.connect(self.toTrade)
        tradeBtn.setFixedHeight(80)
        tradeBtn.setStyleSheet("background-color : {color}; color: #FFF; font-weight: bold; font-size: 18px;".format(color=global_var.color_blue))
        tradeBtn.clicked.connect(self.switch_trade.emit)
        mainLayout.addWidget(tradeBtn)

        profitBtn = QPushButton("PROFIT TRAILER")
        profitBtn.setFixedHeight(80)
        profitBtn.setStyleSheet("background-color : {color}; color: #FFF; font-weight: bold; font-size: 18px;".format(color=global_var.color_blue))
        self.switch_profit.connect(self.toProfit)
        profitBtn.clicked.connect(self.switch_profit.emit)
        mainLayout.addWidget(profitBtn)

        stoplossBtn = QPushButton("STOP LOSS")
        stoplossBtn.setFixedHeight(80)
        stoplossBtn.setStyleSheet("background-color : {color}; color: #FFF; font-weight: bold; font-size: 18px;".format(color=global_var.color_blue))
        self.switch_stoploss.connect(self.toStopLoss)
        stoplossBtn.clicked.connect(self.switch_stoploss.emit)
        mainLayout.addWidget(stoplossBtn)

        notifiBtn = QPushButton("NOTIFICATIONS")
        notifiBtn.setFixedHeight(80)
        notifiBtn.setStyleSheet("background-color : {color}; color: #FFF; font-weight: bold; font-size: 18px;".format(color=global_var.color_blue))
        self.switch_notification.connect(self.toNotification)
        notifiBtn.clicked.connect(self.switch_notification.emit)
        mainLayout.addWidget(notifiBtn)
        fridayBtn = QPushButton("FRIDAY MAX")
        fridayBtn.setFixedHeight(80)
        fridayBtn.setStyleSheet("background-color : {color}; color: #FFF; font-weight: bold; font-size: 18px;".format(color=global_var.color_blue))
        self.switch_friday.connect(self.toFriday)
        fridayBtn.clicked.connect(self.switch_friday.emit)
        mainLayout.addWidget(fridayBtn)

        self.setLayout(mainLayout)
        self.resize(600, 400)
        #self.setStyleSheet("background-color: #2F2F3F;")
        self.setWindowTitle("Trade Copier")

    def closeEvent(self, event):
        self.hide()
        global_var.opendDlg = False
        event.ignore()

    def toTrade(self):
        self.tgt = dlgAccount.HomeWindow()
        self.hide()
        self.tgt.show()
    
    def toProfit(self):
        self.tgt = dlgProfit.ProfitWindow('menu', '', -1, None)
        self.hide()
        self.tgt.show()
    
    def toStopLoss(self):
        self.tgt = dlgStoploss.StopLossWindow('menu', '', -1, None)
        self.hide()
        self.tgt.show()
    
    def toNotification(self):
        self.tgt = dlgNotification.NotificationWindow()
        self.hide()
        self.tgt.show()
    
    def toFriday(self):
        self.tgt = dlgFriday.FridayWindow()
        self.hide()
        self.tgt.show()
