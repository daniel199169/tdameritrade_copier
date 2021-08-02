import os
import webbrowser
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QScrollArea, QPushButton, QLineEdit, QGroupBox, QLabel, QMessageBox
import dlgMenu
import dlgLoginUrl
from comSwitch import MySwitch
import connectDB
import global_var

#import websockets.legacy.server
#import websockets.legacy.client
from td.client import TDClient

class HomeWindow(QWidget):
    switch_menu = QtCore.pyqtSignal()
    ctrl_delete_project = 0
    projectmodel = []
    projectLayout = {}
    accountLayout = {}

    def __init__(self):
        super().__init__()
        global_var.opendDlg = True

        self.projectmodel = connectDB.getProject()

        mainLayout = QGridLayout()
        self.createTopToolbar()
        mainLayout.setColumnStretch(0, 1)
        mainLayout.addLayout(self.topLayout, 1, 1)
        
        listBox = QVBoxLayout()
        scroll = QScrollArea()
        listBox.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)
        self.scrollLayout = QVBoxLayout(scrollContent)
        scrollContent.setLayout(self.scrollLayout)
        for x in self.projectmodel:
            self.scrollLayout.addWidget(self.createProjectGroupBox(x['pk'], x['is_allow'], x['users'], "Project "+str(x['vindex']+1)))
        #self.scrollLayout.addStretch(1)
        scroll.setWidget(scrollContent)
        mainLayout.addLayout(listBox, 0, 0, 1, 2)

        self.setLayout(mainLayout)
        self.resize(1366, 768)
        self.setWindowTitle("TRADE COPIER - TRADE ACCOUNT")

    def createTopToolbar(self):
        self.topLayout = QHBoxLayout()
        addAccountBtn = QPushButton("Add Project")
        addAccountBtn.setFixedHeight(32)
        # addAccountBtn.setFixedWidth(160)
        addAccountBtn.setStyleSheet("background-color : {color}; color: #FFF; font-weight: bold; font-size: 18px;".format(color=global_var.color_blue))
        addAccountBtn.clicked.connect(self.createProject)
        self.topLayout.addWidget(addAccountBtn)
        menuBtn = QPushButton("Back")
        menuBtn.setFixedHeight(32)
        # menuBtn.setFixedWidth(160)
        menuBtn.setStyleSheet("background-color : {color}; color: #FFF; font-weight: bold; font-size: 18px;".format(color=global_var.color_grey))
        self.switch_menu.connect(self.toMenu)
        menuBtn.clicked.connect(self.switch_menu.emit)
        self.topLayout.addWidget(menuBtn)
        self.topLayout.addStretch(1)
    
    def createProjectGroupBox(self, pm_proj_id, allow, users, title="Project"):
        newProject = QGroupBox(title)
        newProject.setStyleSheet("color: #FFF; font-weight: bold; font-size: 20px;")
        self.projectLayout[pm_proj_id] = QVBoxLayout()
        btnLayout = QHBoxLayout()
        allowBtn = MySwitch()
        if allow == 1:
            allowBtn.setChecked(True)
        else:
            allowBtn.setChecked(False)
        allowBtn.clicked.connect(lambda: self.changeAllowProject(pm_proj_id, allowBtn.isChecked()))
        delProjBtn = QPushButton("Delete Project")
        delProjBtn.setFixedHeight(32)
        # delProjBtn.setFixedWidth(160)
        delProjBtn.setStyleSheet("background-color : {color}; color: #FFF; font-weight: bold; font-size: 18px;".format(color=global_var.color_red))
        delProjBtn.clicked.connect(lambda: self.deleteProject(pm_proj_id))
        addAccBtn = QPushButton("Add Account")
        addAccBtn.setFixedHeight(32)
        # addAccBtn.setFixedWidth(160)
        addAccBtn.setStyleSheet("background-color : {color}; color: #FFF; font-weight: bold; font-size: 18px;".format(color=global_var.color_blue))
        addAccBtn.clicked.connect(lambda: self.createAccount(pm_proj_id))
        btnLayout.addStretch(1)
        btnLayout.addWidget(allowBtn)
        btnLayout.addWidget(addAccBtn)
        btnLayout.addWidget(delProjBtn)
        self.projectLayout[pm_proj_id].addLayout(btnLayout)
        index = 0
        if len(users) > 0 :
            for x in users:
                if x['is_main'] == 0:
                    index = index + 1
                self.projectLayout[pm_proj_id].addWidget(self.createAccountGroupBox(x, index))
        
        newProject.setLayout(self.projectLayout[pm_proj_id])
        return newProject

    def createAccountGroupBox(self, usermeta, index=1):
        title = "Sub Account"+str(index)
        if usermeta['is_main'] == 1:
            title = "Main Account"
        self.accountLayout[usermeta['id']] = QGroupBox(title)
        self.accountLayout[usermeta['id']].setStyleSheet("color: #FFF; font-weight: bold; font-size: 18px;")
        #newAccount.setCheckable(True)
        #newAccount.setChecked(True)

        nameEdit = QLineEdit(usermeta['acc_name'])
        nameEdit.setFixedHeight(32)
        nameEdit.setStyleSheet("font-size: 18px; color: #000; font-weight: normal;")
        nameEdit.editingFinished.connect(lambda: self.changeUsermeta(nameEdit.text(), 'acc_name', usermeta['id']))
        nameLabel = QLabel("Account Name:")
        nameLabel.setStyleSheet("font-size: 16px;")
        keyEdit = QLineEdit(usermeta['client_id'])
        keyEdit.setFixedHeight(32)
        keyEdit.setStyleSheet("font-size: 18px; color: #000; font-weight: normal;")
        keyEdit.editingFinished.connect(lambda: self.changeUsermeta(keyEdit.text(), 'client_id', usermeta['id']))
        keyLabel = QLabel("Client ID:")
        keyLabel.setStyleSheet("font-size: 16px;")
        balanceEdit = QLineEdit(usermeta['max_balance'])
        balanceEdit.setFixedHeight(32)
        balanceEdit.setStyleSheet("font-size: 18px; color: #000; font-weight: normal;")
        balanceEdit.editingFinished.connect(lambda: self.changeUsermeta(balanceEdit.text(), 'max_balance', usermeta['id']))
        balanceLabel = QLabel("Maximum Balance:")
        balanceLabel.setStyleSheet("font-size: 16px;")
        leverageEdit = QLineEdit(usermeta['leverage'])
        leverageEdit.setFixedHeight(32)
        leverageEdit.setStyleSheet("font-size: 18px; color: #000; font-weight: normal;")
        leverageEdit.editingFinished.connect(lambda: self.changeUsermeta(leverageEdit.text(), 'leverage', usermeta['id']))
        leverageLabel = QLabel("Leverage:")
        leverageLabel.setStyleSheet("font-size: 16px;")
        spreadEdit = QLineEdit(usermeta['spread'])
        spreadEdit.setFixedHeight(32)
        spreadEdit.setStyleSheet("font-size: 18px; color: #000; font-weight: normal;")
        spreadEdit.editingFinished.connect(lambda: self.changeUsermeta(spreadEdit.text(), 'spread', usermeta['id']))
        spreadLabel = QLabel("Spread:")
        spreadLabel.setStyleSheet("font-size: 16px;")
        maxfirstentryEdit = QLineEdit(usermeta['max_first_entry'])
        maxfirstentryEdit.setFixedHeight(32)
        maxfirstentryEdit.setStyleSheet("font-size: 18px; color: #000; font-weight: normal;")
        maxfirstentryEdit.editingFinished.connect(lambda: self.changeUsermeta(maxfirstentryEdit.text(), 'max_first_entry', usermeta['id']))
        maxfirstentryLabel = QLabel("Max First Entry:")
        maxfirstentryLabel.setStyleSheet("font-size: 16px;")
        ctrlBtnLayout = QHBoxLayout()
        allowBtn = MySwitch()
        if usermeta['is_allow'] == 1:
            allowBtn.setChecked(True)
        else:
            allowBtn.setChecked(False)
        allowBtn.clicked.connect(lambda: self.changeAllowAccount(usermeta['id'], allowBtn.isChecked()))
        registerBtn = QPushButton("Register")
        registerBtn.setFixedHeight(32)
        # registerBtn.setFixedWidth(160)
        registerBtn.setStyleSheet("background-color : {color}; color: #FFF; font-weight: bold; font-size: 18px;".format(color=global_var.color_blue))
        registerBtn.clicked.connect(lambda: self.registerAccount(usermeta['id']))
        deleteBtn = QPushButton("Delete Account")
        deleteBtn.setFixedHeight(32)
        # deleteBtn.setFixedWidth(160)
        deleteBtn.setStyleSheet("background-color : {color}; color: #FFF; font-weight: bold; font-size: 18px;".format(color=global_var.color_red))
        deleteBtn.clicked.connect(lambda: self.deleteAccount(usermeta['project_id'], usermeta['id']))
        ctrlBtnLayout.addWidget(allowBtn)
        ctrlBtnLayout.addWidget(registerBtn)
        ctrlBtnLayout.addWidget(deleteBtn)

        layout = QGridLayout()
        layout.addWidget(nameLabel, 0, 0, 1, 1)
        layout.addWidget(nameEdit, 0, 1, 1, 2)
        layout.addWidget(keyLabel, 0, 3, 1, 1)
        layout.addWidget(keyEdit, 0, 4, 1, 4)
        # layout.addWidget(registerBtn, 0, 8, 1, 2)
        # layout.addWidget(deleteBtn, 0, 10, 1, 2)
        layout.addLayout(ctrlBtnLayout, 0, 8, 1, 4)
        layout.addWidget(balanceLabel, 1, 0, 1, 1)
        layout.addWidget(balanceEdit, 1, 1, 1, 2)
        layout.addWidget(leverageLabel, 1, 3, 1, 1)
        layout.addWidget(leverageEdit, 1, 4, 1, 2)
        layout.addWidget(spreadLabel, 1, 6, 1, 1)
        layout.addWidget(spreadEdit, 1, 7, 1, 2)
        layout.addWidget(maxfirstentryLabel, 1, 9, 1, 1)
        layout.addWidget(maxfirstentryEdit, 1, 10, 1, 2)
        self.accountLayout[usermeta['id']].setLayout(layout)
        return self.accountLayout[usermeta['id']]

    def toMenu(self):
        self.tgt = dlgMenu.MenuWindow()
        self.hide()
        self.tgt.show()
    
    def closeEvent(self, event):
        self.hide()
        global_var.opendDlg = False
        event.ignore()

    def createProject(self):
        id = connectDB.createProject()
        userid = connectDB.createUser(id, 1)
        users = [{
            'id':userid,
            'project_id':id,
            'acc_name':'',
            'client_id':'',
            'max_balance':'',
            'leverage':'',
            'spread':'',
            'max_first_entry':'',
            'is_main':1,
            'vindex':0
        }]
        self.projectmodel.append({
            'pk':id,
            'is_allow':1,
            'vindex':len(self.projectmodel),
            'users':users
        })
        self.scrollLayout.addWidget(self.createProjectGroupBox(id, users, "Project "+str(len(self.projectmodel)+1)))

    def changeAllowProject(self, pk, val):
        if val:
            connectDB.updateProject(pk, 'is_allow', 1)
        else:
            connectDB.updateProject(pk, 'is_allow', 0)

    def deleteProject(self, pk):
        self.ctrl_delete_project = pk
        qm = QMessageBox()
        ret = qm.question(self,'', "Are you sure to delete this project?", qm.Yes | qm.No)
        if ret == qm.Yes:
            connectDB.deleteUsersByPrjId(pk)
            connectDB.deleteProject(pk)
            index = 0
            flag = False
            for x in self.projectmodel:
                if x['pk'] == pk:
                    self.scrollLayout.itemAt(index).widget().setParent(None)
                    flag = True
                if flag:
                    x['vindex'] = x['vindex']-1
                index = index + 1
            self.projectmodel = self.projectmodel[:index-1] + self.projectmodel[index+1:]
    

    def createAccount(self, prj_id):
        is_main = 0
        if connectDB.hasMainAccount(prj_id) == None:
            userid = connectDB.createUser(prj_id, 1)
            is_main = 1
        else:
            userid = connectDB.createUser(prj_id, 0)
        user = {
            'id':userid,
            'project_id':prj_id,
            'acc_name':'',
            'client_id':'',
            'max_balance':'',
            'leverage':'',
            'spread':'',
            'max_first_entry':'',
            'is_main':is_main,
            'vindex':0
        }
        index = 0
        for x in self.projectmodel:
            if x['pk'] == prj_id:
                user['vindex'] = len(self.projectmodel[index]['users'])+1
                self.projectmodel[index]['users'].append(user)
                self.projectLayout[prj_id].addWidget(self.createAccountGroupBox(user, user['vindex']))
            index = index + 1
        
    def changeAllowAccount(self, pk, val):
        if val:
            connectDB.updateUser(pk, 'is_allow', 1)
        else:
            connectDB.updateUser(pk, 'is_allow', 0)

    def deleteAccount(self, prj_id, userid):
        index = -1
        k = 0
        for x in self.projectmodel:
            if x['pk'] == prj_id:
                index = k
                break
            k = k + 1
        if index != -1:
            k = 0
            uindex = -1
            for x in self.projectmodel[index]['users']:
                if x['id'] == userid:
                    self.projectmodel[index]['users'] = self.projectmodel[index]['users'][:k-1]+self.projectmodel[index]['users'][k+1:]
                    self.accountLayout[userid].setParent(None)
                    connectDB.deleteUser(userid)
                    uindex = k
                k = k + 1
            if uindex != -1:
                for x in range(uindex, len(self.projectmodel[index]['users'])):
                    self.projectmodel[index]['users'][x]['vindex'] = self.projectmodel[index]['users'][x]['vindex'] - 1

    def changeUsermeta(self, text, column, userid):
        connectDB.updateUser(userid, column, text)
    
    def registerAccount(self, userid):
        global_var.current_login_userid = userid
        user = connectDB.getUser(userid)
        client_id = user['client_id']
        TDSession = TDClient(
            client_id=client_id,
            redirect_uri='http://127.0.0.1:3000',
            credentials_path='./token/'+client_id+'.json'
        )

        if(os.path.isfile(TDSession.credentials_path) and TDSession._silent_sso()):
            TDSession.authstate = True
            QMessageBox.about(self, "Status", "You are registered.")
        else:
            url = TDSession.grab_url()
            webbrowser.get().open(url)
            self.w = dlgLoginUrl.LoginUrlWindow()
            self.w.show()

