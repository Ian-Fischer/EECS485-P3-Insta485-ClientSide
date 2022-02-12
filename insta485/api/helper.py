"""Helper functions."""

"""
FLASK RESPONSE CODES! 
bad requests should take form of {'message': 'what was wrong', 'code': flaskcode}
for good requests, I think 200 for return content, 204 for good delete, but check spec

ex: return flask.jsonify(**response_dict), CODE
"""


import flask
import insta485
import sqlite3
import hashlib
import uuid
import pathlib

def get_file_path(filename):
    """Get uuid file path."""
    stem = uuid.uuid4().hex
    suffix = pathlib.Path(filename).suffix
    uuid_basename = f"{stem}{suffix}"
    # Save to disk
    path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
    return path, uuid_basename


def get_salt(password):
    """Get the salt from the password in the database."""
    idx = password.find('$')
    password = password[idx+1:]
    idx = password.find('$')
    password = password[:idx]
    return password


def hash_password(password, salt):
    """Hash a password given salt."""
    algorithm = 'sha512'
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    return password_db_string


def new_password_hash(password):
    """Hash a new password given salt."""
    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    return password_db_string

def get_all_comments(postid, connection):
    """Get all comments commented on post with postid."""
    comments = connection.execute(
        "SELECT C.owner, C.text, C.commentid "
        "FROM comments C "
        "WHERE C.postid = ? ",
        (postid,)
    ).fetchall()
    output = [{'owner': elt['owner'],
               'text': elt['text'],
               'commentid': elt['commentid']} for elt in comments]
    output = sorted(output, key=lambda k: k['commentid'])
    return output


def get_likes(postid, connection):
    """Get all likes on post with postid."""
    likes = connection.execute(
                "SELECT L.owner "
                "FROM likes L "
                "WHERE L.postid = ? ",
                (postid,)).fetchall()
    likes = [elt['owner'] for elt in likes]
    logname_liked = flask.session['logname'] in likes
    return likes, logname_liked

def verify_user(username, password):
    """Takes the given username and password and verifies."""
    # search for the user
    connection = insta485.model.get_db()
    connection.row_factory = sqlite3.Row
    current_db_password = connection.execute (
        'SELECT U.username, U.password '
        'FROM users U '
        'WHERE U.username = ? ',
        (username,)
    ).fetchall()
    # return 403 if the user does not exist
    if len(current_db_password) != 1:
        return flask.jsonify(**{'message': 'Forbidden'}), 403
    # user exists, now check password
    db_user = {'username': current_db_password[0]['username'], 
               'password': current_db_password[0]['password']}
    password = hash_password(password, get_salt(db_user['password']))
    if db_user['password'] != password:
        return False
    return True


def check_authentication():
    """Function to handle the authentication of the user."""
    # get flask session stuff
    session_username = flask.request.form.get('username')
    session_password = flask.request.form.get('password')
    if session_username and session_password:
        if verify_user(session_username, session_password):
            flask.session['logname'] = session_username
            return True
        return flask.jsonify(**{'message': 'Forbidden'}), 403

    # get http basic authentification stuff
    http_username = flask.request.authorization.get('username')
    http_password = flask.request.authorization.get('password')
    if http_username and http_password:
        if verify_user(http_username, http_password):
            flask.session['logname'] = http_username
            return True
        return flask.jsonify(**{'message': 'Forbidden'}), 403

    # if neither http or flask session used 
    return flask.jsonify(**{'message': 'Forbidden'}), 403
