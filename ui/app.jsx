class ImageResults extends React.Component {
  render() {
    if (this.props.results.length == 0) {
      return (
        <p>Sorry, no results.</p>
      );
    } else {
      return(
        <div>
          {this.props.results.map(item => (
            <p>{item.tag}: {item.obj}</p>
          ))}
        </div>
      );
    }
  }
}

class VideoResults extends React.Component {
  render() {
    if (this.props.results.length == 0) {
      return (
        <p>Sorry, no results.</p>
      );
    } else {
      return(
        <div>
          {this.props.results.map(item => (
            <p><a href={item.url}>{item.text}</a></p>
          ))}
        </div>
      );
    }
  }
}

class TextResults extends React.Component {
  render() {
    if (this.props.results.length == 0) {
      return (
        <p>Sorry, no results.</p>
      );
    } else {
      return (
        <div>
          {this.props.results.map(item => (
            <p><a href={item.url}>{item.text}</a></p>
          ))}
        </div>
      );
    }
  }
}

class SearchBar extends React.Component {
  constructor(props) {
    super(props);

    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleInputChange(event) {
    this.props.onSearchInput(event.target.value);
  }

  handleSubmit(event) {
    this.props.onSearchSubmit(event);
  }

  render() {
    return (
      <ReactBootstrap.Form horizontal>
        <ReactBootstrap.FormGroup>
          <ReactBootstrap.Col sm={11}>
            <ReactBootstrap.FormControl
              autoFocus="true"
              type="text"
              placeholder="Search..."
              value={this.props.searchInput}
              onChange={this.handleInputChange}
            />
          </ReactBootstrap.Col>
          <ReactBootstrap.Col sm={1}>
            <ReactBootstrap.Button
              type="submit"
              onClick={this.handleSubmit}>
              Search
            </ReactBootstrap.Button>
          </ReactBootstrap.Col>
        </ReactBootstrap.FormGroup>
      </ReactBootstrap.Form>
    );
  }
}


class SearchForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      searchInput: '',
      textResults: [],
      videoResults: [],
      imageResults: [],
    };

    this.handleSearchInput = this.handleSearchInput.bind(this);
    this.handleSearchSubmit = this.handleSearchSubmit.bind(this);
  }

  handleSearchInput(searchInput) {
    this.setState({searchInput: searchInput});
  }

  handleSearchSubmit(event) {
    event.preventDefault();
    if (this.state.searchInput.length == 0) {
      return;
    }

    // this piece of code assumes certain naming conventions
    // of the backend services
    var hostname = window.location.hostname
    var postfix = hostname.substring(hostname.indexOf("-"));

    fetch('http://text' + postfix + "/blast/api/v1.0/text/" + this.state.searchInput)
      .then(result=>result.json())
      .then(items=>this.setState({textResults: items}));

    fetch('http://video' + postfix + '/blast/api/v1.0/video/' + this.state.searchInput)
      .then(result=>result.json())
      .then(items=>this.setState({videoResults: items}));

    fetch('http://image' + postfix + '/blast/api/v1.0/image/' + this.state.searchInput)
      .then(result=>result.json())
      .then(items=>this.setState({imageResults: items}));
  }

  render() {
    return (
      <div>
        <h3>The Blast</h3>
        <SearchBar
          searchInput={this.state.searchInput}
          onSearchInput={this.handleSearchInput}
          onSearchSubmit={this.handleSearchSubmit}
        />

        <br />

        <ReactBootstrap.Tabs defaultActiveKey="{1}" id="search-results">

          <ReactBootstrap.Tab eventKey="{1}" title="Text">
            <TextResults results={this.state.textResults} />
          </ReactBootstrap.Tab>

          <ReactBootstrap.Tab eventKey="{2}" title="Video">
            <VideoResults results={this.state.videoResults} />
          </ReactBootstrap.Tab>

          <ReactBootstrap.Tab eventKey="{3}" title="Image">
            <ImageResults results={this.state.imageResults} />
          </ReactBootstrap.Tab>

        </ReactBootstrap.Tabs>
      </div>
    );
  }
}

ReactDOM.render(
  <SearchForm />,
  document.getElementById('container')
);
