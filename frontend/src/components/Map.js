import React from "react";
import MapGL from "react-map-gl";
import DeckGL, { GeoJsonLayer, ScatterplotLayer } from "deck.gl";
import boundaries from "../data/boundaries_index";

const LIGHT_SETTINGS = {
  lightsPosition: [-125, 50.5, 5000, -122.8, 48.5, 8000],
  ambientRatio: 0.2,
  diffuseRatio: 0.5,
  specularRatio: 0.3,
  lightsStrength: [1.0, 0.0, 2.0, 0.0],
  numberOfLights: 2
};

class Map extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      current_boundary: null,
      data: null,
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
  }
  _getElevation = data => {
    console.log(data);
    console.log(this.state[data] * 10);
    return this.state.hoods[data] * 10;
  };
  _getColor = data => {
    console.log(data);
    console.log();
    var r = this.state[data] / 1477;
    return [r * 255, 140, 200 * (1 - r)];
  };
  componentDidMount() {
    window.addEventListener("resize", this._resize);
    this._resize();
    this.didSelectBoundary("census_tracts");
  }

  componentWillUnmount() {
    window.removeEventListener("resize", this._resize);
    // window.cancelAnimationFrame(animation);
  }

  didSelectBoundary = boundary => {
    fetch(
      "https://s3.amazonaws.com/chicago.bnroths.com/data/boundaries/" +
        boundaries[boundary]["url"]
    )
      .then(resp => resp.json())
      .then(data => {
        this.setState({
          data: data,
          current_boundary: boundary
        });
      });

    // this.setState({ data }));
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
    const { viewport, data, pointdata } = this.state;
    const geosjsonLayer = new GeoJsonLayer({
      id: "geojson-layer",
      data,
      opacity: 0.8,
      stroked: false,
      filled: true,
      extruded: true,
      wireframe: true,
      fp64: true,
      lightSettings: LIGHT_SETTINGS,
      updateTriggers: {
        getElevation: viewport
      }
    });

    const layer = new ScatterplotLayer({
      id: "scatterplot-layer",
      data: pointdata,
      radiusScale: 10,
      outline: false
    });

    return (
      <section className="main-content columns is-gapless is-fullheight">
        <div className="container column is-12">
          <MapGL
            {...viewport}
            onViewportChange={this._onViewportChange}
            mapboxApiAccessToken="pk.eyJ1IjoiYm5yb3RocyIsImEiOiJjajlkMzNqMmkxdzh2MzNucmswN2dwNnc1In0.auXBo3CxsUqpDEO0g_OmnQ"
          >
            <DeckGL {...viewport} layers={[geosjsonLayer, layer]} />
          </MapGL>
        </div>
      </section>
    );
  }
}

export default Map;
