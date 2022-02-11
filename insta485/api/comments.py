"""URLs for comments."""
"""
FLASK RESPONSE CODES! 
bad requests should take form of {'message': 'what was wrong', 'code': flaskcode}
for good requests, I think 200 for return content, 204 for good delete, but check spec
"""


import flask
import insta485
from helper import check_authentication

@insta485.app.route('/api/v1/comments/', methods=['POST'])
def make_comment():
    check_authentication()
    postid = flask.request.args['postid']
    # use SELECT last_insert_rowid() to get the last id
    # this isn't for incrementing, the return of this post
    # needs to include all the comment information
    # which means we need the comment id
    # so, use that function to get the id and return the json
    # then, we can make the comment, and the new id should match
    # the one we need


@insta485.app.route('/api/v1/comments/<commentid>/', method=['DELETE'])
def delete_comment():
    # NOTE: if the commentid does not exist, return flask.abort(404)
    # NOTE: if the comment owner is not the logname, return flask.abort(403)
    # NOTE:
    check_authentication()
    commentid = flask.request.args['commentid']
