import React from 'react';

function Comment(props) {
    // owner of the comment
    // logname
    // text of the comment
    // need logname to know if we show a delete button on the comment
    // TODO: button functionality
    return (
        <div class="comment">
            <a href={"/users/"+owner+"/"}><b><p>{props.owner}</p></b></a>
            <p>{props.text}</p>
            { props.lognameOwnsThis &&
                <button className="delete-comment-button">
                    Delete Comment
                </button>
            }
        </div>
    )
}
