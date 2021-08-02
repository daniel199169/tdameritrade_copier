import xmltodict
def xmlParser(code, xml):
    if xml != '':
        data_dict = xmltodict.parse(xml)
        #print(code)
        #print(data_dict)
        if code == 'OrderEntryRequest':
            data_body = data_dict['OrderEntryRequestMessage']
            orderid = data_body['Order']['OrderKey']
            data = {
                "orderType": data_body['Order']['OrderType'],
                "session": "NORMAL",
                "duration": data_body['Order']['OrderDuration'],
                "orderStrategyType": "SINGLE",
                "price": "",
                "orderLegCollection": [
                    {
                        "instruction": data_body['Order']['OrderInstructions'],
                        "quantity": data_body['Order']['OriginalQuantity'],
                        "instrument": {
                            "symbol": data_body['Order']['Security']['Symbol'],
                            "assetType": "EQUITY"
                        }
                    }
                ]
            }
            if data_body['Order']['OrderPricing']['@xsi:type'] == 'LimitT':
                data['price'] = data_body['Order']['OrderPricing']['Limit']
            return {'id':orderid, 'json':data, 'code':'place_order'}
        elif code == 'UROUT':
            pass
        elif code == 'OrderCancelRequest':
            data_body = data_dict['OrderCancelRequestMessage']
            orderid = data_body['Order']['OrderKey']
            return {'id':orderid, 'code':'cancel_order'}
    return None