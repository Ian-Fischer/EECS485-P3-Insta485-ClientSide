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
    check_authentication()
    postid = flask.request.args.get('postid')
    if not postid:
        return flask.jsonify(**{'message': 'not found'}), 404
    # db connection
    connection = insta485.model.get_db()
    connection.row_factory = sqlite3.Row
    # check if logname already liked
    liked = connection.execute(
        ''
    )
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
    check_authentication()
    if not likeid:
        return flask.jsonify(**{'message': 'not found'}), 404
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
        return flask.jsonify(**{'message': 'not found'}), 404
    # check if they own the like
    if flask.session.get('logname') != like[0]['owner']:
        return flask.jsonify(**{'message': 'you do not own this!'}), 403
    # if it exists and they own it, delete it
    connection.execute(
        'DELETE FROM likes '
        'WHERE likeid = ? ',
        (likeid,)
    )
    # commit changes
    connection.commit()
    return flask.jsonify(**{'message': 'NO CONTENT'}), 204
