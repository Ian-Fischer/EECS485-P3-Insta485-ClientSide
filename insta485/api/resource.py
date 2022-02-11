"""Handle /api/v1/ URL."""
import flask
import insta485

@insta485.app.route('/api/v1/', methods=['GET'])
def resources():
    """Return resources URLs."""
    context = {
        "comments": "/api/v1/comments/",
        "likes": "/api/v1/likes/",
        "posts": "/api/v1/posts/",
        "url": "/api/v1/"
    }
    return flask.jsonify(**context), 200