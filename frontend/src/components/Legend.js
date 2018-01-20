import React from "react";
import "./Legend.css";
import NumberFormat from "react-number-format";

class Legend extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    // console.log(this.props.colors(0));
    // console.log(this.props.colors(0.2));
    // console.log(this.props.colors(0.4));
    // console.log(this.props.colors(0.6));
    // console.log(this.props.colors(0.8));
    return (
      <div className="legend">
        <div className="layout">
          <div className="filled one-fifth zero" />
          <div className="filled one-fifth twenty" />
          <div className="filled one-fifth fourty" />
          <div className="filled one-fifth sixty" />
          <div className="filled one-fifth eighty" />
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
