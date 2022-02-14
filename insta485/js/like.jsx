import React from 'react';
import PropTypes from 'prop-types';


// props should have lognameLiked and numLikes
function Likes(props) {
    // the number of likes
    // logname liked it
    // TODO: button functionality stuff
    return(
        <div>
            {props.numLikes != 1 && <p>{props.numLikes} likes</p>}
            {props.numLikes == 1 && <p>{props.numLikes} like </p>}
            {props.lognameLiked &&
                <button className="like-unlike-button">
                    Unlike
                </button>
            }
            {!props.lognameLiked &&
                <button className="like-unlike-button">
                    Like
                </button>
            }
        </div>
    )
}
