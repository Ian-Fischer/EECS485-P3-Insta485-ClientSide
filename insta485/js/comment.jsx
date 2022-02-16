import React from 'react';

class Comment extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {
        console.log(this.props.comment.owner);
        return (
            <ul>
                <li><a href={"/users/"+this.props.comment.owner+"/"}><b><p>{this.props.comment.owner}</p></b></a></li>
                <li><p>{this.props.comment.text}</p></li>
                {this.props.comment.lognameOwnsThis &&
                    <li>
                        <button className="delete-comment-button" onClick={() => this.props.handleDeleteComment(this.props.comment.url)}>
                            Delete Comment
                        </button>
                    </li>
                }
            </ul>
        )
    }
}


export default Comment;