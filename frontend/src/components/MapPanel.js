import React, { PureComponent } from "react";

// const defaultContainer = ({ children }) =>
//   <div className="control-panel">
//     {children}
//   </div>;

export default class MapPanel extends PureComponent {
  render() {
    // const Container = this.props.containerComponent || defaultContainer;

    console.log(this.props.keys);

    return (
      // <div className="container is-fluid map-panel">
      //   <div className="columns">
      //     <div className="column is-one-quarter">
      <nav className="panel map-panel">
        <p className="panel-heading">Boundaries</p>
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
          <a>Political</a>
          <a>Other</a>
        </p>
        {Object.keys(this.props.keys).map(key =>
          <a
            key={key}
            className={
              this.props.key === key ? " is-active panel-block" : "panel-block"
            }
            onClick={e => {
              this.props.didSelectKey(this.props.keys[key]["key"]);
            }}
          >
            {this.props.keys[key]["name"]}
          </a>
        )}
      </nav>
      //     </div>
      //   </div>
      // </div>
    );
  }
}
