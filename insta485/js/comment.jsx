import React from 'react';

class Comment extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {
        console.log(this.props.comment.owner);
        return (
            <div className='fullcomment'>
                <a href={"/users/"+this.props.comment.owner+"/"}><b><p>{this.props.comment.owner}</p></b></a>
                <p>{this.props.comment.text}</p>
                { this.props.comment.lognameOwnsThis &&
                    <button className="delete-comment-button" onClick={() => this.props.handleDeleteComment(this.props.comment.url)}>
                        Delete Comment
                    </button>
                }
            </div>
        )
    }
}


export default Comment;