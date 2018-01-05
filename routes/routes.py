"""
all routes
"""

from controllers import *

routes = [
    (r'/agent/login', Agent.AgentLoginHandler),
    (r'/agent/logout', Agent.LogoutHandler),
    (r'/agent/profile', Agent.ProfileViewer),
    (r'/transaction/aadhar', parser.AadharAuthentication),
    (r'/agent/complaint', Complain.ComplainHandler)
]


