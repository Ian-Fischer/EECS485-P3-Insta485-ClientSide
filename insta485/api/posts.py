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
  page = flask.request.args.get('page', default=0, type=int)
  size = flask.request.args.get('size', default=10, type=int)
  if page < 0 or size < 0:
    return flask.jsonify(**{'message': 'bad request', 'status_code': 400}), 400
  posts = []
  user_posts = connection.execute(
      "SELECT P.postid "
      "FROM posts P "
      "WHERE P.postid IN ( "
      "SELECT D.postid "
      "FROM posts D, following F "
      "WHERE D.owner = ? OR (F.username1 = ? AND D.owner = F.username2) "
      "ORDER BY D.postid DESC) "
      "ORDER BY P.postid DESC "
      "LIMIT ? OFFSET ? ",
      (flask.session.get('logname'), flask.session.get('logname'), size, page*size,)
  ).fetchall()
  user_posts = [elt['postid'] for elt in user_posts]
  #if postid_lte is not specified on the current page, The ID of the most recent post on the current page
  if len(user_posts) == 0:
    postid_lte_default = 0
  else:
    postid_lte_default = user_posts[0]
  postid_lte = flask.request.args.get('postid_lte', default=postid_lte_default, type=int)
  num_posts = connection.execute(
    "SELECT P.postid "
    "FROM posts P "
    "WHERE P.postid < ? AND P.postid IN ( "
      "SELECT D.postid "
      "FROM posts D, following F "
      "WHERE D.owner = ? OR (F.username1 = ? AND D.owner = F.username2))",
    (flask.session.get('logname'), flask.session.get('logname'), postid_lte, )
  ).fetchall()
  import pdb; pdb.set_trace()
  for elt in user_posts:
    if elt < postid_lte:
      del elt
  num_posts = len(num_posts)
  if size == 0:
    num_pages = 1
  else:
    num_pages = ceil(num_posts/size) - 1
  # if i am on the last page, there is no next
  # import pdb; pdb.set_trace()
  if len(user_posts) < size:
    next_url = ""
  else:
    next_url = f'/api/v1/posts/?size={size}&page={page + 1}&postid_lte={postid_lte}'
  results = []
  for post in user_posts:
    results.append({'postid': post,
                    'url': f'/api/v1/posts/{post}/'})
  if flask.request.full_path[-1] == '?':
    url = flask.request.full_path[:-1]
  else:
    url = flask.request.full_path
  context = {
    'next': next_url,
    'results': results,
    'url': url
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
  likes, likeid = get_likes(postid_url_slug, connection)
  lognameLikesThis = False
  for dictionary in likes:
    if dictionary['owner'] == flask.session.get('logname'):
      lognameLikesThis = True
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
      return flask.jsonify(**{'message': 'Not Found'}), 404
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