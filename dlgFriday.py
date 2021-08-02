from os import fdopen
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QRadioButton, QButtonGroup

import dlgMenu
from comSwitch import MySwitch
import connectDB
import global_var

class FridayWindow(QWidget):
    switch_menu = QtCore.pyqtSignal()
    state_all = True
    state_range = False

    def __init__(self):
        super().__init__()
        global_var.opendDlg = True
        friday_max = connectDB.getFridayMax()
        if friday_max['on_off'] == 1:
            self.state_all = True
        else:
            self.state_all = False
        if friday_max['all_some'] == 1:
            self.state_range = True
        else:
            self.state_range = False
        mainLayout = QGridLayout()

        toplayout1 = QHBoxLayout()
        self.priceEdit = QLineEdit(friday_max['max_percent'])
        self.priceEdit.setFixedHeight(32)
        self.priceEdit.setStyleSheet("font-size: 18px;")
        self.priceEdit.editingFinished.connect(lambda: self.changeSetting(self.priceEdit.text(), 'max_percent'))
        priceLabel = QLabel("&Friday Max %:")
        priceLabel.setBuddy(self.priceEdit)
        priceLabel.setStyleSheet("font-size: 16px;")
        # radiobuttonon = QRadioButton("On")
        # radiobuttonon.setStyleSheet("font-size: 18px;")
        # if self.state_all:
        #     radiobuttonon.setChecked(True)
        # radiobuttonon.value = "On"
        # radiobuttonon.toggled.connect(self.onOnOff)
        # radiobuttonoff = QRadioButton("Off")
        # radiobuttonoff.setStyleSheet("font-size: 18px;")
        # if not self.state_all:
        #     radiobuttonoff.setChecked(True)
        # radiobuttonoff.value = "Off"
        # radiobuttonoff.toggled.connect(self.onOnOff)
        
        # onoff_group = QButtonGroup(self)
        # onoff_group.addButton(radiobuttonon)
        # onoff_group.addButton(radiobuttonoff)
        allowBtn = MySwitch(98, 22, 16, 44)
        if self.state_all == 1:
            allowBtn.setChecked(True)
        else:
            allowBtn.setChecked(False)
        allowBtn.clicked.connect(lambda: self.onOnOff(allowBtn.isChecked()))
        toplayout1.addWidget(priceLabel)
        toplayout1.addWidget(self.priceEdit)
        # toplayout1.addWidget(radiobuttonon)
        # toplayout1.addWidget(radiobuttonoff)
        toplayout1.addWidget(allowBtn)
        mainLayout.addLayout(toplayout1, 0, 0, 1, 2)

        toplayout2 = QHBoxLayout()
        self.radiobuttonall = QRadioButton("All")
        self.radiobuttonall.setStyleSheet("font-size: 18px;")
        if not self.state_range:
            self.radiobuttonall.setChecked(True)
        # self.radiobuttonall.value = "All"
        # self.radiobuttonall.toggled.connect(self.onAllSome)
        # self.radiobuttonsome = QRadioButton("Some")
        # self.radiobuttonsome.setStyleSheet("font-size: 18px;")
        # if self.state_range:
        #     self.radiobuttonsome.setChecked(True)
        # self.radiobuttonsome.value = "Some"
        # self.radiobuttonsome.toggled.connect(self.onAllSome)
        # range_group = QButtonGroup(self)
        # range_group.addButton(self.radiobuttonall)
        # range_group.addButton(self.radiobuttonsome)
        self.rangeBtn = MySwitch(98, 22, 16, 44, t1="SOME", t2="ALL")
        if self.state_range == 1:
            self.rangeBtn.setChecked(True)
        else:
            self.rangeBtn.setChecked(False)
        self.rangeBtn.clicked.connect(lambda: self.onRange(self.rangeBtn.isChecked()))
        self.memberEdit = QLineEdit(friday_max['accs'])
        self.memberEdit.setFixedHeight(32)
        self.memberEdit.setStyleSheet("font-size: 18px;")
        self.memberEdit.editingFinished.connect(lambda: self.changeSetting(self.memberEdit.text(), 'accs'))
        contractLabel = QLabel("&Apply On:")
        contractLabel.setStyleSheet("font-size: 16px;")
        contractLabel.setBuddy(self.memberEdit)
        # lay2right.addWidget(self.radiobuttonall)
        # lay2right.addWidget(self.radiobuttonsome)
        toplayout2.addWidget(contractLabel)
        toplayout2.addWidget(self.memberEdit)
        toplayout2.addWidget(self.rangeBtn)
        mainLayout.addLayout(toplayout2, 1, 0, 1, 2)
        
        toolbarLayout = QHBoxLayout()
        menuBtn = QPushButton("&Save And Back")
        menuBtn.setFixedHeight(32)
        menuBtn.setStyleSheet("background-color : {color}; color: #FFF; font-weight: bold; font-size: 18px;".format(color=global_var.color_blue))
        self.switch_menu.connect(lambda:self.toMenu())
        menuBtn.clicked.connect(self.switch_menu.emit)
        toolbarLayout.addWidget(menuBtn)
        mainLayout.addLayout(toolbarLayout, 2, 1, 1, 1)

        self.setLayout(mainLayout)
        self.resize(400, 180)
        self._switchDlgState()
        self.setWindowTitle("TRADE COPIER - FRIDAY MAX")
    
    def toMenu(self):
        self.tgt = dlgMenu.MenuWindow()
        self.hide()
        self.tgt.show()

    def closeEvent(self, event):
        self.hide()
        global_var.opendDlg = False
        event.ignore()


    def changeSetting(self, text, col):
        connectDB.updateFridayMax(col, text)

    def onOnOff(self, state):
        if state:
            self.state_all = True
            connectDB.updateFridayMax('on_off', 1)
        else:
            self.state_all = False
            connectDB.updateFridayMax('on_off', 0)
        self._switchDlgState()
    
    def onRange(self, state):
        if state:
            self.state_range = True
            connectDB.updateFridayMax('all_some', 1)
        else:
            self.state_range = False
            connectDB.updateFridayMax('all_some', 0)
        self._switchDlgState()
    
    def _switchDlgState(self):
        if self.state_all == True:
            self.priceEdit.setEnabled(True)
            self.rangeBtn.setEnabled(True)
            # self.radiobuttonsome.setEnabled(True)
            if self.state_range == True:
                self.memberEdit.setEnabled(True)
            else:
                self.memberEdit.setEnabled(False)
        else:
            self.priceEdit.setEnabled(False)
            self.rangeBtn.setEnabled(False)
            # self.radiobuttonsome.setEnabled(False)
            self.memberEdit.setEnabled(False)
            
    def changeLossMeta(self, text, col):
        connectDB.updateStopLoss(col, text)

