import React from "react";
import MapGL from "react-map-gl";
import MapPanel from "./MapPanel";
import MapTimeline from "./MapTimeline";
import boundaries from "../data/boundaries_index";
import city_small from "../data/city_small";
import DeckGL, { GeoJsonLayer, ScatterplotLayer } from "deck.gl";
import geolib from "geolib";

const LIGHT_SETTINGS = {
  lightsPosition: [-125, 50.5, 5000, -122.8, 48.5, 8000],
  ambientRatio: 0.2,
  diffuseRatio: 0.5,
  specularRatio: 0.3,
  lightsStrength: [1.0, 0.0, 2.0, 0.0],
  numberOfLights: 2
};

class MapBoundaries extends React.Component {
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
      },
      hoods: {
        "Albany Park": 195,
        Andersonville: 36,
        "Archer Heights": 80,
        "Armour Square": 72,
        Ashburn: 197,
        "Auburn Gresham": 632,
        Austin: 1477,
        "Avalon Park": 101,
        Avondale: 265,
        "Belmont Cragin": 423,
        Beverly: 95,
        Boystown: 23,
        Bridgeport: 167,
        "Brighton Park": 266,
        Bucktown: 118,
        Burnside: 34,
        "Calumet Heights": 142,
        Chatham: 507,
        "Chicago Lawn": 629,
        Chinatown: 34,
        Clearing: 134,
        Douglas: 499,
        Dunning: 169,
        "East Side": 141,
        "East Village": 54,
        Edgewater: 243,
        "Edison Park": 25,
        Englewood: 1225,
        "Fuller Park": 110,
        "Gage Park": 234,
        Galewood: 49,
        "Garfield Park": 753,
        "Garfield Ridge": 246,
        "Gold Coast": 53,
        "Grand Boulevard": 557,
        "Grand Crossing": 591,
        "Grant Park": 6,
        Greektown: 10,
        Hegewisch: 52,
        Hermosa: 161,
        "Humboldt Park": 995,
        "Hyde Park": 148,
        "Irving Park": 315,
        "Jackson Park": 11,
        "Jefferson Park": 103,
        Kenwood: 136,
        "Lake View": 423,
        "Lincoln Park": 239,
        "Lincoln Square": 204,
        "Little Italy, UIC": 278,
        "Little Village": 414,
        "Logan Square": 563,
        Loop: 528,
        "Lower West Side": 279,
        "Magnificent Mile": 102,
        "Mckinley Park": 120,
        "Millenium Park": 3,
        Montclare: 54,
        "Morgan Park": 193,
        "Mount Greenwood": 65,
        "Museum Campus": 10,
        "Near South Side": 213,
        "New City": 550,
        "North Center": 180,
        "North Lawndale": 628,
        "North Park": 102,
        "Norwood Park": 88,
        "O'Hare": 126,
        Oakland: 96,
        "Old Town": 108,
        "Portage Park": 331,
        "Printers Row": 14,
        Pullman: 76,
        "River North": 485,
        Riverdale: 153,
        "Rogers Park": 471,
        Roseland: 637,
        "Rush & Division": 82,
        "Sauganash,Forest Glen": 30,
        "Sheffield & DePaul": 41,
        "South Chicago": 443,
        "South Deering": 141,
        "South Shore": 772,
        Streeterville: 93,
        "Ukrainian Village": 70,
        "United Center": 238,
        Uptown: 447,
        "Washington Heights": 221,
        "Washington Park": 302,
        "West Elsdon": 66,
        "West Lawn": 159,
        "West Loop": 217,
        "West Pullman": 369,
        "West Ridge": 245,
        "West Town": 260,
        "Wicker Park": 314,
        Woodlawn: 450,
        Wrigleyville: 32
      } // geojson: null
    };
  }
  _getElevation = data => {
    return this.state.hoods[data] * 10;
  };
  _getColor = data => {
    // console.log(data);
    // console.log();
    var r = this.state[data] / 1477;
    return [r * 255, 140, 200 * (1 - r)];
  };
  componentDidMount() {
    window.addEventListener("resize", this._resize);
    this._resize();
    this.didSelectBoundary("neighborhoods");
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
      .then(data => this.setState({ data }));

    this.setState({
      data: boundaries[boundary]["data"],
      current_boundary: boundary
    });
  }
  didSelectKey = key => {
    console.log(key);
    this.didSelectBoundary(key);
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
      getFillColor: d => this._getColor(d.properties.pri_neigh),
      getElevation: d => this._getElevation(d.properties.pri_neigh),
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

    console.log(this.state.current_boundary);
    /*
          */
    return (
      <section className="main-content columns is-gapless is-fullheight">
        <aside className="column is-3 is-narrow-mobile is-hidden-mobile">
          <MapPanel
            didSelectKey={this.didSelectKey}
            key={this.state.current_boundary}
            keys={boundaries}
          />
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
    );
  }
}

export default MapBoundaries;
