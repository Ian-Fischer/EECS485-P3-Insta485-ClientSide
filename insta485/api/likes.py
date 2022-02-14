"""Handles like endpoints."""
"""
URLs handled in this file:
/api/v1/likes/, args ?postid=<postid>, POST
/api/v1/likes/<likeid>/, DELETE
"""
import sqlite3
import flask
import insta485
from insta485.api.helper import check_authentication


@insta485.app.route('/api/v1/likes/', methods=['POST'])
def make_like():
    """Make a like at the specified post."""
    # postid is an arg ?postid=<postid>
    # 1. check authentication
    if not check_authentication():
        return flask.jsonify(**{'message': 'Forbidden', 'status_code': 403}), 403
    postid = flask.request.args.get('postid')
    if not postid:
        return flask.jsonify(**{'message': 'Not Found', 'status_code': 404}), 404
    # db connection
    connection = insta485.model.get_db()
    connection.row_factory = sqlite3.Row
    # check if logname already liked
    liked = connection.execute(
        'SELECT L.likeid '
        'FROM likes L '
        'WHERE L.owner = ? AND L.postid = ? ',
        (flask.session.get('logname'), postid,)
    ).fetchall()
    if len(liked) == 1:
        output = {
            'likeid': liked[0]['likeid'],
            'url': f'/api/v1/likes/{liked[0]["likeid"]}/'
        }
        return flask.jsonify(**output), 200
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
    return flask.jsonify(**context), 201


@insta485.app.route('/api/v1/likes/<likeid>/', methods=['DELETE'])
def delete_like(likeid):
    """Delete a like on specified post."""
    if not check_authentication():
        return flask.jsonify(**{'message': 'Forbidden', 'status_code': 403}), 403
    # FIXME: should this be here?
    if not likeid:
        return flask.jsonify(**{'message': 'Not Found', 'status_code': 404}), 404
    # connect to db
    connection = insta485.model.get_db()
    # get the like they are requesting
    like = connection.execute(
        'SELECT L.owner '
        'FROM likes L '
        'WHERE L.likeid = ? ',
        (likeid,)
    ).fetchall()
    # check if the like exists
    if len(like) != 1:
        return flask.jsonify(**{'message': 'Not Found', 'status_code': 404}), 404
    # check if they own the like
    if flask.session.get('logname') != like[0]['owner']:
        return flask.jsonify(**{'message': 'Forbidden', 'status_code': 403}), 403
    # if it exists and they own it, delete it
    connection.execute(
        'DELETE FROM likes '
        'WHERE likeid = ? ',
        (likeid,)
    )
    # commit changes
    connection.commit()
    return flask.jsonify(**{'message': 'No Content', 'status_code': 204}), 204
