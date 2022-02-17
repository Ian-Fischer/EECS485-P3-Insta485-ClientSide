import React from 'react'
import Post from './post'
import PropTypes from 'prop-types';
import InfiniteScroll from 'react-infinite-scroll-component';

class Index extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            results: [],
            next: ""
        };

        this.fetchNext = this.fetchNext.bind(this);
    }

    componentDidMount() {
        const { url } = this.props;
        const requestOptions = {
            credentials: 'same-origin'
        }
        fetch(url, requestOptions)
            .then((response) => {
                if (!response.ok) throw Error(response.statusText);
                return response.json();
            })
            .then((data) => {
                this.setState({
                    results: data.results,
                    next: data.next
                });
            })
            .catch((error) => console.log(error));
    }

    fetchNext() {
        // get state attributes
        const requestOptions = {
            credentials: 'same-origin',
        }
        // check to see if there is a next to get 
        if (this.state.next != null) {
            fetch(this.state.next, requestOptions)
                .then((response) => {
                    if (!response.ok) throw Error(response.statusText);
                    return response.json();
                })
                .then((data) => {
                    // update the state
                    this.setState(() => {
                        var newResults = this.state.results.concat(data.results);
                        var newNext = data.next;
                        return {results: newResults, next: newNext};
                    })
                })
                .catch((error) => console.log(error));
        }
    }


    render() {
        return (
            <InfiniteScroll dataLength={this.state.results.length} hasMore={this.state.next != null} next={this.fetchNext}>
                <div>
                    {this.state.results.map((result) => {
                        return <Post key={result.postid} url={result.url}/>
                    })}
                </div>
            </InfiniteScroll>
            );
    }
}

Index.propTypes = {
    url: PropTypes.string.isRequired,
};

export default Index;