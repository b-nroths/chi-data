// var ReactDOM = require('react-dom');
import React from "react";
import FullScreen from "./full-screen";
import BodyLeft from "./body-left";
import KPIRight from "./kpi-right";

class Data extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      allKPIs: {}, // this is what graphs
      meta: null,
      report: null,
      fullScreen: false,
      selectedKPIs: [] // this is what highlights on the left
    };
    this.didSelectKPI = this.didSelectKPI.bind(this);
    this.didSelectTV = this.didSelectTV.bind(this);
  }

  componentWillMount() {
    // var token = localStorage.getItem('kpi-token');
    fetch(
      "https://iz4gpewi73.execute-api.us-east-1.amazonaws.com/dev/get_meta",
      {
        method: "post",
        headers: {
          // 'token': token,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ kpis: ["adf_leads_autotrader"] })
      }
    )
      .then(response => response.json())
      .then(json => {
        if (json.error === "not authenticated") {
        } else {
          this.setState({ meta: json.meta });
        }
      });
  }

  didSelectReport = (selectedKPIs, ReportName) => {
    if (ReportName === this.state.report) {
      this.setState({ report: null });
      this.setState({ allKPIs: {} });
      this.setState({ selectedKPIs: [] });
    } else {
      // console.log(selectedKPIs, ReportName);
      this.setState({ allKPIs: {} });
      this.setState({ selectedKPIs: selectedKPIs });
      this.setState({ report: ReportName });
      this.didSelectKPI(selectedKPIs, "report");
    }
  };

  didSelectTV = bool => {
    if (bool) {
      fetch(
        "https://iz4gpewi73.execute-api.us-east-1.amazonaws.com/dev/get_current"
      )
        .then(response => response.json())
        .then(json => {
          if (json.error === "not authenticated") {
          } else {
            for (var kpi_name_tile in this.state.allKPIs) {
              console.log(this.state.allKPIs[kpi_name_tile]);
              var item_tile = this.state.allKPIs[kpi_name_tile];

              if (item_tile["name"] in this.state.allKPIs) {
                for (var hour in item_tile["current_data"]) {
                  item_tile["current_data"][hour]["cnt_current"] =
                    json[item_tile["name"]][hour];
                }
                item_tile["total"] = json[item_tile["name"]]["total"];
              }
            }
            this.setState({ current: json });
            this.setState({ fullScreen: true });
          }
        });
    } else {
      this.setState({ fullScreen: false });
    }
  };

  didSelectKPI = (KPIName, fromElement) => {
    if (!(fromElement === "KPI" && this.state.report)) {
      // console.log('here', this.state.selectedKPIs);
      let KPIindex = this.state.selectedKPIs.indexOf(KPIName);
      // remove kpi
      if (KPIindex !== -1) {
        // remove from sidebar
        this.state.selectedKPIs.splice(KPIindex, 1);
        this.setState({ selectedKPIs: this.state.selectedKPIs });
        // remove from graphs
        var stateObject = this.state.allKPIs;
        delete stateObject[KPIName];
        this.setState({ allKPIs: stateObject });
      } else {
        // add kpi
        //
        if (!this.state.report) {
          let selectedKPIs = this.state.selectedKPIs.concat(KPIName);
          this.setState({ selectedKPIs: selectedKPIs });
        }

        var kpiPaylod;
        if (typeof KPIName === "string") {
          kpiPaylod = [KPIName];
        } else {
          kpiPaylod = KPIName;
        }
        fetch(
          "https://iz4gpewi73.execute-api.us-east-1.amazonaws.com/dev/get_kpi",
          {
            method: "post",
            headers: {
              // 'token': token,
              Accept: "application/json",
              "Content-Type": "application/json"
            },
            body: JSON.stringify({ kpis: kpiPaylod })
          }
        )
          .then(response => response.json())
          .then(json => {
            console.log(json);

            if (json.error === "not authenticated") {
              localStorage.removeItem("kpi-token");
            } else {
              var stateObject = this.state.allKPIs;
              for (var key in json) {
                stateObject[key] = json[key];
              }

              this.setState({ allKPIs: stateObject });
            }
          });
      }
    }
  };

  render() {
    if (this.state.meta) {
      if (this.state.fullScreen) {
        return (
          <div>
            <FullScreen
              allKPIs={this.state.allKPIs}
              didSelectTV={this.didSelectTV}
            />
          </div>
        );
      } else {
        return (
          <div>
            <div className="section">
              <div className="container">
                <div className="columns">
                  <BodyLeft
                    meta={this.state.meta}
                    selectedKPIs={this.state.selectedKPIs}
                    didSelectKPI={this.didSelectKPI}
                    didSelectReport={this.didSelectReport}
                  />
                  <KPIRight
                    allKPIs={this.state.allKPIs}
                    didSelectTV={this.didSelectTV}
                  />
                </div>
              </div>
            </div>
          </div>
        );
      }
    } else {
      return (
        <section className="hero is-success is-fullheight">
          <div className="hero-body">
            <div className="container">
              <h1 className="title">
                Data Dash <a className="button is-success is-loading" />
              </h1>
            </div>
          </div>
        </section>
      );
    }
  }
}

export default Data;
