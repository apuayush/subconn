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
    res = {"name": data['name'], "uid": data['uid'], "district": data['dist'], "state": data['state'],
           "postalcode": data['pc'], "gender": data['gender']}
    return res

