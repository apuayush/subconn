from controllers.modules import *


def setToken(user, name):
    """
    setting tokens and saving them on database
    :param user:
    :return:
    """
    now = datetime.now()
    time = now.strftime("%d-%m-%Y %I:%M %p")
    token = jwt.encode({"uid": user, "time": time},
                       JWT_SECRET, JWT_ALGORITHM)

    db.token.insert({"token": token.decode(), "uid": user, "uname": name})

    return token.decode()


def aadhar_scanner_parser(xml_data):

    data = xmltodict.parse(xml_data)
    data = dict(data['PrintLetterBarcodeData'])
    return {'uid':data['@uid'],'uname':data['@name']}


def hash(data):
    data_hash = sha256(json.dumps(data, sort_keys=True).encode('utf-8')).hexdigest()
    return data_hash


@coroutine
def validation(from_id, to_id, items, item_count, gps, token):
    flag = True
    prod = {
        "Rice": 0,
        "Wheat": 0,
        "Oil": 0,
        "Sugar": 0
    }

    status = dict(success=False,
                  message="One or more item not assigned to agent",
                  invalid_list=[],
                  exceeding=prod)

    # Item validation
    print(items)
    for item in items:
        item_db = yield db.items.find_one({'code': item})
        print(item_db)
        assigned_to = int(item_db['assigned_to'])

        if assigned_to != int(from_id):
            status['invalid_list'].append(item)
            flag = False

        item_name = item.split('|')[0]
        prod[item_name] += 1

    if not flag:
        return status
    # update on agent count
    for one in item_count.keys():
        item_count[one] -= prod[one]
        if item_count[one] < 0:
            flag = False

    if flag:
        for item in items:
            item_db = yield db.items.find_one({'code': item})
            last_transaction_id = item_db['transaction_id']
            # send gps and last item transaction id.

            data = {
                "from": from_id,
                "to": to_id,
                'gps': gps,
                'prev_trans': last_transaction_id
            }
            tid = requests.post("http://35.200.142.66:8080/transaction",
                                data=data)
            tid = tid.json()
            yield db.items.update({"code": item},
                                  {"$set":
                                       {'transaction_id': tid['transactionHash'],
                                        "assigned_to": to_id}})

        aadhar_det = yield db.aadhar.find_one({'uid': to_id})
        aadhar_data = aadhar_det['item_count']
        aadhar_items = {
            'Rice': aadhar_data['Rice'] - prod['Rice'],
            'Wheat': aadhar_data['Wheat'] - prod['Wheat'],
            'Oil': aadhar_data['Oil'] - prod['Oil'],
            'Sugar': aadhar_data['Sugar'] - prod['Sugar']
        }
        print(aadhar_items)
        yield db.aadhar.update({'uid': int(to_id)}, {'$set': {'item_count':
                                                                    aadhar_items
                                                                 }})

        agent_det = yield db.agent_details.find_one({'uid': from_id})
        agent_data = agent_det['item_count']
        agent_items = {
            'Rice': agent_data['Rice'] - prod['Rice'],
            'Wheat': agent_data['Wheat'] - prod['Wheat'],
            'Oil': agent_data['Oil'] - prod['Oil'],
            'Sugar': agent_data['Sugar'] - prod['Sugar']
        }

        print(agent_items)
        yield db.agent_details.update({'uid': from_id},{'$set': {
            'item_count': agent_items
        }})
        status['success'] = True
        status["message"] = tid['transactionHash']
        status['invalid_list'] = []

    else:
        for item in items:
            if item_count[item.split('|')[0]] < 0:
                status['invalid_list'].append(item)

        status['success'] = False
        status["message"] = "Exeding item count !!"
        status['exceeding'] = item_count

    return status

def validate(tid):
    flag = 1
    lst = []
    while(tid!=""):
        try:
            cur = db.transactions.find({"transaction_id": tid})[0]
        except IndexError:
            flag = 0
            break
        last = cur['previous_transaction']
        #print "tid : ", tid
        #print "last : ", last
        #print "cur : ", cur['transaction_id']
        data = dumps({"from_id": cur['from_id'], "to_id": cur['to_id'],\
            "transaction_id": cur['last_item_transaction'], "last_transaction": cur['previous_transaction']})
        val = hash(data)
        if val!=tid:
            flag = 0
            break
        tid = last
    return str(flag)

