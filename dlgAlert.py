from PyQt5 import QtCore
from PyQt5.QtWidgets import QDesktopWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel

import dlgMenu
import dlgProfit
import dlgStoploss
import global_var

class AlertWindow(QWidget):
    switch_menu = QtCore.pyqtSignal()
    switch_profit = QtCore.pyqtSignal()
    switch_stoploss = QtCore.pyqtSignal()
    title = ''
    userid = 0
    orderdata = {}

    def __init__(self, title, userid, orderdata):
        super().__init__()
        global_var.opendDlg = True
        mainLayout = QVBoxLayout()

        hlay1 = QHBoxLayout()
        titleLabel = QLabel(title)
        titleLabel.setStyleSheet("font-size: 18px;")
        self.title = title
        self.userid = userid
        self.orderdata = orderdata
        hlay1.addWidget(titleLabel, 1)
        mainLayout.addLayout(hlay1)


        hlay2 = QHBoxLayout()
        profitLabel = QLabel("Set PROFIT TRAILER?")
        profitLabel.setStyleSheet("font-size: 16px;")
        profitYesBtn = QPushButton("Yes")
        profitYesBtn.setFixedHeight(32)
        profitYesBtn.setStyleSheet("background-color : {color}; color: #FFF; font-weight: bold; font-size: 18px;".format(color=global_var.color_blue))
        self.switch_profit.connect(self.toProfit)
        profitYesBtn.clicked.connect(self.switch_profit.emit)
        profitNoBtn = QPushButton("No")
        profitNoBtn.setFixedHeight(32)
        profitNoBtn.setStyleSheet("background-color : {color}; color: #FFF; font-weight: bold; font-size: 18px;".format(color=global_var.color_red))
        profitNoBtn.clicked.connect(self.hideMyDlg)
        hlay2.addWidget(profitLabel, 1)
        hlay2.addWidget(profitYesBtn)
        hlay2.addWidget(profitNoBtn)
        mainLayout.addLayout(hlay2)


        hlay3 = QHBoxLayout()
        lossLabel = QLabel("Set STOP LOSS?")
        lossLabel.setStyleSheet("font-size: 16px;")
        stopYesBtn = QPushButton("Yes")
        stopYesBtn.setFixedHeight(32)
        stopYesBtn.setStyleSheet("background-color : {color}; color: #FFF; font-weight: bold; font-size: 18px;".format(color=global_var.color_blue))
        self.switch_stoploss.connect(self.toStopLoss)
        stopYesBtn.clicked.connect(self.switch_stoploss.emit)
        stopNoBtn = QPushButton("No")
        stopNoBtn.setFixedHeight(32)
        stopNoBtn.setStyleSheet("background-color : {color}; color: #FFF; font-weight: bold; font-size: 18px;".format(color=global_var.color_red))
        stopNoBtn.clicked.connect(self.hideMyDlg)
        hlay3.addWidget(lossLabel, 1)
        hlay3.addWidget(stopYesBtn)
        hlay3.addWidget(stopNoBtn)
        mainLayout.addLayout(hlay3)
        

        self.setLayout(mainLayout)
        self.resize(400, 150)

        ag = QDesktopWidget().availableGeometry()
        sg = QDesktopWidget().screenGeometry()
        widget = self.geometry()
        x = ag.width() - widget.width()
        y = 2 * ag.height() - sg.height() - widget.height()
        self.move(x, y)

        self.setWindowTitle("TRADE COPIER - SUB CALL")
    
    def toMenu(self):
        self.tgt = dlgMenu.MenuWindow()
        self.hide()
        self.tgt.show()

    def toProfit(self):
        self.tgt = dlgProfit.ProfitWindow('alert', self.title, self.userid, self.orderdata)
        self.hide()
        self.tgt.show()
    
    def toStopLoss(self):
        self.tgt = dlgStoploss.StopLossWindow('alert', self.title, self.userid, self.orderdata)
        self.hide()
        self.tgt.show()
    
    def hideMyDlg(self):
        global_var.opendDlg = False
        self.hide()

    def closeEvent(self, event):
        self.hide()
        global_var.opendDlg = False
        event.ignore()

