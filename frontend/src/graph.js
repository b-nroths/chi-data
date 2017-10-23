import React from "react";
import {
  LineChart,
  ReferenceLine,
  ErrorBar,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from "recharts";

class Graph extends React.Component {
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
    // console.log(this.props.future_data);
    var lines = [<Line key="cnt" dataKey="cnt" stroke="#8884d8" />];
    var data = this.props.data;
    if (this.props.previous) {
      lines.push(
        <Line key="prev_cnt" dataKey="prev_cnt" stroke="#82ca9d" />
      );
    }

    if (this.props.trendline) {
      lines.push(
        <Line
          type="linear"
          key="trendline"
          dataKey="trendline"
          stroke="#3273dc"
          dot={false}
        />
      );
    }

    // console.log('goal');
    // console.log(this.props.goal);

    if (this.props.goal) {
      // console.log(this.props.allData)
      lines.push(
        <ReferenceLine
          key="refLine"
          y={this.props.allData.goal}
          stroke="green"
          label="Goal"
        />
      );
    }
    // console.log(this.props.forecast);
    if (this.props.forecast) {
      // console.log(data);
      var a = data[data.length - 1].dt;
      // console.log(this.props.future_data);
      data = data.concat(this.props.future_data);

      lines.push(
        <Line
          type="linear"
          key="future_cnt"
          dataKey="future_cnt"
          stroke="#3273dc"
          dot={true}
        >
          <ErrorBar
            key="error"
            dataKey="error"
            width={4}
            strokeWidth={2}
            direction="y"
          />
        </Line>
      );

      lines.push(
        <ReferenceLine key="refLine" x={a} stroke="green" label="Min PAGE" />
      );
    }

    // console.log(data);
    return (
      <div>
        <div className="modal">
          <div className="modal-background" />
          <div className="modal-card">
            <header className="modal-card-head">
              <p className="modal-card-title">Modal title</p>
              <button className="delete" />
            </header>
            <section className="modal-card-body" />
            <footer className="modal-card-foot">
              <a className="button is-success">Save changes</a>
              <a className="button">Cancel</a>
            </footer>
          </div>
        </div>

        <div className="card graph">
          <header className="card-header">
            <p className="card-header-title">
              {this.props.title}{" "}
              <a
                href="#"
                className="icon is-xsmall icon-sup hint--top hint--long"
                aria-label={
                  this.props.allData.definition +
                  " (Updated: " +
                  this.props.allData.updated_at +
                  " EST)"
                }
              >
                {" "}<i className="fa fa-info-circle" />
              </a>
            </p>
            <a className="card-header-icon">
              <span className="icon">
                <i className="fa fa-angle-down" />
              </span>
            </a>
          </header>
          <div className="card-content">
            <div className="content">
              <div className="graph-container">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart
                    data={data}
                    margin={{ top: 0, right: 0, left: 0, bottom: 0 }}
                  >
                    <XAxis
                      axisLine={false}
                      tickLine={false}
                      mirror={true}
                      dataKey="dt"
                    />
                    <YAxis
                      axisLine={false}
                      tickLine={false}
                      mirror={true}
                      domain={[0, "dataMax"]}
                    />
                    <CartesianGrid strokeDasharray="3 3" />
                    <Tooltip />
                    {lines}
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
          <footer className="card-footer">
            <div className="card-footer-item has-text-centered">
              <div>
                <p className="heading">W/W</p>
                <p className="title">
                  {this.props.stats.wow_change}%
                </p>
                <p>
                  {this.props.stats.wow_diff}/day
                </p>
              </div>
            </div>
            <div className="card-footer-item has-text-centered">
              <div>
                <p className="heading">M/M</p>
                <p className="title">
                  {this.props.stats.mom_change}%
                </p>
                <p>
                  {this.props.stats.mom_diff}/day
                </p>
              </div>
            </div>
            <div className="card-footer-item has-text-centered">
              <div>
                <p className="heading">3M/3M</p>
                <p className="title">
                  {this.props.stats.tot_change}%
                </p>
                <p>
                  {this.props.stats.tot_diff}/day
                </p>
              </div>
            </div>
          </footer>
        </div>
      </div>
    );
  }
}

export default Graph;
