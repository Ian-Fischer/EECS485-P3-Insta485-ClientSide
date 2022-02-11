"""Handles like endpoints."""
"""
FLASK RESPONSE CODES! 
bad requests should take form of {'message': 'what was wrong', 'code': flaskcode}
for good requests, I think 200 for return content, 204 for good delete, but check spec
"""
import sqlite3
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
    # 1. check authentication
    check_authentication()
    postid = flask.request.args.get('postid')
    if not postid:
        # FIXME: i don't know what the correct response code is
        # FIXME: or what to do if an arg is not specified
        return flask.jsonify(**{'message': 'not found'}), 404
    # db connection
    connection = insta485.model.get_db()
    connection.row_factory = sqlite3.Row
    # insert like into table
    connection.execute (
        'INSERT into likes(owner, postid) '
        'VALUES (?,?) ',
        (flask.session.get('logname'), postid,)
    )
    # commit changes
    connection.commit()
    context = {
        'likeid': postid,
        'url': f'/api/v1/likes/{postid}/'
    }
    return flask.jsonify(**context), 200

@insta485.app.route('/api/v1/likes/', methods=['DELETE'])
def delete_like():
    """Delete a like on specified post."""
    check_authentication()
    postid = flask.request.args.get('postid')
    if not postid:
        # FIXME: what to do if an arg is not specified
        return flask.jsonify(**{'message': 'not found'}), 404
