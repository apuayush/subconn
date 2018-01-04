from controllers.modules import *
from controllers.utility import *


class InsertTransaction(RequestHandler):
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
            return

        from_id = token_from_db['uid']
        to_id = self.get_argument('to_id')
        items = self.get_argument('items')

        last_transaction_id = yield db.last_transaction.find_one()
        last_transaction_id = last_transaction_id['last_transaction_id']
        print(last_transaction_id)

        data = {
            "from_id": from_id,
            "to_id": to_id,
            "transaction_id": transaction_id,
            "last_transaction_id": last_transaction_id
        }

        data_hash = hash_function(data)
        db.transactions.insert({"from_id": data['from_id'], "to_id": data['to_id'], \
                                "last_item_transaction": data['transaction_id'], "transaction_id": data_hash,
                                "previous_transaction": last_transaction_id})
        last_transaction_id = data_hash
        yield update_last_transaction_id(last_transaction_id)
        self.write(last_transaction_id)

    def write_error(self, status_code, message="Internal Server Error", **kwargs):
        jsonData = {
            'status': int(status_code),
            'message': message
        }
        self.write(json.dumps(jsonData))

    def options(self):
        self.set_status(204)
        self.finish()


class ValidateTable(RequestHandler):
    pass