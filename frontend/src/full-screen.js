// var ReactDOM = require('react-dom');
import React from "react";
import Tile from "./tile";

class FullScreen extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      current: {}
    };
  }

  componentDidMount() {}

  render() {
    var tv_row = [];
    var graph_row = [];
    var i = 0;
    var graphs = [];

    for (var kpi_name_tile in this.props.allKPIs) {
      var item_tile = this.props.allKPIs[kpi_name_tile];

      // for i in
      graph_row.push(
        <div key={kpi_name_tile} className="tile">
          <Tile data={item_tile} />
        </div>
      );
      if (i % 3 === 0) {
        tv_row.push(
          <div className="tile is-ancestor">
            {graph_row}
          </div>
        );
      } else {
        tv_row.pop();
        tv_row.push(
          <div className="tile is-ancestor">
            {graph_row}
          </div>
        );
      }

      if (i % 3 === 2) {
        graph_row = [];
      }
      i++;
    }

    graphs.push(tv_row);

    return (
      <div>
        <section className="hero is-dark is-bold is-fullheight">
          {graphs}
          <footer className="footer">
            <div className="container">
              <div className="content">
                <a
                  className="button is-link"
                  onClick={e => {
                    this.props.didSelectTV(false);
                  }}
                >
                  Close
                </a>
              </div>
            </div>
          </footer>
        </section>
      </div>
    );
  }
}

export default FullScreen;
