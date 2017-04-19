class ImageResults extends React.Component {
  render() {
    return(
      <div>
        {this.props.results.map(item => (
          <p>{item.tag}: {item.obj}</p>
        ))}
      </div>
    );
  }
}

class VideoResults extends React.Component {
  render() {
    return(
      <div>
        {this.props.results.map(item => (
          <p><a href={item.url}>{item.text}</a></p>
        ))}
      </div>
    );
  }
}

class TextResults extends React.Component {
  render() {
    return (
      <div>
        {this.props.results.map(item => (
          <p><a href={item.url}>{item.text}</a></p>
        ))}
      </div>
    );
  }
}

class SearchBar extends React.Component {
  render() {
    return (
      <form>
        <ReactBootstrap.FormGroup>
          <ReactBootstrap.FormControl type="text" placeholder="Search..." />
        </ReactBootstrap.FormGroup>
      </form>
    );
  }
}


class SearchForm extends React.Component {
  render() {
    return (
      <div>
        <h3>The Blast</h3>
        <SearchBar />

        <br />

        <ReactBootstrap.Tabs defaultActiveKey="{1}" id="search-results">

          <ReactBootstrap.Tab eventKey="{1}" title="Text">
            <TextResults results={this.props.textResults} />
          </ReactBootstrap.Tab>

          <ReactBootstrap.Tab eventKey="{2}" title="Video">
            <VideoResults results={this.props.videoResults} />
          </ReactBootstrap.Tab>

          <ReactBootstrap.Tab eventKey="{3}" title="Image">
            <ImageResults results={this.props.imageResults} />
          </ReactBootstrap.Tab>

        </ReactBootstrap.Tabs>
      </div>
    );
  }
}

var TEXT_RESULTS = [
  {url: 'http://www.example.com/cool', text: 'text1'},
  {url: 'http://www.example.com/awesome', text: 'text2'},
  {url: 'http://www.example.com/handsome', text: 'text3'},
  {url: 'http://www.example.com/cute', text: 'text4'},
  {url: 'http://www.python.org/', text: 'text5'},
  {url: 'http://www.golang.org/', text: 'text6'},
]

var VIDEO_RESULTS = [
  {url: 'http://www.example.com/cool', text: 'video1'},
  {url: 'http://www.example.com/awesome', text: 'video2'},
  {url: 'http://www.example.com/handsome', text: 'video3'},
  {url: 'http://www.example.com/cute', text: 'video4'},
  {url: 'http://www.python.org/', text: 'video5'},
  {url: 'http://www.golang.org/', text: 'video6'},
]

var IMAGE_RESULTS = [
  {tag: 'image1', obj: 'this is img obj'},
  {tag: 'image2', obj: 'this is img obj'},
  {tag: 'image3', obj: 'this is img obj'},
  {tag: 'image4', obj: 'this is img obj'},
  {tag: 'image5', obj: 'this is img obj'},
  {tag: 'image6', obj: 'this is img obj'},
]

ReactDOM.render(
  <SearchForm textResults={TEXT_RESULTS} videoResults={VIDEO_RESULTS} imageResults={IMAGE_RESULTS} />,
  document.getElementById('container')
);
