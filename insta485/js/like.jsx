import React from 'react';
import PropTypes from 'prop-types';

// props should have lognameLiked and numLikes
function Likes(props) {
  console.log(props);
  const {
    numLikes,
    lognameLikedThis,
    handleLike,
    handleUnlike,
  } = props;

  return (
    <div>
      {numLikes !== 1 && (
      <p>
        {numLikes}
        {' '}
        likes
      </p>
      )}
      {numLikes === 1 && (
      <p>
        {numLikes}
        {' '}
        like
        {' '}
      </p>
      )}
      {lognameLikedThis
                  && (
                  <button type="button" className="like-unlike-button" onClick={handleUnlike}>
                    Unlike
                  </button>
                  )}
      {!lognameLikedThis
                  && (
                  <button type="button" className="like-unlike-button" onClick={handleLike}>
                    Like
                  </button>
                  )}
    </div>
  );
}

Likes.defaultProps = {
  numLikes: 0,
  lognameLikedThis: false,
  handleLike: null,
  handleUnlike: null,
};

Likes.propTypes = {
  numLikes: PropTypes.number,
  lognameLikedThis: PropTypes.bool,
  handleLike: PropTypes.func,
  handleUnlike: PropTypes.func,
};

export default Likes;
