import React from 'react';
import PropTypes from 'prop-types';

class Post extends React.Component {
  /* Display number of image and post owner of a single post
   */

  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = { 
      imgUrl: '', 
      owner: '', 
      profileImgURL: '', 
      numLikes = 0, 
      lognameLiked = false, 
      postid: 0
    };
    // ^^ these will be changed once we get information for RestAPI
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
        this.setState({
          imgUrl: data.imgUrl,
          owner: data.owner
        });
      })
      .catch((error) => console.log(error));
  }

  render() {
    // This line automatically assigns this.state.imgUrl to the const variable imgUrl
    // and this.state.owner to the const variable owner
    const { imgUrl, owner } = this.state;

    // Render number of post image and post owner
    // FIXME: add comments
    return (
      <div className="post">
        <ul>
          <li><a href={"/users/"+owner+"/"}><img src={"/uploads/"+profileImgURL+"/"} class="profilepicture" alt="Profile Picture"/></a></li>
          <li><a href={"/users/"+owner+"/"} class="username"><b>{owner}</b></a></li>
          <li><a href={"/posts/"+postid+"/"}  class="time">{{ timestamp }}</a></li>
        </ul>
        <img src={"/uploads/"+imgUrl+"/"} alt="Post" style="width:400px; height:400px; position: relative; margin-right: auto; margin-left: auto;"/>
        <Like numLikes={numLikes} lognameLiked={lognameLiked}/>
        !!! CALL TO COMMENTS FUNCTION HERE !!!
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
/*

  'commentid': commentid,
  'lognameOwnsThis': True,
  'owner': flask.session.get('logname'),
  'ownerShowUrl': '/users/{logname}/'.format(logname=flask.session.get('logname')),
  'text': text,

<div class="posts">
<ul>
    <li><a href="{{ url_for('show_user', user_url_slug=post.owner) }}"><img src="{{ url_for('send_file', filename=post.owner_img_url) }}" alt="Profile picture" class="profilepicture"></a></li>
    <li><a href="{{ url_for('show_user', user_url_slug=post.owner) }}" class="username"><b>{{post.owner}}</b></a></li>
    <li><a href="{{ url_for('show_post', post_url_slug=post.postid) }}" class="time">{{post.timestamp}}</a></li>
</ul>
<img src="{{ url_for('send_file', filename=post.img_url) }}" alt="Post" style="width:400px; height:400px; position: relative; margin-right: auto; margin-left: auto;">
{% if post.likes == 1%}
    <p>1 like</p>
{% else %}
    <p>{{post.likes}} likes</p>
{% endif %}
{% if post.logname_liked == false %}
    <form action="{{ url_for('like') }}?target={{ url_for('show_index') }}" method="post" enctype="multipart/form-data">
        <input type="hidden" name="operation" value="like"/>
        <input type="hidden" name="postid" value="{{post.postid}}"/>
        <input type="submit" name="like" value="like"/>
    </form>
{% else %}
    <form action="{{ url_for('like') }}?target={{ url_for('show_index') }}" method="post" enctype="multipart/form-data">
        <input type="hidden" name="operation" value="unlike"/>
        <input type="hidden" name="postid" value="{{post.postid}}"/>
        <input type="submit" name="unlike" value="unlike"/>
    </form>
{% endif %}
{% for comment in post.comments %}
    <p><a href="{{ url_for('show_user', user_url_slug=comment.owner) }}"><b>{{comment.owner}}</b></a> {{comment.text}}</p>
{% endfor %}
<form action="{{ url_for('comment') }}?target={{ url_for('show_index') }}" method="post" enctype="multipart/form-data">
    <input type="hidden" name="operation" value="create"/>
    <input type="hidden" name="postid" value="{{post.postid}}"/>
    <input type="text" name="text" required/>
    <input type="submit" name="comment" value="comment"/>
</form>
</div>
*/