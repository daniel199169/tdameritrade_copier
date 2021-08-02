import global_var
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, QRect

class MySwitch(QtWidgets.QPushButton):
    def __init__(self, w=132, h=22, r=16, w2=64, t1="ON", t2="OFF", parent = None):
        super().__init__(parent)
        self.r = r
        self.w2 = w2
        self.t1 = t1
        self.t2 = t2
        self.setCheckable(True)
        self.setMinimumWidth(w)
        self.setMinimumHeight(h)

    def paintEvent(self, event):
        label = self.t1 if self.isChecked() else self.t2
        bg_color = QtGui.QColor(global_var.color_blue_arr[0], global_var.color_blue_arr[1], global_var.color_blue_arr[2]) if self.isChecked() else QtGui.QColor(global_var.color_red_arr[0], global_var.color_red_arr[1], global_var.color_red_arr[2])

        radius = self.r
        width = self.w2
        center = self.rect().center()

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.translate(center)
        painter.setBrush(QtGui.QColor(0,0,0))

        pen = QtGui.QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)

        painter.drawRoundedRect(QRect(-width, -radius, 2*width, 2*radius), radius, radius)
        painter.setBrush(QtGui.QBrush(bg_color))
        sw_rect = QRect(-radius, -radius, width + radius, 2*radius)
        if not self.isChecked():
            sw_rect.moveLeft(-width)
        painter.drawRoundedRect(sw_rect, radius, radius)
        if self.isChecked():
            pen = QtGui.QPen(Qt.white)
        else:
            pen = QtGui.QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawText(sw_rect, Qt.AlignCenter, label)