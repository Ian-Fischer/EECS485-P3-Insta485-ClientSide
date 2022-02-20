"""
Insta485 index (main) view.

URLs include:
/
/explore/
/uploads/<filename>/
"""
import sqlite3
import flask
import insta485
from insta485.api.helper import check_authentication


@insta485.app.route('/', methods=['GET'])
def show_index():
    """Display / route."""
    if not check_authentication():
        return flask.redirect(flask.url_for('login'))
    context = {'logname': flask.session.get('logname')}
    return flask.render_template("index.html", **context)


@insta485.app.route('/explore/', methods=['GET'])
def show_explore():
    """Display /explore/ route."""
    # if not in session, login, True if O.K.
    if 'logname' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    # get not following
    not_following = []
    connection = insta485.model.get_db()
    # get users for explore
    logname = flask.session['logname']
    connection.row_factory = sqlite3.Row
    users = connection.execute(
        "SELECT U.username "
        "FROM users U "
        "EXCEPT "
        "SELECT F.username2 "
        "FROM following F "
        "WHERE F.username1 = ? OR F.username2 = ? ",
        (logname, logname, )
    ).fetchall()
    users = [elt['username'] for elt in users]
    if logname in users:
        users.remove(logname)
    for user in users:
        profile_pic = connection.execute(
            "SELECT U.filename "
            "FROM users U "
            "WHERE U.username = ? ",
            (user, )
        ).fetchall()
        user_dict = {}
        user_dict['username'] = user
        user_dict['user_img_url'] = profile_pic[0]['filename']
        not_following.append(user_dict)
    # build context and render
    context = {
        'logname': logname,
        'not_following': not_following
    }
    return flask.render_template("explore.html", **context)


@insta485.app.route('/uploads/<filename>', methods=['GET'])
def send_file(filename):
    """Endpoint handling file requests."""
    # check tos ee if logged in, if not 403
    if 'logname' not in flask.session:
        return flask.abort(403)
    # check to see if the file exists, if not 404
    if not (insta485.app.config['UPLOAD_FOLDER']/filename).exists():
        return flask.abort(404)
    upload_folder = insta485.app.config["UPLOAD_FOLDER"]
    return flask.send_from_directory(upload_folder, filename)
