from PyQt5 import QtCore
from PyQt5.QtWidgets import QDesktopWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel

import global_var

class MessageWindow(QWidget):
    switch_menu = QtCore.pyqtSignal()
    switch_profit = QtCore.pyqtSignal()
    switch_stoploss = QtCore.pyqtSignal()
    title = ''

    def __init__(self, title, backcolor=global_var.color_info_back):
        super().__init__()
        global_var.opendDlg = True
        mainLayout = QVBoxLayout()

        hlay1 = QHBoxLayout()
        titleLabel = QLabel(title)
        titleLabel.setStyleSheet("font-size: 16px;")
        self.title = title
        hlay1.addWidget(titleLabel, 1)
        mainLayout.addLayout(hlay1)

        self.setLayout(mainLayout)
        self.resize(320, 50)

        ag = QDesktopWidget().availableGeometry()
        sg = QDesktopWidget().screenGeometry()
        widget = self.geometry()
        x = ag.width() - widget.width()
        y = 2 * ag.height() - sg.height() - widget.height()
        self.move(x, y)

        self.setStyleSheet("background-color: {color};".format(color=backcolor))
        self.setWindowTitle("TRADE COPIER - NOTIFICATION")
    
    def hideMyDlg(self):
        global_var.opendDlg = False
        self.hide()

    def closeEvent(self, event):
        self.hide()
        global_var.opendDlg = False
        event.ignore()

