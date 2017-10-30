import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";

class Tile extends React.Component {
  // constructor(props) {
  //   super(props);
  // }

  componentDidMount() {
    // console.log('Component DID MOUNT!: ' + this.props.name);
    // console.log('fetch');
  }

  componentWillMount() {
    // console.log('Component WILL MOUNT!')
  }

  componentWillReceiveProps(newProps) {}

  shouldComponentUpdate(newProps, newState) {
    return true;
  }

  componentWillUpdate(nextProps, nextState) {
    // console.log('Component WILL UPDATE!');
  }

  componentDidUpdate(prevProps, prevState) {
    // console.log('Component DID UPDATE!');
  }

  componentWillUnmount() {
    // console.log('Component WILL UNMOUNT!')
  }

  render() {
    var data = this.props.data;

    return (
      <div className="card graph tile is-child">
        <header className="card-header">
          <p className="card-header-title">
            {this.props.data.title}{" "}
            <a
              href="#"
              className="icon is-xsmall icon-sup hint--bottom hint--long"
              aria-label={
                this.props.data.definition +
                " (Updated: " +
                this.props.data.updated_at +
                " EST)"
              }
            >
              {" "}<i className="fa fa-info-circle" />
            </a>
          </p>
        </header>
        <div className="card-content">
          <div className="content">
            <div className="number-container">
              <p className="title">
                {data.total}
              </p>
            </div>
            <div className="graph-container">
              {/* <h1 className="tile-number">777</h1> */}
              <ResponsiveContainer width="100%" height="100%">
                <LineChart
                  data={data.current_data}
                  margin={{ top: 0, right: 0, left: 0, bottom: 0 }}
                >
                  <XAxis
                    axisLine={false}
                    tickLine={false}
                    mirror={true}
                    dataKey="hour"
                  />
                  <YAxis
                    axisLine={false}
                    tickLine={false}
                    mirror={true}
                    domain={[0, "dataMax"]}
                  />

                  <Tooltip />
                  <Line
                    type="monotone"
                    dataKey="cnt"
                    stroke="#8884d8"
                    dot={false}
                  />
                  <Line
                    type="basis"
                    dataKey="cnt_current"
                    stroke="#3273dc"
                    dot={false}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default Tile;
