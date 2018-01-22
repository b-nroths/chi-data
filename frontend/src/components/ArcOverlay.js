import React, { Component } from "react";
import { scaleQuantile } from "d3-scale";

import DeckGL, { GeoJsonLayer, ArcLayer } from "deck.gl";

export const inFlowColors = [
  [255, 255, 204],
  [199, 233, 180],
  [127, 205, 187],
  [65, 182, 196],
  [29, 145, 192],
  [34, 94, 168],
  [12, 44, 132]
];

export const outFlowColors = [
  [255, 255, 178],
  [254, 217, 118],
  [254, 178, 76],
  [253, 141, 60],
  [252, 78, 42],
  [227, 26, 28],
  [177, 0, 38]
];

export default class ArcOverlay extends Component {
  static get defaultViewport() {
    return {
      longitude: -100,
      latitude: 40.7,
      zoom: 3,
      maxZoom: 15,
      pitch: 30,
      bearing: 30
    };
  }

  constructor(props) {
    super(props);
    this.state = {
      arcs: null,
      max_value: 1000
    };
    this._onClick = this._onClick.bind(this);
  }

  componentWillReceiveProps(nextProps) {
    if (
      nextProps.data !== this.props.data ||
      nextProps.selectedFeature !== this.props.selectedFeature
    ) {
      this.setState({
        arcs: this._getArcs(nextProps)
      });
    }
  }

  _getArcs({ data, selectedFeature }) {
    if (!data || !selectedFeature) {
      return null;
    }

    const { flows, centroid } = selectedFeature.properties;

    const arcs = Object.keys(flows).map(toId => {
      const f = data[toId];
      return {
        source: centroid,
        target: f.properties.centroid,
        value: flows[toId]
      };
    });

    const scale = scaleQuantile()
      .domain(arcs.map(a => Math.abs(a.value)))
      .range(inFlowColors.map((c, i) => i));

    arcs.forEach(a => {
      a.gain = Math.sign(a.value);
      a.quantile = scale(Math.abs(a.value));
    });

    return arcs;
  }

  _getColor = r => {
    return [255, 0, 0, Math.round(255 * r/this.state.max_value)];
  };

  render() {
    const { viewport, data } = this.props;
    // const {arcs} = this.state;
    // console.log(data);
    // console.log(data);
    if (!this.state.arcs) {
      var url =
        "http://chicago.bnroths.com/data/" +
        this.props.dataset +
        "/" +
        this.props.dt +
        "/all_arcs.json";
      fetch(url).then(response => response.json()).then(json =>
        this.setState({
          arcs: json
        })
      );
      return null;
    }

    const layers = [
      new GeoJsonLayer({
        id: "geojson",
        data,
        stroked: true,
        filled: true,
        lineWidthMinPixels: 1,
        getFillColor: () => [0, 0, 0, 100],
        pickable: true,
        onClick: data => {
          this.setState({ arcs: data.object.properties.arcs, max_value: data.object.properties.max_value });
        }
        // pickable: Boolean(this.props.onHover || this.props.onClick)
      }),
      new ArcLayer({
        id: "arc",
        data: this.state.arcs,
        // getSourcePosition: d => d.source,
        // getTargetPosition: d => d.target,
        getSourceColor: d =>
          this._getColor(d.value),
        getTargetColor: d =>
          this._getColor(d.value),
        strokeWidth: 2
      })
    ];

    return <DeckGL {...viewport} layers={layers} />;
  }
}
