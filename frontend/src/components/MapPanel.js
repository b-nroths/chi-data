import React from "react";
import {
  BarChart,
  Bar,
  // XAxis,
  // YAxis,
  // CartesianGrid,
  // Tooltip,
  // Legend,
  ResponsiveContainer
} from "recharts";

class MapPanel extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  componentDidMount() {
    this.setState({
      dts: Object.keys(this.props.datasets[this.props.dataset]["cnts"])
    });
  }

  render() {
    // console.log('render map panel');
    var data = Object.keys(this.props.datasets[this.props.dataset]["cnts"]).map(d => ({
      dt: d,
      cnt: this.props.datasets[this.props.dataset]["cnts"][d]
    }));
    // console.log(data)
    const TinyBarChart = React.createClass({
      render() {
        return (
          <ResponsiveContainer width="100%" height={100}>
            <BarChart width={150} height={40} data={data}>
              <Bar isAnimationActive={false} dataKey="cnt" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        );
      }
    });

    return (
      <div>
        <div className="section">
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label style={{ minWidth: "100px" }} className="label">
                Datasets
              </label>
            </div>

            <div className="field-body">
              <div className="field">
                <div className="control">
                  <div className="select">
                    <select
                      name="dataset"
                      value={this.props.dataset}
                      onChange={this.props.handleChange}
                    >
                      {this.props.datasets &&
                        Object.keys(this.props.datasets).map(d => {
                          return (
                            <option value={d} key={d}>
                              {this.props.datasets[d]["name"]}
                            </option>
                          );
                        })}
                    </select>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label style={{ minWidth: "100px" }} className="label">
                Date
              </label>
            </div>

            <div className="field-body">
              <div className="field">
                <div className="control">
                  <div className="select">
                    <select
                      name="dt"
                      value={this.props.dt}
                      onChange={this.props.handleChange}
                    >
                      {this.props.dataset &&
                        Object.keys(this.props.datasets[this.props.dataset][
                          "cnts"
                        ]).sort().map(d => {
                          return (
                            <option value={d} key={d}>
                              {d}
                            </option>
                          );
                        })}
                    </select>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label style={{ minWidth: "100px" }} className="label">
                Start
              </label>
            </div>
            <div
              style={{ paddingTop: "0.375em" }}
              className="field-body is-normal"
            >
              <div className="field">
                {this.props.datasets[this.props.dataset]["dataset_start"]}
              </div>
            </div>
          </div>

          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label style={{ minWidth: "100px" }} className="label">
                Source
              </label>
            </div>
            <div
              style={{ paddingTop: "0.375em" }}
              className="field-body is-normal"
            >
              <div className="field">
                {this.props.datasets[this.props.dataset]["data_source"]}
              </div>
            </div>
          </div>

          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label style={{ minWidth: "100px" }} className="label">
                Description
              </label>
            </div>
            <div
              style={{ paddingTop: "0.375em" }}
              className="field-body is-normal"
            >
              <div className="field">
                {this.props.datasets[this.props.dataset]["description"]}
              </div>
            </div>
          </div>
          <TinyBarChart />
          <strong>Example Data</strong>
          <pre style={{ fontSize: "0.5em" }}>
            {JSON.stringify(
              this.props.datasets[this.props.dataset]["example_data"],
              null,
              2
            )}
          </pre>
        </div>
      </div>
    );
  }
}

export default MapPanel;
