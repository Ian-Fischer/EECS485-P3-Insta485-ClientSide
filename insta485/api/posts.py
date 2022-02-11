"""REST API for posts."""
import flask
import insta485

"""
notes on authentication with http


"""

@insta485.app.route('/api/v1/posts/', methods=['GET'])
def get_posts():
  """Return the 10 newests posts"""
  # 1. CHECK AUTHENTIFICATION
  # 2. Get 10 newests posts (should be the 10 highest postid's)
  # note postid is an int!
  # the "next" attribute should contain the URL of the next page
  # of posts, using arguments size, page, and postid_lte
  # so, next should have the size, page, and the next post ? idk
  context = {}
  return flask.jsonify(**context)


@insta485.app.route('/api/v1/posts/<int:postid_url_slug>/')
def get_post(postid_url_slug):
    """Return post on postid."""
    context = {}
    return flask.jsonify(**context)