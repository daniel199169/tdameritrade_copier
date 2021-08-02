import os
import requests, json
from time import sleep
from threading import Thread

import global_var
import dataConverter
import connectDB

from td.client import TDClient

def catch_thread(event):
    cnt = 0
    while event.is_set() == False:
        # td_consumer_key = 'UGPAX5IGKEO3JRPGAEQMS4CCNH4I6GPC'
        # base_url = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/quotes?'
        # endpoint = base_url.format(stock_ticker = 'AAPL')
        # page = requests.get(url=endpoint,
        #                     params={'apikey' : td_consumer_key})
        # if page.status_code == 200:
        #     content = json.loads(page.content)
        #     val = content['AAPL']['mark']
        #     global_var.strike_val = val
        # else:
        #     pass
        cnt = cnt + 1
        if cnt > 2:
            cnt = 0
        # print(cnt)
        # print('catching')
        sleep(2)



def makeOrder(db_id):
    print('make_order')
    log = connectDB.getSubOrder(db_id)
    row = connectDB.getUser(log['sub_acc_id'])
    data = json.loads(log['order_json'])
    client_id = row['client_id']
    print('**makeorder**'*5)
    print(client_id)
    print('**makeorder**'*5)
    TDSession = TDClient(
        client_id=client_id,
        redirect_uri='http://127.0.0.1:3000',
        credentials_path='./token/'+client_id+'.json'
    )
    #print('*'*90)
    #print(db_id)
    #print(client_id)
    #print(os.path.isfile(TDSession.credentials_path))
    #print(TDSession._silent_sso())
    #print('&'*90)
    if(os.path.isfile(TDSession.credentials_path) and TDSession._silent_sso()):
        TDSession.login()
        accmeta = TDSession.get_accounts()
        callback = TDSession.place_order(account=accmeta[0]['securitiesAccount']['accountId'], order=data)
        connectDB.updateSubLog(db_id, 'sub_orderid', callback['order_id'])
        connectDB.updateSubLog(db_id, 'is_done', 1)
    else:
        connectDB.updateSubLog(db_id, 'is_done', 3)

def cancelOrder(json_data):
    print('cancel_order')
    client_id = json_data['client_id']
    TDSession = TDClient(
        client_id=client_id,
        redirect_uri='http://127.0.0.1:3000',
        credentials_path='./token/'+client_id+'.json'
    )
    if(os.path.isfile(TDSession.credentials_path) and TDSession._silent_sso()):
        TDSession.login()
        accmeta = TDSession.get_accounts()
        callback = TDSession.get_orders(account=accmeta[0]['securitiesAccount']['accountId'], order_id=json_data['sub_orderid'])
        if callback['status'] == 'QUEUED' or callback['status'] == 'WORKING':
            TDSession.cancel_order(account=accmeta[0]['securitiesAccount']['accountId'], order_id=json_data['sub_orderid'])
            connectDB.updateSubLog(json_data['id'], 'is_done', 5)
            connectDB.updateSubLog(json_data['id'], 'state', 'CANCELED')
        else:
            connectDB.updateSubLog(json_data['id'], 'is_done', 7)
            connectDB.updateSubLog(json_data['id'], 'state', callback['status'])
    else:
        connectDB.updateSubLog(json_data['id'], 'is_done', 6)
    
def copy_trade(event):
    while event.is_set() == False:
        if len(global_var.tradeCode) > 0:
            print(global_var.tradeCode)
            data = dataConverter.xmlParser(global_var.tradeCode.pop(), global_var.tradeXml.pop())
            if data != None:
                if data['code'] == 'place_order':
                    global_var.tadeJson = data['json']
                    main_log_id = connectDB.createMainLog(data['id'], global_var.TDStreamingDbUserID, json.dumps(data['json']))

                    rows = connectDB.getToTradeAccounts(global_var.TDStreamingClientID)
                    for row in rows:
                        tmp = data['json']
                        #print(tmp)
                        #tmp['orderLegCollection'][0]['quantity'] = str(float(tmp['orderLegCollection'][0]['quantity']) * row['leverage'])
                        sub_log_id = connectDB.createSubLog(main_log_id, '', row['id'], json.dumps(tmp))
                        tmp_thread = Thread(target=makeOrder, args=(sub_log_id, ))
                        tmp_thread.start()
                elif data['code'] == 'cancel_order':
                    main_order = connectDB.getMainOrder(data['id'])
                    suborders = connectDB.getSubOrdersByMainID(main_order['id'])
                    for suborder in suborders:
                        tmp_thread = Thread(target=cancelOrder, args=(suborder, ))
                        tmp_thread.start()
                    #print(data)
                    #print(main_order)