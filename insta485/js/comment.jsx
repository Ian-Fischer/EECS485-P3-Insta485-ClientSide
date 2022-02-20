import React from 'react';
import PropTypes from 'prop-types';

class Comment extends React.PureComponent {
  render() {
    const { comment, handleDeleteComment } = this.props;

    return (
      <ul>
        <li><a href={`/users/${comment.owner}/`}><b><p>{comment.owner}</p></b></a></li>
        <li><p>{comment.text}</p></li>
        {comment.lognameOwnsThis
        && (
        <li>
          <button type="button" className="delete-comment-button" onClick={() => handleDeleteComment(comment.url)}>
            Delete Comment
          </button>
        </li>
        )}
      </ul>
    );
  }
}

Comment.defaultProps = {
  comment: null,
  handleDeleteComment: null,
};

Comment.propTypes = {
  comment: PropTypes.objectOf(PropTypes.any),
  handleDeleteComment: PropTypes.func,
};

export default Comment;
