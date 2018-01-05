from controllers.modules import *
from controllers.utility import *


class AadharAuthentication(RequestHandler):
    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, OPTIONS')

    @coroutine
    def post(self):
        req = self.get_argument('req')
        req = json.loads(req)
        token = req['token']

        token_from_db = yield db.token.find_one({'token': token})

        if token_from_db is None:
            self.write_error(401, message="unauthorized token")

        else:
            # request parameters
            xml_data = req['xml_data']
            items_req = req['items']
            gps = req['gps']

            to_id = aadhar_scanner_parser(xml_data)

            print(to_id)

            if to_id == None:
                self.write_error("400", message="Not aadhar")
                return

            from_id = int(token_from_db['uid'])
            customer = yield db.aadhar.find_one({'uid': int(to_id['uid'])})

            if customer == None:
                customer = {
                    'item_count': {
                        'Rice': 5,
                        'Sugar': 5,
                        'Oil': 5,
                        'Wheat': 5
                    },
                    **to_id
                }
                yield db.aadhar.insert(customer)
            print(items_req)
            # items_req = ''.join(items_req.split())
            # items_req = items_req[1:-1].replace(r'"', "").split(',')

            print(items_req)
            status = yield validation(int(from_id), int(to_id['uid']), items_req, customer['item_count'], gps, token)
            print(status)
            self.write(status)

    def write_error(self, status_code, message="Internal Server Error", **kwargs):
        jsonData = {
            'status': 400,
            'message': message
        }
        self.write(json.dumps(jsonData))

    def options(self):
        self.set_status(204)
        self.finish()
