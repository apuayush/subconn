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
    data = soup(xml_data, "lxml").printletterbarcodedata
    res = {"uname": data['name'], "uid": data['uid'], "district": data['dist'], "state": data['state'],
           "postalcode": data['pc'], "gender": data['gender']}
    return res


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
    for item in items:
        item_db = yield db.items.find_one({'code': item})
        assigned_to = item_db['assigned_to']

        if assigned_to != from_id:
            status['invalid_list'].append(item)
            flag = False

        item_name = item.split('|')[0]
        prod[item_name] += 1

    if not flag:
        return status


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
                "jwt": token,
                'gps': gps,
                'prev_item_transaction': last_transaction_id
            }
            tid = requests.post("http://35.200.142.66:8080/transaction",
                                data=data)
            tid = tid.json()
            print(type(tid))
            yield db.items.update({"code": item},
                                  {"$set":
                                       {'transaction_id': tid['transactionHash'],
                                        "assigned_to": to_id}})

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
