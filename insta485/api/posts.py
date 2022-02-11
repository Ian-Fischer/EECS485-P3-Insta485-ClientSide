"""REST API for posts."""
"""
FLASK RESPONSE CODES! 
bad requests should take form of {'message': 'what was wrong', 'code': flaskcode}
for good requests, I think 200 for return content, 204 for good delete, but check spec
"""
import flask
import insta485
import sqlite3
from insta485.api.helper import check_authentication, get_likes
from insta485.api.helper import get_all_comments

"""
URLs in this file:
/api/v1/posts/ -- GET
/api/v1/posts/<int:postid_url_slug>/

"""

@insta485.app.route('/api/v1/posts/', methods=['GET'])
def get_posts():
  """Return the 10 newests posts"""
  check_authentication()
  # 1. CHECK AUTHENTIFICATION
  # 2. Get 10 newests posts (should be the 10 highest postid's)
  #    Posts need to be the logged in user or someone he follows
  # note postid is an int!
  # the "next" attribute should contain the URL of the next page
  # of posts, using arguments size, page, and postid_lte
  # so, next should have the size, page, and the next post ? idk
  # NOTE: these are the three args that could be passed
  page = flask.request.args['page']
  size = flask.request.args['size']
  post_lte = flask.request.args['post_lte']

  # NOTE: there is a Like 'object' nested in the Post object
  # it contains lognameLiked, likeid, and url to the post
  # if the user liked the post, then the url is the url to the like
  # endpoint where you can like posts
  # if the user has not liked the post, the the url is null (I think
  # in python that will be None, but we should double check)

  context = {}
  return flask.jsonify(**context)


@insta485.app.route('/api/v1/posts/<int:postid_url_slug>/', methods=['GET'])
def get_post(postid_url_slug):
    """Return post on postid."""
    check_authentication()
    # connect to database
    connection = insta485.model.get_db()
    connection.row_factory = sqlite3.Row
    # get likes and comments
    likes, logname_liked = get_likes(postid_url_slug, connection)
    comments = get_all_comments(postid_url_slug, connection)
    logname = flask.session['logname']
    post = connection.execute(
        "SELECT P.owner, P.filename as im, P.created, U.filename "
        "FROM posts P, users U "
        "WHERE P.postid = ? AND U.username = P.owner",
        (postid_url_slug, )
    ).fetchall()
    # if there is no post, abort
    if not post:
        return flask.jsonify(**{'message': 'Not Found'}), 404
    # build context and render
    context = {
        'logname': logname,
        'postid': postid_url_slug,
        "owner": post[0][0],
        "owner_img_url": post[0][3],
        "img_url": post[0][1],
        "timestamp": post[0][2],
        "likes": len(likes),
        "comments": comments,
        "logname_liked": logname_liked
    }
    # return context, and good response code
    return flask.jsonify(**context), 200