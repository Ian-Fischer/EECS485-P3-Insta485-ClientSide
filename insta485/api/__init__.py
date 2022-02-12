"""Insta485 Rest API."""

import insta485
from insta485.api.posts import get_post
from insta485.api.posts import get_posts
from insta485.api.likes import make_like
from insta485.api.likes import delete_like
from insta485.api.resource import resources
from insta485.api.helper import get_file_path
from insta485.api.helper import get_salt
from insta485.api.helper import hash_password
from insta485.api.helper import new_password_hash
from insta485.api.helper import get_all_comments
from insta485.api.helper import get_likes
from insta485.api.helper import verify_user
from insta485.api.helper import check_authentication
from insta485.api.comments import make_comment
from insta485.api.comments import delete_comment
