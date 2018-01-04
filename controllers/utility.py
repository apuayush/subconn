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

def validation(from_id, to_id):
    pass