import React from "react";
import "./Legend.css";
import NumberFormat from "react-number-format";

class Legend extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    var zero = this.props.colors(0.0);
    var twenty = this.props.colors(0.2);
    var fourty = this.props.colors(0.4);
    var sixty = this.props.colors(0.6);
    var eighty = this.props.colors(0.8);
    
    return (
      <div className="legend">
        <div className="layout">
          <div
            className="filled one-fifth"
            style={{
              background:
                "rgba(" +
                zero[0] +
                "," +
                zero[1] +
                "," +
                zero[2] +
                "," +
                (zero[3] / 255).toFixed(2) +
                ")"
            }}
          />
          <div
            className="filled one-fifth"
            style={{
              background:
                "rgba(" +
                twenty[0] +
                "," +
                twenty[1] +
                "," +
                twenty[2] +
                "," +
                (twenty[3] / 255).toFixed(2) +
                ")"
            }}
          />
          <div
            className="filled one-fifth"
            style={{
              background:
                "rgba(" +
                fourty[0] +
                "," +
                fourty[1] +
                "," +
                fourty[2] +
                "," +
                (fourty[3] / 255).toFixed(2) +
                ")"
            }}
          />
          <div
            className="filled one-fifth"
            style={{
              background:
                "rgba(" +
                sixty[0] +
                "," +
                sixty[1] +
                "," +
                sixty[2] +
                "," +
                (sixty[3] / 255).toFixed(2) +
                ")"
            }}
          />
          <div
            className="filled one-fifth"
            style={{
              background:
                "rgba(" +
                eighty[0] +
                "," +
                eighty[1] +
                "," +
                eighty[2] +
                "," +
                (eighty[3] / 255).toFixed(2) +
                ")"
            }}
          />
        </div>
        <div className="layout">
          <div className="one-fifth">
            <NumberFormat
              value={0}
              displayType={"text"}
              thousandSeparator={true}
              decimalScale={0}
            />
          </div>
          <div className="one-fifth">
            <NumberFormat
              value={0.2 * this.props.max}
              displayType={"text"}
              thousandSeparator={true}
              decimalScale={0}
            />
          </div>
          <div className="one-fifth">
            <NumberFormat
              value={0.4 * this.props.max}
              displayType={"text"}
              thousandSeparator={true}
              decimalScale={0}
            />
          </div>
          <div className="one-fifth">
            <NumberFormat
              value={0.6 * this.props.max}
              displayType={"text"}
              thousandSeparator={true}
              decimalScale={0}
            />
          </div>
          <div className="one-fifth">
            <NumberFormat
              value={0.8 * this.props.max}
              displayType={"text"}
              thousandSeparator={true}
              decimalScale={0}
            />
          </div>
        </div>
      </div>
    );
  }
}

export default Legend;
