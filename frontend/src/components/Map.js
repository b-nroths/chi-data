import React from "react";
import MapGL from "react-map-gl";
import MapPanel from "./MapPanel";
import MapPanel2 from "./MapPanel2";
import DeckGL, { ScatterplotLayer, GeoJsonLayer } from "deck.gl";
import config from "./config";
import "./Map.sass";
import NumberFormat from "react-number-format";
import ArcOverlay from "./ArcOverlay.js";
import _ from "lodash";
import Legend from "./Legend";

class Map extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      dataset: "lehd_rac",
      dt: "2002",
      sub_data: "C000",
      datasets: null,
      data: null,
      city: null,
      tracts: null,
      x: null,
      y: null,
      panel2: false,
      boundary: null,
      map_type: "geojson",
      hoveredObject: null,
      pointdata: [
        {
          position: [-87.9401140825, 41.6445431225],
          radius: 100,
          color: [255, 0, 0]
        },
        {
          position: [-87.9401140825, 42.023038587],
          radius: 100,
          color: [255, 0, 0]
        },
        {
          position: [-87.5241371039, 41.6445431225],
          radius: 100,
          color: [255, 0, 0]
        },
        {
          position: [-87.5241371039, 42.023038587],
          radius: 100,
          color: [255, 0, 0]
        }
      ],
      viewport: {
        latitude: 41.8781,
        longitude: -87.6298,
        zoom: 10,
        bearing: 0,
        pitch: 45,
        width: 500,
        height: 500
      },
      loading: false
    };
    this.handleChange = this.handleChange.bind(this);
    this.refreshData = this.refreshData.bind(this);
  }

  refreshData(update) {
    var url =
      "http://chicago.bnroths.com/data/" +
      update.dataset +
      "/" +
      update.dt +
      "/" +
      update.sub_data +
      ".json";
    // console.log(url)
    if (update.boundary) {
      fetch(
        "https://s3.amazonaws.com/chicago.bnroths.com/data/boundaries/tracts_" +
          update.boundary +
          ".json"
      )
        .then(response => response.json())
        .then(data => this.setState({ tracts: data }));
    }

    // console.log(json);
    fetch(url).then(response => response.json()).then(json =>
      this.setState({
        ...update,
        data: json,
        loading: false
      })
    );
  }

  handleChange(event) {
    var update = {
      dataset: this.state.dataset,
      dt: this.state.dt,
      sub_data: this.state.sub_data,
      loading: true
    };
    update[event.target.name] = event.target.value;

    // set dt to deafult
    if (event.target.name === "dataset") {
      update["map_type"] = this.state.datasets[event.target.value]["map_type"];
      update["boundary"] = this.state.datasets[event.target.value]["boundary"];
      update["dt"] = Object.keys(
        this.state.datasets[event.target.value]["cnts"]
      )[0];
      // set subdata to default
      if (this.state.datasets[event.target.value]["sub_data"].length > 0) {
        update["sub_data"] = this.state.datasets[event.target.value][
          "sub_data"
        ][0]["key"];
        update["dt"] = "2002";
      } else {
        update["sub_data"] = "all";
      }
    }
    console.log(update);
    this.refreshData(update);
  }

  componentDidMount() {
    this._resize();

    fetch(config.datasets_url)
      .then(response => response.json())
      .then(data => this.setState({ datasets: data }));

    // fetch(
    //   "https://s3.amazonaws.com/chicago.bnroths.com/data/boundaries/Boundaries+-+City.json"
    // )
    //   .then(response => response.json())
    //   .then(data => this.setState({ city: data }));

    // fetch(
    //   "https://s3.amazonaws.com/chicago.bnroths.com/data/boundaries/tracts_chicago.json"
    // )
    //   .then(response => response.json())
    //   .then(data => this.setState({ tracts: data }));

    this.refreshData({
      dataset: this.state.dataset,
      sub_data: this.state.sub_data,
      dt: this.state.dt,
      boundary: "chicago"
    });
  }

  componentWillUnmount() {
    window.removeEventListener("resize", this._resize);
    // window.cancelAnimationFrame(animation);
  }

  _getElevation = data => {
    return this.state.hoods[data] * 10;
  };

  _resize = () => {
    this.setState({
      viewport: {
        ...this.state.viewport,
        width: this.props.width || window.innerWidth,
        height: this.props.height || window.innerHeight
      }
    });
  };
  _onViewportChange = viewport => this.setState({ viewport });
  _getColor = r => {
    return [255, 0, 0, Math.round(255 * r)];
  };

  _onHover = data => {
    console.log(data);
    if (_.get(data, "object.properties.geoid10")) {
      this.setState({
        geoid10: data.object.properties.geoid10,
        x: data.x,
        y: data.y
      });
    }
  };

  _renderTooltip() {
    const { x, y, geoid10 } = this.state;
    console.log(geoid10);
    if (!geoid10) {
      return null;
    }
    const num = this.state.data.data[this.state.geoid10];
    return (
      <div className="tooltip" style={{ left: x, top: y }}>
        <div>
          <h6>Census Code</h6>
          <NumberFormat value={this.state.geoid10} displayType={"text"} />
          <h6>Count</h6>
          <NumberFormat
            value={num}
            displayType={"text"}
            thousandSeparator={true}
          />
        </div>
      </div>
    );
  }

  render() {
    // console.log(
    //   "render map",
    //   this.state.dataset,
    //   this.state.sub_data,
    //   this.state.dt,
    //   this.state.map_type
    // );
    const { viewport, data, city, tracts } = this.state;

    const cityBoundaryLayer = new GeoJsonLayer({
      id: "geojson-layer-city",
      data: city,
      filled: false,
      stroked: true,
      extruded: false,
      lineWidthScale: 10,
      lineWidthMinPixels: 5
    });

    const censusTractsLayer = new GeoJsonLayer({
      id: "geojson-layer-tracts",
      data: tracts,
      filled: true,
      stroked: true,
      extruded: false,
      lineWidthScale: 1,
      pickable: true,
      lineWidthMinPixels: 1,
      onHover: d => this._onHover(d),
      getFillColor: d =>
        this._getColor(
          this.state.data.data[d.properties.geoid10] / this.state.data.meta.top
        ),
      updateTriggers: {
        getFillColor: this.state.data
      }
    });

    const scatterplotLayer = new ScatterplotLayer({
      id: "scatterplot-layer",
      data: data,
      radiusScale: 10,
      outline: false,
      getPosition: d => [d[0], d[1], 0],
      getRadius: d => 10,
      getColor: d => [255, 0, 128]
    });

    var layers;
    if (this.state.map_type === "geojson") {
      layers = [censusTractsLayer];
    } else if (this.state.map_type === "scatter") {
      layers = [scatterplotLayer];
    } else if (this.state.map_type === "arc") {
      layers = [scatterplotLayer];
    }

    return (
      <section className="columns is-fullheight">
        <div className="column is-4 is-sidebar-menu is-hidden-mobile">
          {this.state.datasets &&
            this.state.map_type &&
            !this.state.panel2 &&
            <MapPanel
              handleChange={this.handleChange}
              datasets={this.state.datasets}
              dataset={this.state.dataset}
              dt={this.state.dt}
              map_type={this.state.map_type}
            />}
          {this.state.datasets &&
            this.state.map_type &&
            this.state.panel2 &&
            <MapPanel2 />}
        </div>
        <div className="column is-main-content">
          {this.state.loading &&
            <div className="loading">
              <a className="button is-loading">Loading</a>
            </div>}
          {_.get(this.state, "data.meta.max") &&
            <Legend colors={this._getColor} max={this.state.data.meta.max} />}

          <MapGL
            {...viewport}
            onViewportChange={this._onViewportChange}
            mapboxApiAccessToken="pk.eyJ1IjoiYm5yb3RocyIsImEiOiJjajlkMzNqMmkxdzh2MzNucmswN2dwNnc1In0.auXBo3CxsUqpDEO0g_OmnQ"
          >
            {this.state.map_type !== "arc" &&
              <DeckGL {...viewport} layers={layers} />}
            {this._renderTooltip()}
            {this.state.map_type === "arc" &&
              <ArcOverlay
                viewport={viewport}
                data={data}
                dt={this.state.dt}
                dataset={this.state.dataset}
                // selectedFeature={selectedCounty}
                // onClick={this._onClick.bind(this)}
                strokeWidth={3}
              />}
          </MapGL>
        </div>
      </section>
    );
  }
}

export default Map;
