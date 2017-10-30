import React from "react";

class BodyLeft extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      searchString: "",
      category: null,
      report: null
    };
    this.onSearchChange = this.onSearchChange.bind(this);
    this.onCategoryClick = this.onCategoryClick.bind(this);
    this.onReportClick = this.onReportClick.bind(this);
  }

  onSearchChange(event) {
    if (!this.state.report) {
      this.setState({ searchString: event.target.value });
    }
  }

  onCategoryClick(data) {
    if (!this.state.report) {
      if (this.state.category === data) {
        this.setState({ category: null });
      } else {
        this.setState({ category: data });
      }
    }
  }

  onReportClick(data) {
    if (this.state.report === data) {
      this.setState({ report: null });
    } else {
      this.setState({ report: data });
    }
  }

  render() {
    var searchString = this.state.searchString.trim().toLowerCase();
    var kpi_elements = [];

    for (let kpi in this.props.meta.kpis) {
      let k = this.props.meta.kpis[kpi];
      let kpi_name = this.props.meta.kpis[kpi].name;
      var include = false;

      if (this.state.report) {
        // include = true;
        if (this.props.meta.kpis[kpi].reports.indexOf(this.state.report) >= 0) {
          include = true;
          this.props.selectedKPIs.push(kpi_name);
          // this.setState({report: null});
          // this.props.didSelectKPI(kpi_name);
        } else {
        }
      } else {
        // filter countries list by value from input box
        if (searchString.length < 2) {
          include = true;
        } else {
          // if search string is greater than two than search name
          if (kpi_name.search(searchString) > -1) {
            include = true;
          }
        }

        // if we still include then filter out category if category is chosen
        if (this.state.category && include) {
          if (k.categories.indexOf(this.state.category) >= 0) {
            include = true;
          } else {
            include = false;
          }
        }
      }

      if (include) {
        let isSelectedStyle = this.props.selectedKPIs.includes(kpi_name)
          ? " is-active"
          : "";
        console.log(k.current);

        if (k.current) {
          kpi_elements.push(
            <a
              onClick={e => {
                this.props.didSelectKPI(kpi_name, "KPI");
              }}
              key={kpi_name}
              className={"panel-block" + isSelectedStyle}
            >
              {k.title}
              <i
                className="fa fa-bolt is-xsmall icon-supp"
                aria-hidden="true"
              />
            </a>
          );
        } else {
          kpi_elements.push(
            <a
              onClick={e => {
                this.props.didSelectKPI(kpi_name, "KPI");
              }}
              key={kpi_name}
              className={"panel-block" + isSelectedStyle}
            >
              {k.title}
            </a>
          );
        }
      }
    }

    return (
      <div className="column is-one-quarter">
        <nav className="panel">
          <p className="panel-heading">KPIs</p>
          <div className="panel-block">
            <p className="control has-icons-left">
              <input
                className="input is-small"
                type="text"
                placeholder="Search"
                onChange={this.onSearchChange}
                value={this.state.searchString}
                disabled={this.state.report ? true : false}
              />
              <span className="icon is-small is-left">
                <i className="fa fa-search" />
              </span>
            </p>
          </div>
          <p className="panel-tabs">
            {this.props.meta.categories.map(d => {
              return (
                <a
                  key={d}
                  className={this.state.category === d ? " is-active" : ""}
                  onClick={this.onCategoryClick.bind(this, d)}
                >
                  {d}
                </a>
              );
            })}
          </p>
          <div
            style={{
              maxHeight: 450 + "px",
              overflowY: "scroll",
              borderBottom: "1px solid #dbdbdb"
            }}
          >
            {kpi_elements}
          </div>
        </nav>

        <nav className="panel">
          <p className="panel-heading">Reports</p>

          <div
            style={{
              maxHeight: 450 + "px",
              overflowY: "scroll",
              borderBottom: "1px solid #dbdbdb"
            }}
          >
            {Object.keys(this.props.meta.reports).map(d => {
              return (
                <a
                  key={d}
                  className={
                    this.state.report === d
                      ? " is-active panel-block"
                      : "panel-block"
                  }
                  // onClick={this.onReportClick.bind(this,d)}
                  onClick={e => {
                    this.props.didSelectReport(this.props.meta.reports[d], d);
                    this.onReportClick(d);
                  }}
                >
                  {d}
                </a>
              );
            })}
          </div>
        </nav>
      </div>
    );
  }
}

export default BodyLeft;
