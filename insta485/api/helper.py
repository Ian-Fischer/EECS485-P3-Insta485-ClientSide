"""Helper functions"""
"""
FLASK RESPONSE CODES! 
bad requests should take form of {'message': 'what was wrong', 'code': flaskcode}
for good requests, I think 200 for return content, 204 for good delete, but check spec
"""


import flask
import insta485

def verify_user(username, password):
    """Takes the given username and password and verifies."""
    print('implement me')

def check_authentication():
    """Function to handle the authentication of the user."""
    # get flask session stuff
    session_username = flask.request.form.get('username')
    session_password = flask.request.form.get('password')
    if session_username and session_password:
        # do flask stuff
        print('implement me')

    # get http basic authentification stuff
    http_username = flask.request.authorization.get('username')
    http_password = flask.request.authorization.get('password')
    if http_username and http_password:
        # do http stuff
        print('implement me')
    
