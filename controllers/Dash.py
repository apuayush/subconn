from controllers.modules import *
from controllers.utility import *


class InsertTransaction(RequestHandler):
    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, OPTIONS')

    @coroutine
    def post(self):
        from_id = self.get_argument('from_id')
        to_id = self.get_argument('to_id')
        transaction_id = self.get_argument('transaction_id')

        last_transaction_id = yield db.last_transaction.find_one()
        last_transaction_id = last_transaction_id['last_transaction_id']
        print(last_transaction_id)

        data = {
            "from_id": from_id,
            "to_id": to_id,
            "transaction_id": transaction_id,
            "last_transaction_id":last_transaction_id
        }

        data_hash = hash_function(data)
        db.transactions.insert({"from_id": data['from_id'], "to_id": data['to_id'], \
                                "last_item_transaction": data['transaction_id'], "transaction_id": data_hash,
                                "previous_transaction": last_transaction_id})
        last_transaction_id = data_hash
        yield update_last_transaction_id(last_transaction_id)

