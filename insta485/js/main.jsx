import React from 'react';
import ReactDOM from 'react-dom';
import Index from './index';

// This method is only called once
// change to the root of the DOM
ReactDOM.render(
  // Insert the post component into the DOM
  <Index url="/api/v1/posts/" />,
  document.getElementById('reactEntry'),
);
