"""Helper functions"""
"""
FLASK RESPONSE CODES! 
bad requests should take form of {'message': 'what was wrong', 'code': flaskcode}
for good requests, I think 200 for return content, 204 for good delete, but check spec
"""


import flask
import insta485

def check_authentication():
    """Function to handle the authentication of the user."""
    # needs to work with session and authen. with http
    print('implement me!')
    # NOTE: return 403 if the credentials don't work out