"""REST API for posts.

URLs in this file:
/api/v1/posts/ -- GET
/api/v1/posts/<int:postid_url_slug>/
"""

import sqlite3
import flask
import insta485
from insta485.api.helper import check_authentication, get_likes, response_dict
from insta485.api.helper import get_all_comments


@insta485.app.route('/api/v1/posts/', methods=['GET'])
def get_posts():
    """Return the 10 newests posts."""
    if not check_authentication():
        return flask.jsonify(**response_dict(403)), 403
    # get args
    logname = flask.session.get('logname')
    page = flask.request.args.get('page', default=0, type=int)
    size = flask.request.args.get('size', default=10, type=int)
    # check to make sure page and size are not negative
    if page < 0 or size < 0:
        return flask.jsonify(**response_dict(400)), 400
    postid_lte = 0
    # what we query depends on what we know
    # connect to the db
    connection = insta485.model.get_db()
    connection.row_factory = sqlite3.Row
    if flask.request.args.get('postid_lte', type=int) is not None:
        postid_lte = flask.request.args.get('postid_lte', type=int)
        # query all necessary posts
        user_posts = connection.execute(
            "SELECT P.postid "
            "FROM posts P "
            "WHERE P.postid IN ( "
            "SELECT D.postid "
            "FROM posts D, following F "
            "WHERE (D.owner = ? OR (F.username1 = ? "
            "AND D.owner = F.username2)) "
            "AND D.postid <= ?) "
            "ORDER BY P.postid DESC "
            "LIMIT ? OFFSET ? ",
            (logname, logname, postid_lte, size, page*size,)
        ).fetchall()
        user_posts = [elt['postid'] for elt in user_posts]
    else:
        # query all necessary posts
        user_posts = connection.execute(
            "SELECT P.postid "
            "FROM posts P "
            "WHERE P.postid IN ( "
            "SELECT D.postid "
            "FROM posts D, following F "
            "WHERE D.owner = ? OR (F.username1 = ? AND D.owner = F.username2))"
            "ORDER BY P.postid DESC "
            "LIMIT ? OFFSET ? ",
            (logname, logname, size, page*size,)
        ).fetchall()
        # get postid's for everything returned
        user_posts = [elt['postid'] for elt in user_posts]
        if len(user_posts) == 0:
            postid_lte = 0
        else:
            postid_lte = max(user_posts)

    # now, we have taken care of all of arguments
    # first, do next_url
    if len(user_posts) < size or len(user_posts) == 0:
        next_url = ''
    else:
        next_url = f'/api/v1/posts/?size={size}'
        next_url = f'{next_url}&page={page+1}&postid_lte={postid_lte}'
    # construct results for all posts with postid <= postid_lte
    results = []
    for postid in user_posts:
        if postid <= postid_lte:
            results.append({
              'postid': postid,
              'url': f'/api/v1/posts/{postid}/'
            })
    # construct url
    if flask.request.full_path[-1] == '?':
        url = flask.request.full_path[:-1]
    else:
        url = flask.request.full_path
    # build context
    context = {
        'next': next_url,
        'results': results,
        'url': url
    }
    # return
    return flask.jsonify(**context), 200


@insta485.app.route('/api/v1/posts/<int:postid_url_slug>/', methods=['GET'])
def get_post(postid_url_slug):
    """Return post on postid."""
    if not check_authentication():
        return flask.jsonify(**response_dict(403)), 403
    # connect to database
    connection = insta485.model.get_db()
    connection.row_factory = sqlite3.Row
    # get likes and comments
    likes, likeid = get_likes(postid_url_slug, connection)
    logname_likes_this = False
    for dictionary in likes:
        if dictionary['owner'] == flask.session.get('logname'):
            logname_likes_this = True
    # set like url
    url = None
    if logname_likes_this:
        url = f'/api/v1/likes/{likeid}/'
    likes = {
        'numLikes': len(likes),
        'lognameLikesThis': logname_likes_this,
        'url': url
    }
    comments = get_all_comments(postid_url_slug, connection)
    post = connection.execute(
        "SELECT P.owner, P.filename as im, P.created, U.filename "
        "FROM posts P, users U "
        "WHERE P.postid = ? AND U.username = P.owner",
        (postid_url_slug, )
    ).fetchall()
    # if there is no post, abort
    if len(post) == 0:
        return flask.jsonify(**response_dict(404)), 404
    # build context and render
    context = {
        'comments': comments,
        'created': post[0]['created'],
        'imgUrl': f'/uploads/{post[0]["im"]}',
        'likes': likes,
        'owner': post[0]['owner'],
        'ownerImgUrl': f'/uploads/{post[0]["filename"]}',
        'ownerShowUrl': f'/users/{flask.session.get("logname")}/',
        'postShowUrl': f'/posts/{postid_url_slug}/',
        'postid': postid_url_slug,
        'url': f'/api/v1/posts/{postid_url_slug}/'
    }
    # return context, and good response code
    return flask.jsonify(**context), 200
