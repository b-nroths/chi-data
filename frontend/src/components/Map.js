import React from "react";
import MapGL from "react-map-gl";
import MapPanel from "./MapPanel";
import DeckGL, { ScatterplotLayer, GeoJsonLayer } from "deck.gl";
import config from "./config";

class Map extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      dataset: "food_inspections",
      dt: "2010-01",
      datasets: null,
      data: null,
      city: null,
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
      }
    };
    this.handleChange = this.handleChange.bind(this);
    this.refreshData = this.refreshData.bind(this);
  }

  refreshData() {
    var year = this.state.dt.split("-")[0];
    var month = this.state.dt.split("-")[1];
    console.log(year, month);
    fetch(
      "http://chicago.bnroths.com/data/" +
        this.state.dataset +
        "/" +
        year +
        "/" +
        month +
        ".json"
    )
      .then(response => response.json())
      // .then(data => console.log(data))
      .then(json => this.setState({ data: json }));
  }
  handleChange(event) {
    this.setState(
      {
        [event.target.name]: event.target.value
      },
      this.refreshData()
    );
  }

  componentDidMount() {
    this._resize();

    fetch(config.datasets_url)
      .then(response => response.json())
      .then(data => this.setState({ datasets: data }));

    fetch(
      "https://s3.amazonaws.com/chicago.bnroths.com/data/boundaries/Boundaries+-+City.json"
    )
      .then(response => response.json())
      .then(data => this.setState({ city: data }));
    this.refreshData();
  }

  componentWillUnmount() {
    window.removeEventListener("resize", this._resize);
    // window.cancelAnimationFrame(animation);
  }

  _getElevation = data => {
    console.log(data);
    console.log(this.state[data] * 10);
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
  render() {
    const { viewport, data, city } = this.state;
    const geosjsonLayer = new GeoJsonLayer({
      id: "geojson-layer",
      data: city,
      filled: false,
      stroked: true,
      extruded: false,
      // lineWidthScale: 10,
      lineWidthMinPixels: 5
      // updateTriggers: {
      //   getElevation: viewport
      // }
    });
    // const pointLayer = new ScatterplotLayer({
    //   id: "scatterplot-layer",
    //   data: pointdata,
    //   radiusScale: 10,
    //   outline: false
    // });
    // console.log(city)
    const layer = new ScatterplotLayer({
      id: "scatterplot-layer",
      data: data,
      radiusScale: 10,
      outline: false,
      getPosition: d => [d[0], d[1], 0],
      getRadius: d => 10,
      getColor: d => [255, 0, 128]
    });

    return (
      <section className="main-content columns is-gapless is-fullheight">
        <aside className="column is-4">
          {this.state.datasets &&
            <MapPanel
              handleChange={this.handleChange}
              didSelectKey={this.didSelectKey}
              datasets={this.state.datasets}
              dataset={this.state.dataset}
              dt={this.state.dt}
            />}
        </aside>
        <div className="container column is-8">
          <MapGL
            {...viewport}
            onViewportChange={this._onViewportChange}
            mapboxApiAccessToken="pk.eyJ1IjoiYm5yb3RocyIsImEiOiJjajlkMzNqMmkxdzh2MzNucmswN2dwNnc1In0.auXBo3CxsUqpDEO0g_OmnQ"
          >
            <DeckGL {...viewport} layers={[layer, geosjsonLayer]} />
          </MapGL>
        </div>
      </section>
    );
  }
}

export default Map;
