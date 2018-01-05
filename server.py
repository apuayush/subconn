from routes import routes
from controllers.modules import *


class ApplicationHandler(Application):
    def __init__(self):
        handlers = routes.routes
        settings = dict(
            debug=True,

        )
        Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    parse_command_line()
    server = HTTPServer(ApplicationHandler())
    server.listen(os.environ.get("PORT", 8000))
    IOLoop.instance().start()
