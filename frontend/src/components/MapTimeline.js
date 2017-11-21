import React from "react";

class MapTimeline extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  componentDidMount() {}

  componentWillUnmount() {}

  render() {
    // console.log(this.props.year);
    return (
      <nav className="level">
        <div className="field has-addons">
          {this.props.years.map(key =>
            <p className="control">
              <a
                key={key}
                className={
                  this.props.year === key ? "button is-primary" : "button"
                }
                onClick={e => {
                  this.props.didSelectYear(key);
                }}
              >
                <span>
                  {key}
                </span>
              </a>
            </p>
          )}
        </div>
      </nav>
    );
  }
}

export default MapTimeline;
