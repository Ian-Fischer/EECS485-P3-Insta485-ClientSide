import React from 'react';
import PropTypes from 'prop-types';

class CommentForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      value: '',
    };
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event) {
    this.setState({ value: event.target.value });
  }

  render() {
    const { handleSubmitComment } = this.props;
    const { value } = this.state;

    return (
      <form
        className="comment-form"
        onSubmit={(event) => {
          const temp = value;
          this.setState({ value: '' });
          handleSubmitComment(event, temp);
        }}
      >
        <input type="text" value={value} onChange={this.handleChange} />
      </form>
    );
  }
}

CommentForm.defaultProps = {
  handleSubmitComment: null,
};

CommentForm.propTypes = {
  handleSubmitComment: PropTypes.func,
};

export default CommentForm;
