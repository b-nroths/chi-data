import React from "react";

class KPIs extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      kpis: ["registration", "deal"]
    };
  }

  render() {
    return (
      <nav className="panel">
        <p className="panel-heading">KPIS</p>
        <div className="panel-block">
          <p className="control has-icons-left">
            <input
              className="input is-small"
              type="text"
              placeholder="Search"
            />
            <span className="icon is-small is-left">
              <i className="fa fa-search" />
            </span>
          </p>
        </div>
        <p className="panel-tabs">
          <a className="is-active">All</a>
          <a>Website</a>
          <a>Call Center</a>
        </p>
        <a className="panel-block is-active">
          <span className="panel-icon" />
          Registrations
        </a>
        <a className="panel-block">
          <span className="panel-icon" />
          Deals
        </a>
        <a className="panel-block">
          <span className="panel-icon" />
          Credit Applictions
        </a>
      </nav>
    );
  }
}

export default KPIs;
