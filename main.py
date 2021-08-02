import os
import sys
import asyncio
import json
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPalette, QColor
#from PyQt5.QtWidgets import QMessageBox

#from win10toast_click import ToastNotifier
#import concurrent.futures
import threading
from threading import Thread, Event

import dlgMenu
import dlgAlert
import dlgMessage
import catchThread
import connectDB
import global_var

#import websockets.legacy.server
#import websockets.legacy.client
from td.client import TDClient

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    walert = {}
    parent = None
    def __init__(self, icon, parent=None):
        global_var.strike_val = 0
        global_var.event = Event()
        global_var.opendDlg = False
        self.parent = parent

        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtWidgets.QMenu(parent)

        #####################################################################
        self.activated.connect(self.onTrayIconActivated)

        prefs_action = menu.addAction('Open')
        self.setContextMenu(menu)
        prefs_action.triggered.connect(self.openHome)

        """prefs_action = menu.addAction('Test')
        self.setContextMenu(menu)
        prefs_action.triggered.connect(self.onTest)"""

        prefs_action = menu.addAction('Exit')
        self.setContextMenu(menu)
        prefs_action.triggered.connect(self.onExit)
        #####################################################################
        timer = QTimer(self)
        timer.timeout.connect(self.onTimer)
        timer.start(3000)
    
    def onTrayIconActivated(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.DoubleClick:
            self.openHome()

    def openHome(self):
        self.window = dlgMenu.MenuWindow()
        self.window.show()
    
    """def onTest(self):
        self.w = dlgAlert.AlertWindow("Sub 1 [aaa] CALL AAPL", -1, None)
        self.w.show()
    
    def openAlert(self):
        self.w = dlgAlert.AlertWindow()
        self.w.show()"""
    
    def onExit(self):
        global_var.event.set()
        global_var.db_conn.commit()
        # for id, thread in threading._active.items():
        #     print(thread)
        #     print(id)
        #sys.exit()
        os._exit(1)
    
    def onTimer(self):
        """projects = connectDB.getOnlyProjects()
        print(global_var.strike_val)
        for x in projects:
            var = x['price']
            if var == None:
                var = 0
            if global_var.strike_val >= float(var):
                #toast = ToastNotifier()
                #toast.show_toast(title="Notification", msg="Hello, there!", callback_on_click=self.openAlert)
                if global_var.opendDlg == False:
                    global_var.opendDlg = True
                    self.w = dlgAlert.AlertWindow()
                    self.w.show()"""
        #print('&@'*40)
        #print(global_var.tradeCode)
        #print('@#'*40)
        """ to thread """
                    
        logs = connectDB.getMessageLogs()
        index = 1
        for row in logs:
            #print(row)
            if row['is_done'] == 1: # buy/sell request
                data = json.loads(row['order_json'])
                symbol = data['orderLegCollection'][0]['instrument']['symbol']
                dir = data['orderLegCollection'][0]['instruction']
                func_name = 'CALL'
                if dir == 'Sell':
                    func_name = 'PUT'
                self.walert[row['id']] = dlgAlert.AlertWindow("Sub "+str(index)+" ["+row['acc_name']+"] "+func_name+" "+symbol, row['id'], data)
                self.walert[row['id']].show()
            elif row['is_done'] == 3 or row['is_done'] == 6: # token err
                self.walert[row['id']] = dlgMessage.MessageWindow(row['acc_name']+" can not use copier function.\nPlease register now.", global_var.color_err_back)
                self.walert[row['id']].show()
            elif row['is_done'] == 5: # canceled
                data = json.loads(row['order_json'])
                symbol = data['orderLegCollection'][0]['instrument']['symbol']
                dir = data['orderLegCollection'][0]['instruction']
                func_name = 'CALL'
                if dir == 'Sell':
                    func_name = 'PUT'
                self.walert[row['id']] = dlgMessage.MessageWindow(row['acc_name']+" trade order '"+func_name+" "+symbol+"' is canceled", global_var.color_warning_back)
                self.walert[row['id']].show()
            elif row['is_done'] == 7: # cancel failed
                data = json.loads(row['order_json'])
                symbol = data['orderLegCollection'][0]['instrument']['symbol']
                dir = data['orderLegCollection'][0]['instruction']
                func_name = 'CALL'
                if dir == 'Sell':
                    func_name = 'PUT'
                self.walert[row['id']] = dlgMessage.MessageWindow(row['acc_name']+" can not cancel trade order '"+func_name+" "+symbol+"'.\nOrder already is "+row['state'], global_var.color_err_back)
                self.walert[row['id']].show()
            index = index + 1

def startThreadAccAction():
    mainAccounts = connectDB.getMainAccounts()
    for x in mainAccounts:
        client_id = x['client_id']
        TDSession = TDClient(
            client_id=client_id,
            redirect_uri='http://127.0.0.1:3000',
            credentials_path='./token/'+client_id+'.json'
        )
        if(os.path.isfile(TDSession.credentials_path) and TDSession._silent_sso()):
            TDSession.login()
            global_var.TDStreamingDbUserID = x['id']
            global_var.TDStreamingClientID = client_id
            global_var.TDStreamingClient = TDSession.create_streaming_session()
            global_var.TDStreamingClient.account_activity()
            return True
        else:
            return False

async def data_pipeline(event):
    await global_var.TDStreamingClient.build_pipeline()
    while event.is_set() == False:
        data = await global_var.TDStreamingClient.start_pipeline()
        if 'data' in data:
            data2 = data['data'][0]
            if data2['service'] == 'ACCT_ACTIVITY':
                #print(data2)
                global_var.tradeCode.append(data2['content'][0]['2'])
                global_var.tradeXml.append(data2['content'][0]['3'])
                #print(data2['content'][0]['2'])
                #print(data2['content'][0]['3'])

def between_callback(event):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(data_pipeline(event))
    loop.close()



def main(image):
    connectDB.init()

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    qp = QPalette()
    qp.setColor(QPalette.ButtonText, QColor(20, 20, 20))
    qp.setColor(QPalette.WindowText, Qt.white)
    qp.setColor(QPalette.Window, QColor(60, 60, 60))
    qp.setColor(QPalette.Button, Qt.gray)
    app.setPalette(qp)
    w = QtWidgets.QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon(image), w)
    trayIcon.show()

    global_var.tradeCode = []
    global_var.tradeXml = []
    global_var.event = Event()
    t1 = Thread(target=catchThread.catch_thread, args=(global_var.event, ))
    t1.start()
    # t2 = Thread(target=catchThread.copy_trade, args=(global_var.event, ))
    # t2.start()

    if startThreadAccAction():
        t2 = Thread(target=between_callback, args=(global_var.event, ))
        t2.start()
    else:
        #QMessageBox.about(w, "Warning", "Can not use copier function.\nPlease register now.")
        w.walert = dlgMessage.MessageWindow("Can not use copier function.\nPlease register now.", global_var.color_err_back)
        w.walert.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    icon = 'icon.png'
    main(icon)