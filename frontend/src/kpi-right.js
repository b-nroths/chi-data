import React from "react";
import Graph from "./graph";
import Tile from "./tile";
import { CSVLink } from "react-csv";

var dateFormat = require("dateformat");
// DataNav = require('./data-nav');

class KPIRight extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      items: [],
      timeframe: "month",
      trendline: true,
      previous: false,
      forecast: false,
      annotations: false,
      goal: false,
      view: "graph"
    };

    this.setTimeframe = this.setTimeframe.bind(this);
    this.setPrevious = this.setPrevious.bind(this);
    this.setTrendline = this.setTrendline.bind(this);
    this.setForecast = this.setForecast.bind(this);
    this.setAnnotations = this.setAnnotations.bind(this);
    this.setGoal = this.setGoal.bind(this);
    this.setDisplay = this.setDisplay.bind(this);
    this.setView = this.setView.bind(this);
  }

  componentDidMount() {
    // console.log('Component DID MOUNT!');
    // fetch('http://localhost:8080/get_kpi').then(response => response.json())
    //   .then(json => {
    //     this.setState({items: json});
    // })
  }

  componentWillMount() {
    // console.log('Component WILL MOUNT!')
  }

  componentWillReceiveProps(newProps) {
    // console.log('Component WILL RECIEVE PROPS!')
  }

  shouldComponentUpdate(newProps, newState) {
    return true;
  }

  componentWillUpdate(nextProps, nextState) {
    // console.log('Component WILL UPDATE!');
  }

  componentDidUpdate(prevProps, prevState) {
    // console.log('Component DID UPDATE!')
  }

  componentWillUnmount() {
    // console.log('Component WILL UNMOUNT!')
  }

  setDisplay(event) {
    this.setState({ display: event.target.value });
  }

  setTimeframe(event) {
    this.setState({ timeframe: event.target.value });
  }

  setPrevious(event) {
    const target = event.target;
    const value = target.type === "checkbox" ? target.checked : target.value;
    // const name = target.name;
    this.setState({ previous: value });
  }

  setTrendline(event) {
    const target = event.target;
    const value = target.type === "checkbox" ? target.checked : target.value;
    // const name = target.name;
    this.setState({ trendline: value });
  }

  setView(viewType) {
    // console.log(data);
    // const value = target.type === 'checkbox' ? target.checked : target.value;
    // const name = target.name;
    this.setState({ view: viewType });
  }

  setForecast(event) {
    const target = event.target;
    const value = target.type === "checkbox" ? target.checked : target.value;
    // const name = target.name;
    this.setState({ forecast: value });
  }

  setAnnotations(event) {
    const target = event.target;
    const value = target.type === "checkbox" ? target.checked : target.value;
    // const name = target.name;
    this.setState({ annotations: value });
  }

  setGoal(event) {
    const target = event.target;
    const value = target.type === "checkbox" ? target.checked : target.value;
    // const name = target.name;
    this.setState({ goal: value });
  }

  render() {
    var trendline = this.state.trendline;
    var previous = this.state.previous;
    var forecast = this.state.forecast;
    var graphs = [];
    var csvData = [];

    // prepare csv
    var first_row = [""];
    var kpis = [];
    var kpi_name_csv;
    for (kpi_name_csv in this.props.allKPIs) {
      first_row.push(kpi_name_csv);
      kpis.push(kpi_name_csv);
    }
    csvData.push(first_row);

    if (kpi_name_csv) {
      var dt;
      for (dt in this.props.allKPIs[kpi_name_csv].data.three_months.data) {
        var row;
        row = [
          this.props.allKPIs[kpi_name_csv].data.three_months.data[dt]["dt"]
        ];
        var kpi;
        for (kpi in kpis) {
          row.push(
            this.props.allKPIs[kpis[kpi]].data.three_months.data[dt]["cnt"]
          );
        }
        csvData.push(row);
      }
    }

    if (this.props.allKPIs) {
      // graphs
      if (this.state.view === "graph") {
        for (var kpi_name in this.props.allKPIs) {
          var item = this.props.allKPIs[kpi_name];
          switch (this.state.timeframe) {
            case "week":
              graphs.push(
                <Graph
                  title={item.title}
                  goal={this.state.goal}
                  allData={item}
                  trendline={trendline}
                  previous={previous}
                  forecast={forecast}
                  key={item.name}
                  data={item.data.week.data}
                  future_data={item.data.week.future_data}
                  stats={item.data}
                />
              );
              break;
            case "month":
              graphs.push(
                <Graph
                  title={item.title}
                  goal={this.state.goal}
                  allData={item}
                  trendline={trendline}
                  previous={previous}
                  forecast={forecast}
                  key={item.name}
                  data={item.data.month.data}
                  future_data={item.data.month.future_data}
                  stats={item.data}
                />
              );
              break;
            case "three_months":
              graphs.push(
                <Graph
                  title={item.title}
                  goal={this.state.goal}
                  allData={item}
                  trendline={trendline}
                  previous={previous}
                  forecast={forecast}
                  key={item.name}
                  data={item.data.three_months.data}
                  future_data={item.data.three_months.future_data}
                  stats={item.data}
                />
              );
              break;
            default:
              graphs.push(
                <Graph
                  title={item.title}
                  goal={this.state.goal}
                  allData={item}
                  trendline={trendline}
                  previous={previous}
                  forecast={forecast}
                  key={item.name}
                  data={item.data.month.data}
                  future_data={item.data.month.future_data}
                  stats={item.data}
                />
              );
          }
        }
      } else if (this.state.view === "table" && this.props.allKPIs) {
        // table
        var kpi_names = [];
        var dts = [];
        for (var k_name in this.props.allKPIs) {
          kpi_names.push(k_name);
        }
        for (var table_dt in this.props.allKPIs[kpi_names[0]]["data"][
          "three_months"
        ]["current_dts"]) {
          // console.log(dt);
          dts.push(
            this.props.allKPIs[kpi_names[0]]["data"]["three_months"][
              "current_dts"
            ][table_dt]
          );
        }
        // reverse so newest is at top;
        dts.reverse();
        graphs.push(
          <table key="table" className="table">
            <thead>
              <tr>
                <td key="date">
                  <strong>Date</strong>
                </td>
                {kpi_names.map(d => {
                  return (
                    <td key={d}>
                      <strong>
                        {this.props.allKPIs[d].title}
                      </strong>
                      <a
                        href="#"
                        className="icon is-xsmall icon-sup hint--top hint--long"
                        aria-label={
                          this.props.allKPIs[d].definition +
                          " (Updated: " +
                          this.props.allKPIs[d].updated_at +
                          " EST)"
                        }
                      >
                        {" "}<i className="fa fa-info-circle" />
                      </a>
                    </td>
                  );
                })}
              </tr>
            </thead>
            <tbody>
              {dts.map(d => {
                return (
                  <tr key={d}>
                    <th>
                      <span style={{ width: 40 + "px", float: "left" }}>
                        {dateFormat(Date.parse(d), "ddd")}
                      </span>
                      <span style={{ width: 64 + "px" }}>
                        {dateFormat(Date.parse(d), "m/d")}
                      </span>
                    </th>
                    {kpi_names.map(k => {
                      return (
                        <td>
                          {this.props.allKPIs[k]["data"]["orig_data"][d]}
                        </td>
                      );
                    })}
                  </tr>
                );
              })}
            </tbody>
          </table>
        );
      } else if (this.state.view === "television") {
        var tv_row = [];
        var graph_row = [];
        var i = 0;
        for (var kpi_name_tile in this.props.allKPIs) {
          var item_tile = this.props.allKPIs[kpi_name_tile];

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
      }
      graphs.push(tv_row);
    }

    // this is for the number of kpi string in the top bar
    var num_kpis = 0;
    var num_kpis_str = "KPIs";
    if (this.props.allKPIs) {
      num_kpis = Object.keys(this.props.allKPIs).length;
      if (num_kpis === 1) {
        num_kpis_str = "KPI ";
      }
    }

    var view_types = {
      graph: {
        icon: "fa-line-chart"
      },
      table: {
        icon: "fa-table"
      },
      television: {
        icon: "fa-television"
      }
    };
    var views = [];
    for (var view in view_types) {
      let isSelectedStyle = this.state.view === view ? " is-primary" : "";
      var view_to_push;
      if (view === "television") {
        view_to_push = (
          <p key={view} className="control">
            <a
              className={"button " + isSelectedStyle}
              onClick={e => {
                this.props.didSelectTV(true);
              }}
            >
              <span className="icon is-small">
                <i className={"fa " + view_types[view].icon} />
              </span>
            </a>
          </p>
        );
      } else {
        view_to_push = (
          <p key={view} className="control">
            <a
              className={"button " + isSelectedStyle}
              onClick={this.setView.bind(this, view)}
            >
              <span className="icon is-small">
                <i className={"fa " + view_types[view].icon} />
              </span>
            </a>
          </p>
        );
      }
      views.push(view_to_push);
    }

    return (
      <div className="column">
        <nav className="level data-nav">
          <div className="level-left">
            <div className="level-item">
              <p className="subtitle is-5" style={{ width: 60 + "px" }}>
                <strong style={{ width: 12 + "px" }}>{num_kpis}</strong>{" "}
                {num_kpis_str}
              </p>
            </div>
            <div className="level-item">
              <div className="field has-addons">
                <p className="control">
                  <span className="select">
                    <select
                      onChange={this.setTimeframe}
                      value={this.state.timeframe}
                    >
                      <option value="week">Past Week</option>
                      <option value="month">Past Month</option>
                      <option value="three_months">Past 3 Months</option>
                    </select>
                  </span>
                </p>
              </div>
            </div>
            <div className="level-item">
              <p className="control">
                <label className="checkbox">
                  <input
                    name="trendline"
                    type="checkbox"
                    checked={this.state.trendline}
                    onChange={this.setTrendline}
                  />
                  <span> Trend</span>
                </label>
              </p>
            </div>
            <div className="level-item">
              <p className="control">
                <label className="checkbox">
                  <input
                    name="forecast"
                    type="checkbox"
                    checked={this.state.forecast}
                    onChange={this.setForecast}
                  />
                  <span> Forecast</span>
                </label>
              </p>
            </div>
            {/*
        <div className="level-item">
            <p className="control">
                <label className="checkbox">
                    <input name="annotations" type="checkbox" checked={this.state.annotations} onChange={this.setAnnotations} />
                    <span> Annotations</span>
                </label>
            </p>
        </div>
        */}
            <div className="level-item">
              <p className="control">
                <label className="checkbox">
                  <input
                    name="previous"
                    type="checkbox"
                    checked={this.state.previous}
                    onChange={this.setPrevious}
                  />
                  <span> Previous</span>
                </label>
              </p>
            </div>
            <div className="level-item">
              <p className="control">
                <label className="checkbox">
                  <input
                    name="previous"
                    type="checkbox"
                    checked={this.state.goal}
                    onChange={this.setGoal}
                  />
                  <span> Goal</span>
                </label>
              </p>
            </div>
          </div>

          <div className="level-right">
            <div className="level-item">
              <div className="field has-addons">
                {views}
              </div>
            </div>
            <div className="level-item">
              <CSVLink data={csvData} filename={"vroom-kpis.csv"}>
                <div className="button is-primary is-outlined">
                  <span className="icon">
                    <i className="fa fa-download" />
                  </span>
                </div>
              </CSVLink>
            </div>
          </div>
        </nav>
        {graphs}
      </div>
    );
  }
}

export default KPIRight;
