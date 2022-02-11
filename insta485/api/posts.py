"""REST API for posts."""
import flask
import insta485

"""
URLs in this file:
/api/v1/posts/ -- GET
/api/v1/posts/<int:postid_url_slug>/

"""

@insta485.app.route('/api/v1/posts/', methods=['GET'])
def get_posts():
  """Return the 10 newests posts"""
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

  # NOTE: there is a like 'object' nested in the posts object
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
    # again, postid is an int
    # need all the as p2, but it's important to note
    # that the time stored in the db is not humanized
    # we need to do that on the front end
    context = {}
    return flask.jsonify(**context)