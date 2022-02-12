"""URLs for comments."""

"""
FLASK RESPONSE CODES! 
bad requests should take form of {'message': 'what was wrong', 'code': flaskcode}
for good requests, I think 200 for return content, 204 for good delete, but check spec
"""

import sqlite3
import flask
import insta485
from helper import check_authentication

@insta485.app.route('/api/v1/comments/', methods=['POST'])
def make_comment():
    """Make a comment on the specified post."""
    check_authentication()
    postid = flask.request.args['postid']
    # connect to db
    connection = insta485.model.get_db()
    connection.row_factory = sqlite3.Row
    # get last commentid
    last_commentid = connection.execute(
        'SELECT last_insert_rowid() '
        'FROM comments '
    ).fetchall()
    if len(last_commentid) == 0:
        commentid = 1
    else:
        commentid = last_commentid[0]['last_insert_rowid()']
    


@insta485.app.route('/api/v1/comments/<commentid>/', method=['DELETE'])
def delete_comment():
    """Delete a comment."""
    # NOTE: if the commentid does not exist, return flask.abort(404)
    # NOTE: if the comment owner is not the logname, return flask.abort(403)
    check_authentication()
    commentid = flask.request.args['commentid']
