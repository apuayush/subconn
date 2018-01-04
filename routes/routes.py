"""
all routes
"""

from controllers import *

routes = [
    (r'/agent/login', Agent.AgentLoginHandler),
    (r'/agent/logout', Agent.LogoutHandler),
    (r'/agent/profile', Agent.ProfileViewer),
    (r'/transaction/aadhar', parser.AadharAuthentication),
    (r'/dash/insert', Dash.InsertTransaction),
    (r'/dash/validate', Dash.ValidateTable),
    (r'/agent/complaint', Complain.ComplainHandler)
]


