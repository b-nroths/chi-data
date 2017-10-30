import React from 'react'
import Header from './Header'
import Main from './Main'

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }


  render() {
    return (<div>
    <Header />
    <Main />
  </div>)
    // return (
    //   <div className="container">
    //     <nav className="navbar" role="navigation" aria-label="main navigation">
    //       <div className="navbar-brand">
    //         <a className="navbar-item" href="https://bulma.io">
    //           <img
    //             src="https://bulma.io/images/bulma-logo.png"
    //             alt="Bulma: a modern CSS framework based on Flexbox"
    //             width="112"
    //             height="28"
    //           />
    //         </a>

    //         <Link to="/" className="navbar-item">Home</Link>
    //         <Link to="/" className="navbar-item">About</Link>
    //         <Link to="/" className="navbar-item">Map</Link>
    //         <Link to="/" className="navbar-item">Data</Link>
    //       </div>
    //     </nav>
    //   </div>
    // );
  }
}

export default App;
