import React from "react";
var createReactClass = require("create-react-class");
import { BarChart, Bar, ResponsiveContainer } from "recharts";
import "./MapPanel.css";

class MapPanel2 extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      tract_data: null
    };
  }

  componentDidMount() {
    var url =
      "http://chicago.bnroths.com/data/tract_data/lehd_rac/17031839000.json";
    // console.log(url)
    fetch(url).then(response => response.json()).then(json =>
      this.setState({
        tract_data: json
      })
    );
  }

  render() {
    const TinyBarChart = createReactClass({
      render() {
        return (
          <div>
            <h1>
              {this.props.graphTitle}
            </h1>
            <ResponsiveContainer width="100%" height={100}>
              <BarChart width={150} height={40} data={this.props.data}>
                <Bar isAnimationActive={false} dataKey="cnt" fill="#8884d8" />
                }
              </BarChart>
            </ResponsiveContainer>
          </div>
        );
      }
    });
    if (this.state.tract_data) {
      Object.keys(this.state.tract_data).map(d => console.log(d));
    }

    return (
      <div>
        <div className="section">
          {this.state.tract_data &&
            Object.keys(this.state.tract_data).map((entry, index) =>
              <TinyBarChart
                key={index}
                graphTitle={this.state.tract_data[entry].meta.name}
                data={this.state.tract_data[entry].data}
              />
            )}
        </div>
      </div>
    );
  }
}

export default MapPanel2;
