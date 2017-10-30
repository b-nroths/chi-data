import React from "react";
import MapGL from "react-map-gl";
import MapPanel from "./MapPanel";
import boundaries from "../data/boundaries_index";
import DeckGL, { GeoJsonLayer } from "deck.gl";

class Map extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      current_boundary: null,
      data: null,
      viewport: {
        latitude: 41.8781,
        longitude: -87.6298,
        zoom: 10,
        bearing: 0,
        pitch: 45,
        width: 500,
        height: 500
      }
      // geojson: null
    };
  }
  componentDidMount() {
    window.addEventListener("resize", this._resize);
    this._resize();
    // animation = window.requestAnimationFrame(this._animatePoint);
  }

  componentWillUnmount() {
    window.removeEventListener("resize", this._resize);
    // window.cancelAnimationFrame(animation);
  }

  didSelectBoundary = boundary => {
    fetch(
      "https://s3.amazonaws.com/chicago.bnroths.com/boundaries/" +
        boundaries[boundary]["url"]
    )
      .then(resp => resp.json())
      .then(data => this.setState({ data }));

    this.setState({
      data: boundaries[boundary]["data"],
      current_boundary: boundary
    });
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
    const { viewport, data } = this.state;
    const geosjsonLayer = new GeoJsonLayer({
      id: "geojson-layer",
      data,
      filled: true,
      stroked: false,
      extruded: true
    });

    return (
      <div>
        <MapPanel
          didSelectBoundary={this.didSelectBoundary}
          current_boundary={this.state.current_boundary}
          boundaries={boundaries}
        />
        <MapGL
          {...viewport}
          onViewportChange={this._onViewportChange}
          mapboxApiAccessToken="pk.eyJ1IjoiYm5yb3RocyIsImEiOiJjajlkMzNqMmkxdzh2MzNucmswN2dwNnc1In0.auXBo3CxsUqpDEO0g_OmnQ"
        >
          <DeckGL {...viewport} layers={[geosjsonLayer]} />
        </MapGL>
      </div>
    );
  }
}

export default Map;
