import React from 'react';
import PropTypes from 'prop-types';
import InfiniteScroll from 'react-infinite-scroll-component';
import Post from './post';

class Index extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      results: [],
      next: '',
    };

    this.fetchNext = this.fetchNext.bind(this);
  }

  componentDidMount() {
    const { url } = this.props;
    const requestOptions = {
      credentials: 'same-origin',
    };
    fetch(url, requestOptions)
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          results: data.results,
          next: data.next,
        });
      })
      .catch((error) => console.log(error));
  }

  fetchNext() {
    // get state attributes
    const requestOptions = {
      credentials: 'same-origin',
    };
    const { results, next } = this.state;
    // check to see if there is a next to get
    if (next != null) {
      fetch(next, requestOptions)
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          // update the state
          this.setState(() => {
            const newResults = results.concat(data.results);
            const newNext = data.next;
            return { results: newResults, next: newNext };
          });
        })
        .catch((error) => console.log(error));
    }
  }

  render() {
    const { results, next } = this.state;

    return (
      <InfiniteScroll dataLength={results.length} hasMore={next != null} next={this.fetchNext}>
        <div>
          {results.map((result) => <Post key={result.postid} url={result.url} />)}
        </div>
      </InfiniteScroll>
    );
  }
}

Index.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Index;
