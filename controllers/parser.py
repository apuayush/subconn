from controllers.modules import *
from controllers.utility import *

class AadharAuthentication(RequestHandler):
    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, OPTIONS')

    @coroutine
    def post(self):
        token = self.get_argument('token')

        token_from_db = yield db.token.find_one({'token': token})

        if token_from_db is None:
            self.write_error(401, "unauthorized token")

        else:
            xml_data = self.get_argument('xml_data')
            customer = aadhar_scanner_parser(xml_data)
            agent = {
                'uid': token_from_db['uid'],
                'uname': token_from_db['uid'],

            }

            self.write(json.dumps({**agent, **customer}))

    def write_error(self, status_code, message="Internal Server Error", **kwargs):
        jsonData = {
            'status': int(status_code),
            'message': message
        }
        self.write(json.dumps(jsonData))