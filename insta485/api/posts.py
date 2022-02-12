"""REST API for posts."""
"""
FLASK RESPONSE CODES! 
bad requests should take form of {'message': 'what was wrong', 'code': flaskcode}
for good requests, I think 200 for return content, 204 for good delete, but check spec
"""
from math import ceil
import flask
import insta485
import sqlite3
from insta485.api.helper import check_authentication, get_likes
from insta485.api.helper import get_all_comments, chunks

"""
URLs in this file:
/api/v1/posts/ -- GET
/api/v1/posts/<int:postid_url_slug>/

"""

@insta485.app.route('/api/v1/posts/', methods=['GET'])
def get_posts():
  """Return the 10 newests posts"""
  check_authentication()
  # connect to the db
  connection = insta485.model.get_db()
  connection.row_factory = sqlite3.Row
  # get a list of everyone logname follows and himself
  following = connection.execute(
    'SELECT F.username2 '
    'FROM following F '
    'WHERE F.username1 = ? ',
    (flask.session.get('logname'),)
  ).fetchall()
  following = [elt['username2'] for elt in following]
  following.append(flask.session.get('logname'))
  # get args
  page = flask.request.args.get('page', default=1, type=int)
  size = flask.request.args.get('size', default=1, type=int)
  post_lte = flask.request.args.get('post_lte', default=10, type=int)
  posts = []
  user_posts = connection.execute(
      "SELECT P.postid "
      "FROM posts P "
      "WHERE P.postid IN ( "
      "SELECT D.postid "
      "FROM posts D, following F "
      "WHERE P.owner = ? OR (F.username1 = ? AND P.owner = F.username2) "
      "ORDER BY D.postid DESC) "
      "ORDER BY P.postid DESC "
      "LIMIT ? "
      "OFFSET ? ",
      (flask.session.get('logname'), flask.session.get('logname'), size, (page - 1)*size,)
  ).fetchall()
  user_posts = [elt['postid'] for elt in user_posts]
  num_posts = connection.execute(
    "SELECT P.postid "
    "FROM posts P "
    "WHERE P.postid IN ( "
      "SELECT D.postid "
      "FROM posts D, following F "
      "WHERE P.owner = ? OR (F.username1 = ? AND P.owner = F.username2))",
    (flask.session.get('logname'), flask.session.get('logname'),)
  ).fetchall()
  num_posts = len(num_posts)
  num_pages = ceil(num_posts/size)
  if page == num_pages:
    next = ""
  else:
    next = f'/api/v1/posts/?size={size}&page={page + 1}&postid_lte={post_lte}'
  results = []
  for post in user_posts:
    results.append({'postid': post,
                    'url': f'/api/v1/posts/{post}/'})
  context = {
    'next': next,
    'results': results,
    'url': f'/api/v1/posts/?size={size}&page={page}&postid_lte={post_lte}'
  }
  return flask.jsonify(**context), 200


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