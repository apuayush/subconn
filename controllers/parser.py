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

            try:
                to_id = aadhar_scanner_parser(xml_data)
            except:
                self.write_error(400, "Not aadhar")
                to_id = None
                return

            from_id = token_from_db['uid']
            gps_location = self.get_argument('gps')

            customer = yield db.aadhar.find_one({'uid': to_id['uid']})

            if customer == None:
                push_data = {
                    'item_count': {
                        'Rice': 5,
                        'Sugar': 5,
                        'Oil': 5,
                        'Wheat': 5
                    },
                    **to_id
                }
                print(push_data)
                yield db.aadhar.insert(push_data)

            validation(from_id, to_id)






            # self.write(json.dumps({**agent, **customer}))

    def write_error(self, status_code, message="Internal Server Error", **kwargs):
        jsonData = {
            'status': int(status_code),
            'message': message
        }
        self.write(json.dumps(jsonData))

    def options(self):
        self.set_status(204)
        self.finish()
