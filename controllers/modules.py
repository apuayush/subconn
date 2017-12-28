from tornado.web import RequestHandler, Application, removeslash
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import parse_command_line
from tornado.gen import coroutine

# other libraries
import sys
import jwt
import uuid
import json
import os
import base64
from datetime import datetime
# import env
from motor import MotorClient
import json
from bson import json_util

JWT_SECRET = os.environ['JWT_SECRET']
JWT_ALGORITHM = os.environ['JWT_ALGORITHM']
db = MotorClient(os.environ['DB_LINK'])['subconn']
