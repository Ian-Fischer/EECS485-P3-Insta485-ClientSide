"""Helper functions."""


import sqlite3
# import hashlib
# import uuid
# import pathlib
import flask
import insta485


# def get_file_path(filename):
#     """Get uuid file path."""
#     stem = uuid.uuid4().hex
#     suffix = pathlib.Path(filename).suffix
#     uuid_basename = f"{stem}{suffix}"
#     # Save to disk
#     path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
#     return path, uuid_basename


# def get_salt(password):
#     """Get the salt from the password in the database."""
#     idx = password.find('$')
#     password = password[idx+1:]
#     idx = password.find('$')
#     password = password[:idx]
#     return password


# def hash_password(password, salt):
#     """Hash a password given salt."""
#     algorithm = 'sha512'
#     hash_obj = hashlib.new(algorithm)
#     password_salted = salt + password
#     hash_obj.update(password_salted.encode('utf-8'))
#     password_hash = hash_obj.hexdigest()
#     password_db_string = "$".join([algorithm, salt, password_hash])
#     return password_db_string


# def new_password_hash(password):
#     """Hash a new password given salt."""
#     algorithm = 'sha512'
#     salt = uuid.uuid4().hex
#     hash_obj = hashlib.new(algorithm)
#     password_salted = salt + password
#     hash_obj.update(password_salted.encode('utf-8'))
#     password_hash = hash_obj.hexdigest()
#     password_db_string = "$".join([algorithm, salt, password_hash])
#     return password_db_string


def response_dict(status_code):
    """Return response dictionary."""
    if status_code == 403:
        message = 'Forbidden'
    elif status_code == 404:
        message = 'Not Found'
    elif status_code == 204:
        message = 'No Content'
    elif status_code == 400:
        message = 'Bad Request'
    return {'message': message, 'status_code': status_code}


def get_all_comments(postid, connection):
    """Get all comments commented on post with postid."""
    comments = insta485.views.helper.comment_query(postid, connection)
    output = [
        {
            'owner': elt['owner'],
            'text': elt['text'],
            'commentid': elt['commentid'],
            'ownerShowUrl': f'/users/{elt["owner"]}/',
            'lognameOwnsThis': elt['owner'] == flask.session.get('logname'),
            'url': f'/api/v1/comments/{elt["commentid"]}/'
        }
        for elt in comments
    ]
    output = sorted(output, key=lambda k: k['commentid'])
    return output


def get_likes(postid, connection):
    """Get all likes on post with postid."""
    likes = connection.execute(
                "SELECT L.owner, L.likeid "
                "FROM likes L "
                "WHERE L.postid = ? ",
                (postid,)
            ).fetchall()
    likes = [{'owner': elt['owner'], 'likeid': elt['likeid']} for elt in likes]
    likeid = None
    for dictionary in likes:
        if dictionary.get('owner') == flask.session.get('logname'):
            likeid = dictionary.get('likeid')
    return likes, likeid


def verify_user(username, password):
    """Take the given username and password and verify."""
    # search for the user
    connection = insta485.model.get_db()
    connection.row_factory = sqlite3.Row
    current_db_password = connection.execute(
        'SELECT U.username, U.password '
        'FROM users U '
        'WHERE U.username = ? ',
        (username,)
    ).fetchall()
    # return 403 if the user does not exist
    if len(current_db_password) != 1:
        return False
    # user exists, now check password
    db_user = {'username': current_db_password[0]['username'],
               'password': current_db_password[0]['password']}
    salt = insta485.views.helper.get_salt(db_user['password'])
    password = insta485.views.helper.hash_password(password, salt)
    if db_user['password'] != password:
        return False
    return True


def check_authentication():
    """Handle the authentication of the user."""
    # check if already logged in
    if 'logname' in flask.session:
        return True

    # get flask session stuff
    if flask.request.form:
        session_username = flask.request.form['username']
        session_password = flask.request.form['password']
        if verify_user(session_username, session_password):
            flask.session['logname'] = session_username
            return True

    # get http basic authentification stuff
    elif flask.request.authorization:
        http_username = flask.request.authorization['username']
        http_password = flask.request.authorization['password']
        if verify_user(http_username, http_password):
            flask.session['logname'] = http_username
            return True

    # if neither http or flask session used
    return False
