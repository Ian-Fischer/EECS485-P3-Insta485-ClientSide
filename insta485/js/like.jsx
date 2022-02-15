import React from 'react';
import PropTypes from 'prop-types';


// props should have lognameLiked and numLikes
class Likes extends React.Component {
    // the number of likes
    // logname liked it
    // TODO: button functionality stuff
    constructor(props) {
        super(props);
    }

    render() {
        return(
            <div>
                {this.props.numLikes != 1 && <p>{this.props.numLikes} likes</p>}
                {this.props.numLikes == 1 && <p>{this.props.numLikes} like </p>}
                {this.props.lognameLiked &&
                    <button className="like-unlike-button" onClick={this.props.handleUnlike}>
                        Unlike
                    </button>
                }
                {!this.props.lognameLiked &&
                    <button className="like-unlike-button" onClick={this.props.handleLike}>
                        Like
                    </button>
                }
            </div>
        )
    }
}

export default Likes;