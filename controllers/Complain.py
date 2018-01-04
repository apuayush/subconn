from controllers.modules import *
from controllers.utility import *


class ComplainHandler(RequestHandler):
    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, OPTIONS')

    @coroutine
    def post(self):
        token = self.get_argument('token')

        token_from_db = yield db.token.find_one({'token': token})
        if token_from_db is None:
            self.write_error(401, message="unauthorized token")
            return

        item = self.get_argument('item')
        comment = self.get_argument('comment')

        yield db.complaint.insert({'comment': comment, 'item': item})

        self.write({
            'status': 200,
            'message': "complaint registered"
        })

    def write_error(self, status_code, message="Internal Server Error", **kwargs):
        jsonData = {
            'status': int(status_code),
            'message': message
        }
        self.write(json.dumps(jsonData))

    def options(self):
        self.set_status(204)
        self.finish()
