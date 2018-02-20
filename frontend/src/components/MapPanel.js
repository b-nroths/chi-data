import React from "react";
var createReactClass = require("create-react-class");
import {
  BarChart,
  Bar,
  // XAxis,
  // YAxis,
  // CartesianGrid,
  // Tooltip,
  // Legend,
  Cell,
  ResponsiveContainer
} from "recharts";
import "./MapPanel.css";
class MapPanel extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      datasets: this.props.datasets,
      dataset: this.props.dataset,
      dt: this.props.dt,
      sub_data: this.props.datasets[this.props.dataset]["sub_data"]
    };
  }

  componentDidMount() {
    // this.setState({
    //   dts: Object.keys(this.props.datasets[this.props.dataset]["cnts"])
    // });
  }

  render() {
    var data = Object.keys(this.state.datasets[this.props.dataset]["cnts"])
      .sort()
      .map(d => ({
        dt: d,
        cnt: this.state.datasets[this.props.dataset]["cnts"][d]
      }));

    var activeIndex = Object.keys(
      this.props.datasets[this.props.dataset]["cnts"]
    ).indexOf(this.props.dt);

    const TinyBarChart = createReactClass({
      render() {
        return (
          <ResponsiveContainer width="100%" height={100}>
            <BarChart width={150} height={40} data={data}>
              <Bar isAnimationActive={false} dataKey="cnt" fill="#8884d8">
                {data.map((entry, index) =>
                  <Cell
                    cursor="pointer"
                    fill={index === activeIndex ? "#82ca9d" : "#8884d8"}
                    key={`cell-${index}`}
                  />
                )}
              </Bar>
              }
            </BarChart>
          </ResponsiveContainer>
        );
      }
    });

    var example_data = this.props.datasets[this.props.dataset]["example_data"];
    const ExampleData = createReactClass({
      render() {
        return (
          <div>
            <strong>Example Data</strong>
            <pre style={{ fontSize: "0.5em" }}>
              {JSON.stringify(example_data, null, 2)}
            </pre>
          </div>
        );
      }
    });

    var table = this.props.datasets[this.props.dataset]["table"][this.props.dt];
    const Table = createReactClass({
      render() {
        return (
          <div>
            <strong>Eigenvalues</strong>
            <table className="table is-fullwidth">
              <tbody>
                {table.map(row => {
                  return (
                    <tr key={row.key}>
                      <th>{row.name}</th>
                      <th>{row.value}</th>
                    </tr>
                  );
                })}
              </tbody>
            </table>
            
          </div>
        );
      }
    });

    console.log(this.props.dataset);
    console.log(this.props.datasets[this.props.dataset]["table"]);
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
                      {this.state.datasets &&
                        Object.keys(this.state.datasets).map(d => {
                          return (
                            <option value={d} key={d}>
                              {this.state.datasets[d]["name"]}
                            </option>
                          );
                        })}
                    </select>
                  </div>
                </div>
              </div>
            </div>
          </div>
          {this.state.datasets[this.props.dataset].sub_data.length > 0 &&
            <div className="field is-horizontal">
              <div className="field-label is-normal">
                <label style={{ minWidth: "100px" }} className="label">
                  Sub Data
                </label>
              </div>

              <div className="field-body">
                <div className="field">
                  <div className="control">
                    <div className="select">
                      <select
                        name="sub_data"
                        value={this.props.sub_data}
                        onChange={this.props.handleChange}
                      >
                        {this.state.datasets[
                          this.props.dataset
                        ].sub_data.map(d => {
                          return (
                            <option value={d["key"]} key={d["key"]}>
                              {d["name"]}
                            </option>
                          );
                        })}
                      </select>
                    </div>
                  </div>
                </div>
              </div>
            </div>}
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
                        Object.keys(
                          this.state.datasets[this.props.dataset]["cnts"]
                        )
                          .sort()
                          .map(d => {
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
                Updated
              </label>
            </div>
            <div
              style={{ paddingTop: "0.375em" }}
              className="field-body is-normal"
            >
              <div className="field">
                {this.props.datasets[this.props.dataset]["last_updated"]}
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
                {this.props.datasets[this.props.dataset]["source"]}
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
          {data.length > 0 &&
            this.props.map_type === "scatter" &&
            <TinyBarChart />}
          {this.props.map_type === "scatter" &&
            this.props.datasets[this.props.dataset]["example_data"] &&
            <ExampleData />}
          {this.props.dataset === "eigs" &&
            this.props.datasets[this.props.dataset]["table"] &&
            <Table />}
        </div>
      </div>
    );
  }
}

export default MapPanel;
