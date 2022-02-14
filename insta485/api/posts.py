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
from insta485.api.helper import get_all_comments

"""
URLs in this file:
/api/v1/posts/ -- GET
/api/v1/posts/<int:postid_url_slug>/

"""

@insta485.app.route('/api/v1/posts/', methods=['GET'])
def get_posts():
  """Return the 10 newests posts"""
  if not check_authentication():
    return flask.jsonify(**{'message': 'Forbidden', 'status_code': 403}), 403
  # connect to the db, get logname
  connection = insta485.model.get_db()
  connection.row_factory = sqlite3.Row
  logname = flask.session.get('logname')
  # get args
  page = flask.request.args.get('page', default=0, type=int)
  size = flask.request.args.get('size', default=10, type=int)
  # check to make sure page and size are not negative
  if page < 0 or size < 0:
    return flask.jsonify(**{'message': 'Bad Request', 'status_code': 400}), 400
  postid_lte = 0
  # what we query depends on what we know
  if flask.request.args.get('postid_lte', type=int) is not None:
    postid_lte = flask.request.args.get('postid_lte', type=int)
    # query all necessary posts
    user_posts = connection.execute(
        "SELECT P.postid "
        "FROM posts P "
        "WHERE P.postid IN ( "
        "SELECT D.postid "
        "FROM posts D, following F "
        "WHERE (D.owner = ? OR (F.username1 = ? AND D.owner = F.username2)) AND D.postid <= ?)"
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
    next_url = f'/api/v1/posts/?size={size}&page={page+1}&postid_lte={postid_lte}'
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
    return flask.jsonify(**{'message': 'Forbidden', 'status_code': 403}), 403
  # connect to database
  connection = insta485.model.get_db()
  connection.row_factory = sqlite3.Row
  # get likes and comments
  likes, likeid = get_likes(postid_url_slug, connection)
  lognameLikesThis = False
  for dictionary in likes:
    if dictionary['owner'] == flask.session.get('logname'):
      lognameLikesThis = True
  # set like url
  url = None
  if lognameLikesThis:
    url = f'/api/v1/likes/{likeid}/'
  likes = {
    'numLikes': len(likes),
    'lognameLikesThis': lognameLikesThis,
    'url': url
  }
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
      return flask.jsonify(**{'message': 'Not Found', 'status_code': 404}), 404
  # build context and render
  context = {
    'comments': comments,
    'created': post[0]['created'],
    'imgUrl': f'/uploads/{post[0]["im"]}',
    'likes': likes,
    'owner': flask.session.get('logname'),
    'ownerImgUrl': f'/uploads/{post[0]["filename"]}',
    'ownerShowUrl': f'/users/{flask.session.get("logname")}/',
    'postShowUrl': f'/posts/{postid_url_slug}/',
    'postid': postid_url_slug,
    'url': f'/api/v1/posts/{postid_url_slug}/'
  }
  # return context, and good response code
  return flask.jsonify(**context), 200