import React from 'react'

class CommentForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            value: ""
        };
        this.handleChange = this.handleChange.bind(this);
    }

    handleChange(event) {
        this.setState({value: event.target.value})
    }

    render() {
        return (
            <form className="comment-form" onSubmit={() => this.props.handleSubmitComment}>
                <input type="text" value={this.state.value} onChange={this.handleChange} />
            </form>  
        );
    }
}

export default CommentForm;