import React from 'react';
import ReactDOM from 'react-dom';
import Post from './post';

// This method is only called once
// chagne to the root of the DOM
ReactDOM.render(
  // Insert the post component into the DOM
  <Post url="/api/v1/posts/1/" />,
  document.getElementById('reactEntry'),
);
