import sqlite3
import global_var
from os.path import exists
dbName = "store.db"
def init():
    if not exists(dbName):
        global_var.db_conn = sqlite3.connect(dbName)
        global_var.db_cursor = global_var.db_conn.cursor()
        global_var.db_cursor.execute("""
            CREATE TABLE "project" (
                "id"	INTEGER NOT NULL,
                "is_allow"	INTEGER DEFAULT 1,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
        """)

        global_var.db_cursor.execute("""
            CREATE TABLE "account" (
                "id"	INTEGER NOT NULL,
                "project_id"	INTEGER NOT NULL,
                "acc_name"	TEXT,
                "client_id"	TEXT,
                "max_balance"	TEXT,
                "leverage"	TEXT,
                "spread"	TEXT,
                "max_first_entry"	TEXT,
                "is_main"	INTEGER,
                "is_allow"	INTEGER DEFAULT 1,
                FOREIGN KEY("project_id") REFERENCES "project"("id"),
                PRIMARY KEY("id" AUTOINCREMENT)
            );
        """)

        global_var.db_cursor.execute("""
            CREATE TABLE "profit" (
                "id"	INTEGER,
                "profit"	TEXT,
                "price"	TEXT,
                "contract"	TEXT,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
        """)

        global_var.db_cursor.execute("""
            CREATE TABLE "stop_loss" (
                "price"	TEXT,
                "contract"	TEXT,
                "stop_loss"	TEXT
            );
        """)

        global_var.db_cursor.execute("""
            CREATE TABLE "copier_log_main" (
                "id"	INTEGER,
                "main_orderid"	TEXT,
                "main_acc_id"	INTEGER,
                "order_json"	TEXT,
                "state"	TEXT,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
        """)

        global_var.db_cursor.execute("""
            CREATE TABLE "copier_log_sub" (
                "id"	INTEGER,
                "main_id"	INTEGER,
                "sub_orderid"	TEXT,
                "sub_acc_id"	INTEGER,
                "order_json"	TEXT,
                "state"	TEXT,
                "is_done"	INTEGER,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
        """)

        global_var.db_cursor.execute("""
            CREATE TABLE "friday_max" (
                "on_off"	INTEGER DEFAULT 0,
                "max_percent"	TEXT,
                "all_some"	INTEGER DEFAULT 0,
                "accs"	TEXT
            );
        """)

        global_var.db_cursor.execute("""
            CREATE TABLE "notification" (
                "duration"	TEXT
            );
        """)

        # connection.commit()
    else:
        global_var.db_conn = sqlite3.connect(dbName)
        global_var.db_cursor = global_var.db_conn.cursor()

def createProject():
    # connection = sqlite3.connect(dbName)
    # cursor = connection.cursor()
    global_var.db_cursor.execute("INSERT INTO project(title) VALUES ('');")
    ret = global_var.db_cursor.lastrowid
    # connection.commit()
    return ret

def getProject():
    # connection = sqlite3.connect(dbName)
    # cursor = connection.cursor()
    global_var.db_cursor.execute("SELECT * FROM project;")
    rows = global_var.db_cursor.fetchall()
    ret = []
    index = 0
    for row in rows:
        global_var.db_cursor.execute("SELECT * FROM account WHERE project_id={id};".format(id=row[0]))
        users = global_var.db_cursor.fetchall()
        tmp = {
            'pk' : row[0],
            'is_allow' : row[1],
            'vindex' :index,
            'users' : []
        }
        vindex = 0
        for user in users:
            tmpuser = {
                'id':user[0],
                'project_id':user[1],
                'acc_name':user[2],
                'client_id':user[3],
                'max_balance':user[4],
                'leverage':user[5],
                'spread':user[6],
                'max_first_entry':user[7],
                'is_main':user[8],
                'is_allow':user[9],
                'vindex':vindex
            }
            vindex = vindex + 1
            tmp['users'].append(tmpuser)
        index = index + 1
        ret.append(tmp)
    # connection.commit()
    return ret

def getOnlyProjects():
    # connection = sqlite3.connect(dbName)
    # cursor = connection.cursor()
    global_var.db_cursor.execute("SELECT * FROM project;")
    rows = global_var.db_cursor.fetchall()
    ret = []
    for row in rows:
        tmp = {
            'id' : row[0],
            'profit' : row[2],
            'price' : row[3],
            'contract' : row[4]
        }
        ret.append(tmp)
    # connection.commit()
    return ret

def updateProject(id, col, data):
    # connection = sqlite3.connect(dbName)
    # cursor = connection.cursor()
    global_var.db_cursor.execute("UPDATE project SET {col}='{data}' WHERE id={id};".format(col=col,data=data,id=id))
    # connection.commit()

def deleteProject(id):
    # connection = sqlite3.connect(dbName)
    # cursor = connection.cursor()
    global_var.db_cursor.execute("DELETE FROM project WHERE id={id};".format(id=id))
    # connection.commit()

def hasMainAccount(id):
    # connection = sqlite3.connect(dbName)
    # cursor = connection.cursor()
    global_var.db_cursor.execute("SELECT CASE MAX(id) WHEN NULL THEN 0 ELSE MAX(id) END id FROM account WHERE project_id={id} AND is_main=1;".format(id=id))
    row = global_var.db_cursor.fetchone()
    ret = row[0]
    # connection.commit()
    return ret

def createUser(prj_id, is_main):
    # connection = sqlite3.connect(dbName)
    # cursor = connection.cursor()
    global_var.db_cursor.execute("INSERT INTO account(project_id, is_main) VALUES ({id}, {is_main});".format(id=prj_id,is_main=is_main))
    ret = global_var.db_cursor.lastrowid
    # connection.commit()
    return ret

def getUser(userid):
    # connection = sqlite3.connect(dbName)
    # cursor = connection.cursor()
    global_var.db_cursor.execute("SELECT * FROM account WHERE id={id};".format(id=userid))
    row = global_var.db_cursor.fetchone()
    ret = {
        'id':row[0],
        'project_id':row[1],
        'acc_name':row[2],
        'client_id':row[3],
        'max_balance':row[4],
        'leverage':row[5],
        'spread':row[6],
        'max_first_entry':row[7],
        'is_main':row[8],
        'is_allow':row[9]
    }
    # connection.commit()
    return ret

def getMainAccounts():
    # connection = sqlite3.connect(dbName)
    # cursor = connection.cursor()
    global_var.db_cursor.execute("SELECT * FROM account WHERE is_main=1;")
    rows = global_var.db_cursor.fetchall()
    ret = []
    for row in rows:
        tmp = {
            'id':row[0],
            'project_id':row[1],
            'acc_name':row[2],
            'client_id':row[3],
            'max_balance':row[4],
            'leverage':row[5],
            'spread':row[6],
            'max_first_entry':row[7],
            'is_main':row[8],
            'is_allow':row[9]
        }
        ret.append(tmp)
    # connection.commit()
    return ret

def getToTradeAccounts(client_id):
    # connection = sqlite3.connect(dbName)
    # cursor = connection.cursor()
    global_var.db_cursor.execute("SELECT * FROM account WHERE is_main=1 AND client_id='{client_id}' AND is_allow=1;".format(client_id=client_id))
    rows = global_var.db_cursor.fetchall()
    ret = []
    for row in rows:
        tmp = {
            'id':row[0],
            'project_id':row[1],
            'acc_name':row[2],
            'client_id':row[3],
            'max_balance':row[4],
            'leverage':float(row[5]),
            'spread':row[6],
            'max_first_entry':row[7]
        }
        ret.append(tmp)
    # connection.commit()
    return _getTradeAccounts(ret, [])

def _getTradeAccounts(cond, ret):
    # connection = sqlite3.connect(dbName)
    # cursor = connection.cursor()
    cur_step = []
    for x in cond:
        global_var.db_cursor.execute("SELECT * FROM account WHERE is_main=1 AND client_id='{client_id}' AND is_allow=1;".format(client_id=x['client_id']))
        projects = global_var.db_cursor.fetchall()
        for project in projects:
            global_var.db_cursor.execute("SELECT * FROM account WHERE is_main=0 AND project_id='{project_id}' AND is_allow=1;".format(project_id=project[1]))
            rows = global_var.db_cursor.fetchall()
            for row in rows:
                cur_step.append({
                    'id':row[0],
                    'project_id':row[1],
                    'acc_name':row[2],
                    'client_id':row[3],
                    'max_balance':row[4],
                    'leverage':float(row[5])*x['leverage'],
                    'spread':row[6],
                    'max_first_entry':row[7]
                })
    # connection.commit()
    if len(cur_step) > 0:
        ret = ret + cur_step
        return _getTradeAccounts(cur_step, ret)
    else:
        return ret
    

def getSubUsers():
    # connection = sqlite3.connect(dbName)
    # cursor = connection.cursor()
    global_var.db_cursor.execute("SELECT * FROM account WHERE is_main=0;")
    rows = global_var.db_cursor.fetchall()
    ret = []
    for row in rows:
        tmp = {
            'id':row[0],
            'project_id':row[1],
            'acc_name':row[2],
            'client_id':row[3],
            'max_balance':row[4],
            'leverage':row[5],
            'spread':row[6],
            'max_first_entry':row[7],
            'is_main':row[8],
            'is_allow':row[9]
        }
        ret.append(tmp)
    # connection.commit()
    return ret

def updateUser(userid, column, data):
    # connection = sqlite3.connect(dbName)
    # cursor = connection.cursor()
    global_var.db_cursor.execute("UPDATE account SET {column}='{data}' WHERE id={userid};".format(column=column,data=data,userid=userid))
    # connection.commit()

def deleteUsersByPrjId(id):
    # connection = sqlite3.connect(dbName)
    # cursor = connection.cursor()
    global_var.db_cursor.execute("DELETE FROM account WHERE project_id={id};".format(id=id))
    # connection.commit()

def deleteUser(id):
    # connection = sqlite3.connect(dbName)
    # cursor = connection.cursor()
    global_var.db_cursor.execute("DELETE FROM account WHERE id={id};".format(id=id))
    # connection.commit()

def createProfit():
    # connection = sqlite3.connect(dbName)
    # cursor = connection.cursor()
    global_var.db_cursor.execute("INSERT INTO profit(profit, price, contract) VALUES ('', '', '');")
    ret = global_var.db_cursor.lastrowid
    # connection.commit()
    return ret

def getProfit():
    # connection = sqlite3.connect(dbName)
    # cursor = connection.cursor()
    global_var.db_cursor.execute("SELECT * FROM profit;")
    rows = global_var.db_cursor.fetchall()
    ret = []
    for row in rows:
        tmp = {
            'id' : row[0],
            'profit' : row[1],
            'price' : row[2],
            'contract' : row[3]
        }
        ret.append(tmp)
    # connection.commit()
    return ret

def validateProfit():
    # connection = sqlite3.connect(dbName)
    # cursor = connection.cursor()
    global_var.db_cursor.execute("SELECT * FROM profit WHERE profit != '' AND price == '' AND contract == '';")
    rows = global_var.db_cursor.fetchall()
    ret = []
    for row in rows:
        tmp = {
            'id' : row[0],
            'profit' : row[1],
            'price' : row[2],
            'contract' : row[3]
        }
        ret.append(tmp)
    # connection.commit()
    return ret

def updateProfit(userid, column, data):
    # connection = sqlite3.connect(dbName)
    # cursor = connection.cursor()
    global_var.db_cursor.execute("UPDATE profit SET {column}='{data}' WHERE id={userid};".format(column=column,data=data,userid=userid))
    # connection.commit()

def deleteProfit(id):
    # connection = sqlite3.connect(dbName)
    # cursor = connection.cursor()
    global_var.db_cursor.execute("DELETE FROM profit WHERE id={id};".format(id=id))
    # connection.commit()

def getStopLoss():
    # connection = sqlite3.connect(dbName)
    # cursor = connection.cursor()
    global_var.db_cursor.execute("SELECT COUNT(*) FROM stop_loss;")
    row = global_var.db_cursor.fetchone()
    if row[0] == 0:
        global_var.db_cursor.execute("INSERT INTO stop_loss(price) VALUES ('');")
    global_var.db_cursor.execute("SELECT * FROM stop_loss;")
    row = global_var.db_cursor.fetchone()
    ret = {
        'price' : str(row[0]),
        'contract' : str(row[1]),
        'stop_loss' : str(row[2])
    }
    # connection.commit()
    return ret

def updateStopLoss(col, data):
    # connection = sqlite3.connect(dbName)
    # cursor = connection.cursor()
    global_var.db_cursor.execute("SELECT COUNT(*) FROM stop_loss;")
    row = global_var.db_cursor.fetchone()
    if row[0] == 0:
        global_var.db_cursor.execute("INSERT INTO stop_loss({col}) VALUES ('{data}');".format(col=col,data=data))
    else:
        global_var.db_cursor.execute("UPDATE stop_loss SET {col}='{data}';".format(col=col,data=data))
    # connection.commit()

def createMainLog(orderid, accid, json, state='WORKING'):
    # connection = sqlite3.connect(dbName)
    # cursor = connection.cursor()
    global_var.db_cursor.execute("INSERT INTO copier_log_main(main_orderid, main_acc_id, order_json, state) VALUES ('{orderid}', {accid}, '{json}', '{state}');".format(orderid=orderid,accid=accid,json=json,state=state))
    ret = global_var.db_cursor.lastrowid
    # connection.commit()
    return ret

def getMainOrder(id):
    # connection = sqlite3.connect(dbName)
    # cursor = connection.cursor()
    global_var.db_cursor.execute("SELECT * FROM copier_log_main WHERE main_orderid={id};".format(id=id))
    row = global_var.db_cursor.fetchone()
    ret = {
        'id':row[0],
        'main_orderid':row[1],
        'main_acc_id':row[2],
        'order_json':row[3],
        'state':row[4]
    }
    # connection.commit()
    return ret

def createSubLog(main_id, orderid, accid, json, state='WORKING', is_done=0):
    # connection = sqlite3.connect(dbName)
    # cursor = connection.cursor()
    global_var.db_cursor.execute("INSERT INTO copier_log_sub(main_id, sub_orderid, sub_acc_id, order_json, state, is_done) VALUES ({main_id}, '{orderid}', {accid}, '{json}', '{state}', {is_done});".format(main_id=main_id,orderid=orderid,accid=accid,json=json,state=state,is_done=is_done))
    ret = global_var.db_cursor.lastrowid
    # connection.commit()
    return ret

def getSubOrder(id):
    # connection = sqlite3.connect(dbName)
    # cursor = connection.cursor()
    global_var.db_cursor.execute("SELECT * FROM copier_log_sub WHERE id={id};".format(id=id))
    row = global_var.db_cursor.fetchone()
    ret = {
        'id':row[0],
        'main_id':row[1],
        'sub_orderid':row[2],
        'sub_acc_id':row[3],
        'order_json':row[4],
        'state':row[5],
        'is_done':row[6]
    }
    # connection.commit()
    return ret

def getSubOrdersByMainID(id):
    # connection = sqlite3.connect(dbName)
    # cursor = connection.cursor()
    global_var.db_cursor.execute("SELECT xx.*, yy.client_id FROM copier_log_sub xx LEFT JOIN account yy ON xx.sub_acc_id=yy.id WHERE main_id={id} AND (is_done=1 OR is_done=2);".format(id=id))
    rows = global_var.db_cursor.fetchall()
    ret = []
    for row in rows:
        tmp = {
            'id':row[0],
            'main_id':row[1],
            'sub_orderid':row[2],
            'sub_acc_id':row[3],
            'order_json':row[4],
            'state':row[5],
            'is_done':row[6],
            'client_id':row[7]
        }
        ret.append(tmp)
    # connection.commit()
    return ret

def updateSubLog(id, col, data):
    # connection = sqlite3.connect(dbName)
    # cursor = connection.cursor()
    global_var.db_cursor.execute("UPDATE copier_log_sub SET {col}='{data}' WHERE id={id};".format(col=col,data=data,id=id))
    # connection.commit()

def getMessageLogs():
    # connection = sqlite3.connect(dbName)
    # cursor = connection.cursor()
    global_var.db_cursor.execute("SELECT xx.*, yy.acc_name FROM copier_log_sub xx LEFT JOIN account yy ON xx.sub_acc_id=yy.id WHERE is_done IN (1,3,5,6,7);")
    rows = global_var.db_cursor.fetchall()
    ret = []
    for row in rows:
        tmp = {
            'id':row[0],
            'main_id':row[1],
            'sub_orderid':row[2],
            'sub_acc_id':row[3],
            'order_json':row[4],
            'state':row[5],
            'is_done':row[6],
            'acc_name':row[7]
        }
        ret.append(tmp)
    global_var.db_cursor.execute("UPDATE copier_log_sub SET is_done=2 WHERE is_done=1;")
    global_var.db_cursor.execute("UPDATE copier_log_sub SET is_done=4 WHERE is_done=3;")
    global_var.db_cursor.execute("UPDATE copier_log_sub SET is_done=8 WHERE is_done=5;")
    global_var.db_cursor.execute("UPDATE copier_log_sub SET is_done=9 WHERE is_done=6;")
    global_var.db_cursor.execute("UPDATE copier_log_sub SET is_done=10 WHERE is_done=7;")
    # connection.commit()
    return ret

def getNotification():
    # connection = sqlite3.connect(dbName)
    # cursor = connection.cursor()
    global_var.db_cursor.execute("SELECT COUNT(*) FROM notification;")
    row = global_var.db_cursor.fetchone()
    if row[0] == 0:
        global_var.db_cursor.execute("INSERT INTO notification(duration) VALUES ('');")
    global_var.db_cursor.execute("SELECT * FROM notification;")
    row = global_var.db_cursor.fetchone()
    ret = {
        'duration' : str(row[0])
    }
    # connection.commit()
    return ret

def updateNotification(col, data):
    # connection = sqlite3.connect(dbName)
    # cursor = connection.cursor()
    global_var.db_cursor.execute("SELECT COUNT(*) FROM notification;")
    row = global_var.db_cursor.fetchone()
    if row[0] == 0:
        global_var.db_cursor.execute("INSERT INTO notification({col}) VALUES ('{data}');".format(col=col,data=data))
    else:
        global_var.db_cursor.execute("UPDATE notification SET {col}='{data}';".format(col=col,data=data))
    # connection.commit()
    
def getFridayMax():
    # connection = sqlite3.connect(dbName)
    # cursor = connection.cursor()
    global_var.db_cursor.execute("SELECT COUNT(*) FROM friday_max;")
    row = global_var.db_cursor.fetchone()
    if row[0] == 0:
        global_var.db_cursor.execute("INSERT INTO friday_max(on_off) VALUES (0);")
    global_var.db_cursor.execute("SELECT * FROM friday_max;")
    row = global_var.db_cursor.fetchone()
    ret = {
        'on_off' : row[0],
        'max_percent' : str(row[1]),
        'all_some' : row[2],
        'accs' : str(row[3])
    }
    # connection.commit()
    return ret

def updateFridayMax(col, data):
    # connection = sqlite3.connect(dbName)
    # cursor = connection.cursor()
    global_var.db_cursor.execute("SELECT COUNT(*) FROM friday_max;")
    row = global_var.db_cursor.fetchone()
    if row[0] == 0:
        global_var.db_cursor.execute("INSERT INTO friday_max({col}) VALUES ('{data}');".format(col=col,data=data))
    else:
        global_var.db_cursor.execute("UPDATE friday_max SET {col}='{data}';".format(col=col,data=data))
    # connection.commit()