import React from 'react';
import PropTypes from 'prop-types';

class Like extends React.Component {
    
    constructor(props) {
        super(props)
        this.state = { numlikes: 0, lognameLiked: false };
    }

    componentDidMount() {

    }

    render() {

    }

}

Like.PropTypes = {
    url = PropTypes.string.isRequired,
};

export default Like;