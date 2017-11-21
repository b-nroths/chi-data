import React from "react";
import MapGL from "react-map-gl";
import MapPanel from "./MapPanel";
import MapTimeline from "./MapTimeline";
import boundaries from "../data/boundaries_index";
// import city_small from "../data/city_small";
import DeckGL, { GeoJsonLayer, ScatterplotLayer } from "deck.gl";
// import geolib from "geolib";

const LIGHT_SETTINGS = {
  lightsPosition: [-125, 50.5, 5000, -122.8, 48.5, 8000],
  ambientRatio: 0.2,
  diffuseRatio: 0.5,
  specularRatio: 0.3,
  lightsStrength: [1.0, 0.0, 2.0, 0.0],
  numberOfLights: 2
};

class MapTracts extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      boundary: null,
      keys: null,
      year: '2002',
      current_key: null,
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
      current_data: null,
      data_for_stat: null
    };
  }
  _getElevation = data => {
    // console.log(this.state.data_for_stat)
    if (this.state.current_key === "C000") {
      var scale = 25
    }
    // console.log(data, this.state.current_key, scale, this.state.year, this.state.data_for_stat[this.state.year][data])
    return this.state.data_for_stat[this.state.year][data]/scale
    // console.log(this.data_for_stat)
    // return 100;
    
    // console.log(this.state.current_key, this.state.data_for_stat[this.state.current_key][data])
    // if (this.state.current_key) {
    //   return this.state.data_for_stat[this.state.current_key][data];
    // } else {
    //   return 100;
    // }
  };

  _getColor = data => {
    // console.log(data);
    // console.log();
    // console.log(this.state.data_for_stat[this.state.year][data])
    if (this.state.current_key === "C000") {
      var scale = 64348
    }
    var r = this.state.data_for_stat[this.state.year][data]/scale;
    return [r * 255, 140, 200 * (1 - r)];
  };

  componentDidMount() {
    window.addEventListener("resize", this._resize);
    this._resize();
    this.didSelectBoundary("census_tracts");
    this.didSelectKey("C000");
    fetch(
      "https://s3.amazonaws.com/chicago.bnroths.com/data/rac/tract_keys.json"
    )
      .then(resp => resp.json())
      .then(data => {
        // console.log(data);
        this.setState({
          keys: data
        });
      });
  }

  componentWillUnmount() {
    window.removeEventListener("resize", this._resize);
  }

  

  didSelectBoundary = boundary => {
    fetch(
      "https://s3.amazonaws.com/chicago.bnroths.com/data/boundaries/" +
        boundaries[boundary]["url"]
    )
      .then(resp => resp.json())
      .then(data => {
        this.setState({
          boundary: data,
          boundary_name: boundary
        });
        // console.log(data);
        // console.log(boundaries[boundary]["data"]);
        // console.log(boundary);
      });
  };

  didSelectKey = key => {
    console.log(key);
    fetch(
      "https://s3.amazonaws.com/chicago.bnroths.com/data/rac/" + key + ".json"
    )
      .then(resp => resp.json())
      .then(data => {
        // console.log(data);
        this.setState({ data_for_stat: data, current_key: key }, () => {
            console.log(this.state.data_for_stat)
        });
      });
  };

  didSelectYear = key => {
    console.log(key);
    // console.log(this.state.data_for_stat);
    this.setState({ year: key });
    // this.setState({ current_data: this.state.data_for_stat[key] });
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
    const { viewport, boundary, pointdata } = this.state;
    // console.log(boundary);
    const geosjsonLayer = new GeoJsonLayer({
      id: "geojson-layer",
      data: boundary,
      // opacity: 0.8,
      stroked: false,
      filled: true,
      extruded: true,
      // wireframe: true,
      fp64: true,
      lightSettings: LIGHT_SETTINGS,
      getFillColor: d => this._getColor(d.properties.geoid10),
      getElevation: d => this._getElevation(d.properties.geoid10),
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

    // console.log(this.state.keys);
    // /*
    //       */
    const years = [
      "2002",
      "2003",
      "2004",
      "2005",
      "2006",
      "2007",
      "2008",
      "2009",
      "2010",
      "2011",
      "2012"
    ];
    return (
      <div>
        <MapTimeline
          years={years}
          year={this.state.year}
          didSelectYear={this.didSelectYear}
        />
        <section className="main-content columns is-gapless is-fullheight">
          <aside className="column is-3 is-narrow-mobile is-hidden-mobile">
            {this.state.keys &&
              <MapPanel
                didSelectKey={this.didSelectKey}
                keys={this.state.keys}
              />}
          </aside>
          <div className="container column is-9">
            <MapGL
              {...viewport}
              onViewportChange={this._onViewportChange}
              mapboxApiAccessToken="pk.eyJ1IjoiYm5yb3RocyIsImEiOiJjajlkMzNqMmkxdzh2MzNucmswN2dwNnc1In0.auXBo3CxsUqpDEO0g_OmnQ"
            >
              <DeckGL {...viewport} layers={[geosjsonLayer, layer]} />
            </MapGL>
          </div>
        </section>
      </div>
    );
  }
}

export default MapTracts;
