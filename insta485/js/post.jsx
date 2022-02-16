import React from 'react';
import PropTypes from 'prop-types';
import moment from 'moment';
import Like from './like';
import Comment from './comment';
import CommentForm from './commentform';

class Post extends React.Component {
  /* Display number of image and post owner of a single post
   */

  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = {
      comments: [],
      created: "",
      imgUrl: "",
      likes: {},
      owner: "",
      ownerImgUrl: "",
      ownerShowUrl: "",
      postShowUrl: "",
      postid: 0,
    };

    this.handleLike = this.handleLike.bind(this);
    this.handleUnlike = this.handleUnlike.bind(this);
    this.handleDeleteComment = this.handleDeleteComment.bind(this)
  }

  componentDidMount() {
    // This line automatically assigns this.props.url to the const variable url
    const { url } = this.props;
    // Call REST API to get the post's information
    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        console.log(data.comments)
        this.setState({
          comments: data.comments,
          created: data.created,
          imgUrl: data.imgUrl,
          likes: data.likes,
          owner: data.owner,
          ownerImgUrl: data.ownerImgUrl,
          ownerShowUrl: data.ownerShowUrl,
          postShowUrl: data.postShowUrl,
          postid: data.postid,
        });
        console.log('after the setState')
        console.log(this.state.comments)
      })
      .catch((error) => console.log(error));
  }

  handleLike() {
    const makeLikeUrl = '/api/v1/likes/?postid='+this.state.postid;
    fetch(makeLikeUrl, { credentials: 'same-origin', method: 'POST' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        console.log(this.state.likes.lognameLikesThis)
        if (this.state.likes.lognameLikesThis == false) {
          this.setState(() => {
            // increment likes, change lognameLikesThis to true, url to likeid
            const newStateLikes = {
              numLikes: this.state.likes.numLikes + 1,
              lognameLikesThis: true,
              url: data.url
            };
            return { likes: newStateLikes};
          });
      }
      })
      .catch((error) => console.log(error));
  }

  handleUnlike() {
    const deleteLikeURL = this.state.likes.url
    fetch(deleteLikeURL, { credentials: 'same-origin', method: 'DELETE' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
      })
      .then(() => {
        this.setState(() => {
          // decrement likes, change lognameLikesThis to false, url to null
          var newStateLikes = {
            numLikes: this.state.likes.numLikes - 1,
            lognameLikesThis: false,
            url: null
          }
          return {likes: newStateLikes}
        });
      })
      .catch((error) => console.log(error));
  }

  handleDeleteComment(url) {
    console.log(url)
    fetch(url, { credentials: 'same-origin', method: 'DELETE'})
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
      })
      .then(() => {
        this.setState((state) => {
          var newComments = state.comments.filter((comment) => comment.url != url)
          return {comments: newComments}
        });
      })
      .catch((error) => console.log(error));
  }

  render() {
    // This line automatically assigns this.state.imgUrl to the const variable imgUrl
    // and this.state.owner to the const variable owner
    // humanized time stamp
    var humanized = moment(this.state.timestamp).fromNow(true);
    console.log(this.state)
    return (
      <div className="posts">
        <ul className='toppost'>
          <li className='leftStuff'><a href={"/users/"+this.state.owner+"/"}><img src={this.state.ownerImgUrl} className="profilepicture" alt="Profile Picture"/></a></li>
          <li className='leftStuff'><a href={"/users/"+this.state.owner+"/"} className="username"><b>{this.state.owner}</b></a></li>
          <li><a href={"/posts/"+this.state.postid+"/"}  className="time">{humanized}</a></li>
        </ul>
        <img src={this.state.imgUrl} alt="Post" onDoubleClick={this.handleLike}/>
        <Like numLikes={this.state.likes.numLikes} lognameLikedThis={this.state.likes.lognameLikesThis} handleLike={this.handleLike} handleUnlike={this.handleUnlike}/>
        {this.state.comments.map((comment) => {
          return <Comment comment={comment} handleDeleteComment={this.handleDeleteComment}/>
        })}
        <CommentForm/>
      </div>
    );
  }
}

// this checks type of immutable props that are passed down
// makes sure that the url we get is a string, so we can
// use it safely
Post.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Post;