import React from 'react';

class Comment extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div>
                <a href={"/users/"+owner+"/"}><b><p>{this.props.owner}</p></b></a>
                <p>{this.props.text}</p>
                { this.props.lognameOwnsThis &&
                    <button className="delete-comment-button" onClick={() => this.props.handleDeleteComment(this.props.comment.url)}>
                        Delete Comment
                    </button>
                }
            </div>
        )
    }
    }


export default Comment;