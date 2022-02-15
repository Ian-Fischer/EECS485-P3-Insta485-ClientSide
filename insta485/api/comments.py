"""URLs for comments."""

"""
FLASK RESPONSE CODES! 
bad requests should take form of {'message': 'what was wrong', 'code': flaskcode}
for good requests, I think 200 for return content, 204 for good delete, 201 for create
"""

import sqlite3
import flask
import insta485
from insta485.api.helper import check_authentication

@insta485.app.route('/api/v1/comments/', methods=['POST'])
def make_comment():
    """Make a comment on the specified post."""
    if not check_authentication():
        return flask.jsonify(**{'message': 'Forbidden', 'status_code': 403}), 403
    postid = flask.request.args.get('postid')
    comment = flask.request.json.get('text')
    # connect to db
    connection = insta485.model.get_db()
    connection.row_factory = sqlite3.Row
    # check that the post exists
    post = connection.execute(
        'SELECT P.postid '
        'FROM posts P '
        'WHERE postid = ? ',
        (postid, )
    ).fetchall()
    if len(post) == 0:
         return flask.jsonify(**{'message': 'Not Found', 'status_code': 404}), 404
    # put the comment in
    connection.execute(
        'INSERT INTO comments(owner, postid, text) '
        'VALUES (?,?,?) ',
        (flask.session.get('logname'), postid, comment,)
    )
    connection.commit()
    # get last commentid
    last_commentid = connection.execute(
        'SELECT last_insert_rowid() '
    ).fetchall()
    if len(last_commentid) == 0:
        commentid = 1
    else:
        commentid = last_commentid[0]['last_insert_rowid()']
    text = flask.request.json.get('text')
    # build the response
    context = {
        'owner': flask.session.get('logname'),
        'text': text,
        'commentid': commentid,
        'ownerShowUrl': '/users/{logname}/'.format(logname=flask.session.get('logname')),
        'lognameOwnsThis': True,
        'url': '/api/v1/comments/{cid}/'.format(cid=commentid)
    }
    # return w/ 201
    return flask.jsonify(**context), 201


@insta485.app.route('/api/v1/comments/<commentid>/', methods=['DELETE'])
def delete_comment(commentid):
    """Delete a comment."""
    if not check_authentication():
        return flask.jsonify(**{'message': 'Forbidden', 'status_code': 403}), 403
    # connect to db
    connection = insta485.model.get_db()
    connection.row_factory = sqlite3.Row
    # check ifthe comment exists
    comment = connection.execute(
        'SELECT C.owner '
        'FROM comments C '
        'WHERE C.commentid = ? ',
        (commentid,)
    ).fetchall()

    if len(comment) == 0:
        return flask.jsonify(**{'message': 'Not Found', 'status_code': 404}), 404
    # check if they own the comment
    if comment[0]['owner'] != flask.session.get('logname'):
        return flask.jsonify(**{'message': 'Forbidden', 'status_code': 403}), 403
    # they own the comment, now delete
    connection.execute(
        'DELETE FROM comments '
        'WHERE commentid = ? ',
        (commentid,)
    )
    # commit changes
    connection.commit()
    # return 204
    return flask.jsonify(**{'message': 'No Content', 'status_code': 204 }), 204
