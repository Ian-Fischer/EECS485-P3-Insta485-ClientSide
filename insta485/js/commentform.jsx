import React from 'react'

class CommentForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            value: ""
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        this.setState({value: event.target.value})
    }

    handleSubmit() {
        console.log('implement me!')
    }
    render() {
        return (
            <form className="comment-form">
                <label>New Comment: </label>
                <input type="text" value="" defaultValue=""/>
                <input type="submit" valuue="submit"/>
            </form>
        );
    }
}

export default CommentForm;