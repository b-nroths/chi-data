import React from "react";
import { Switch, Route } from "react-router-dom";
import Home from "./Home";
import About from "./About";
import Map from "./Map";
import MapBoundaries from "./MapBoundaries";
import MapTracts from "./MapTracts";
import Data from "./Data";

const Main = () =>
	<main>
		<Switch>
			<Route path="/about" component={About} />
			<Route path="/map/boundaries" component={MapBoundaries} />
			<Route path="/map/tracts" component={MapTracts} />
			<Route path="/map" component={Map} />
			<Route path="/data" component={Data} />
			<Route path="/" component={Home} />
		</Switch>
	</main>;

export default Main;
