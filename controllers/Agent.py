from controllers.modules import *
from controllers.utility import *


class AgentLoginHandler(RequestHandler):
    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, OPTIONS')

    @coroutine
    def post(self):
        agent_id = self.get_argument('agent_id')
        password = self.get_argument('password')

        print(type(agent_id), password)
        user = yield db.agent_profile.find_one({'agent_id': int(agent_id)}, {'_id':0})

        print(user)

        if user is None:
            self.write(json.dumps(dict(
                status="403",
                message="Agent_id not registered"
            )
            ))

        elif user['password'] == password :

            jwt_token = setToken(agent_id)

            self.write(json.dumps(dict(
                user="admin",
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

    def write_error(self, status_code, **kwargs):
        jsonData = {
            'status': int(status_code),
            'message': "Internal server error"
        }
        self.write(json.dumps(jsonData))

    def options(self):
        self.set_status(204)
        self.finish()


