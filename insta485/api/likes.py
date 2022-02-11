"""Handles like endpoints."""
"""
FLASK RESPONSE CODES! 
bad requests should take form of {'message': 'what was wrong', 'code': flaskcode}
for good requests, I think 200 for return content, 204 for good delete, but check spec
"""
import flask
import insta485
from insta485.api.helper import check_authentication


"""
URLs handled in this file.

/api/v1/likes/ , args ?postid=<postid>, POST
/api/v1/likes/<likeid>/, DELETE
"""

@insta485.app.route('/api/v1/likes/', methods=['POST'])
def make_like():
    """Make a like at the specified post."""
    # postid is an arg ?postid=<postid>
    # TODO: what do we do if the argument is not specified?
    # 1. check authentication
    check_authentication()
