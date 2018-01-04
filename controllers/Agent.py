from controllers.modules import *
from controllers.utility import *


class AgentLoginHandler(RequestHandler):
    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, OPTIONS')

    @coroutine
    def post(self):
        uid = self.get_argument('uid')
        password = self.get_argument('password')

        agent = yield db.agent_details.find_one({'uid': int(uid)}, {'_id': 0})

        if agent is None:
            self.write(json.dumps(dict(
                status="403",
                message="Agent_id not registered"
            )
            ))

        elif agent['password'] == password:

            jwt_token = setToken(uid, agent['uname'])

            self.write(json.dumps(dict(
                uid=agent['uid'],
                uname=agent['uname'],
                token=jwt_token,
                status="200",
                message="authenticated"
            )
            ))

        else:
            self.write(json.dumps(dict(
                status="403",
                message="invalid password"
            )
            ))

    def write_error(self, status_code, message="Internal Server Error", **kwargs):
        jsonData = {
            'status': int(status_code),
            'message': message
        }
        self.write(json.dumps(jsonData))

    def options(self):
        self.set_status(204)
        self.finish()


class ProfileViewer(RequestHandler):
    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header('Access-Control-Allow-Methods', ' POST, OPTIONS')

    @coroutine
    def post(self):
        token = self.get_argument('token')

        token_from_db = yield db.token.find_one({'token': token})
        if token_from_db is None:
            self.write_error(401, "unauthorized token")

        else:
            profile = yield db.agent_details.find_one({'uid': int(token_from_db['uid'])}, {'_id': 0})
            json_data = {
                'uname': profile['uname'],
                'uid': profile['uid'],
                'itemcount': profile['item_count']
            }

            self.write(json.dumps(json_data))

    def write_error(self, status_code, message="Internal Server Error", **kwargs):
        jsonData = {
            'status': int(status_code),
            'message': message
        }
        self.write(json.dumps(jsonData))

    def options(self):
        self.set_status(204)
        self.finish()


class LogoutHandler(RequestHandler):
    """
    method = POST
    route : /logout
    parameter : token
    """
    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header('Access-Control-Allow-Methods', ' POST, OPTIONS')

    @coroutine
    def post(self):
        token = self.get_argument("token")

        db.token.remove({"token": token})
        self.write({"status": 200, "msg": "successful"})

    def options(self):
        self.set_status(204)
