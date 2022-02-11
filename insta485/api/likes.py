"""Handles like endpoints."""
import flask
import insta485


"""
URLs handled in this file.

/api/v1/likes/ , args ?postid=<postid>, POST
/api/v1/likes/<likeid>/, DELETE
"""

@insta485.app.route('/api/v1/likes/', methods=['POST'])
def make_like():
    """Make a like at the specified post."""
    # postid is an arg ?postid=<postid>
    # TODO: what do we do if the argument is not specified?
    # 1. check authentication
