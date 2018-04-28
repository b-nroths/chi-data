import React from "react";
import { Link } from "react-router-dom";

const Header = () =>
	<nav
		className="navbar has-shadow"
		role="navigation"
		aria-label="main navigation"
	>
		<div className="navbar-brand">
			<a className="navbar-item" href="https://bulma.io">
				CHICAGO DATA
			</a>

			<Link to="/" className="navbar-item">
				Home
			</Link>
			{/*
			<Link to="/about" className="navbar-item">
				About
			</Link>
			<Link to="/map" className="navbar-item">
				Map
			</Link>
			<Link to="/data" className="navbar-item">
					Data
				</Link>*/}
		</div>
	</nav>;

export default Header;
