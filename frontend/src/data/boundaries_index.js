const boundaries = {
	// "census_2010": {
	// 	"file": "Boundaries - Census Blocks - 2010.json",
	// 	"name": "Census Blocks",
	// 	"url": "./Boundaries+-+Census+Blocks+-+2010.json"
	// },
	// "grocery_stores": {
	// 	"file": "Grocery Stores (2013).json",
	// 	"name": "Grocery Stores",
	// 	"url": "Grocery+Stores+(2013).json"
	// },
	// "tax_increment_financing_districts": {
	// 	"file": "Boundaries - Tax Increment Financing Districts.json",
	// 	"name": "Tax Increment Financing Districts",
	// 	"url": "Boundaries+-+Tax+Increment+Financing+Districts.json"
	// },
	// "hospitals": {
	// 	"file": "Hospitals in Chicago.json",
	// 	"name": "Hospitals",
	// 	"url": "Hospitals+in+Chicago.json"
	// },
	// "metra_lines": {
	// 	"file": "Metra Lines.json",
	// 	"name": "Metra Line",
	// 	"url": "Metra+Lines.json",
	// 	"other": "not boundary"
	// },
	"community_areas": {
		"key": "community_areas",
		"file": "Boundaries - Community Areas (current).json",
		"name": "Community Areas",
		"url": "Boundaries+-+Community+Areas+(current).json",
	"other": "not working"
	},
	// "metra_stations": {
	// 	"file": "Metra Stations.json",
	// 	"name": "Metra Stations",
	// 	"url": "Metra+Stations.json"
	// 	"other": "not boundary"
	// },
	// "empowerment_zones": {
	// 	"file": "Boundaries - Empowerment Zones.json",
	// 	"name": "Empowerment Zones",
	// 	"url": "Boundaries+-+Empowerment+Zones.json"
	// },
	// "public_art": {
	// 	"file": "Parks - Public Art - Shapefiles.json",
	// 	"name": "Public Art",
	// 	"url": "Parks+-+Public+Art+-+Shapefiles.json",
	// 	"other": "not boundary"
	// },
	// "parks": {
	// 	"file": "Parks - Shapefiles.json",
	// 	"name": "Parks",
	// 	"url": "Parks+-+Shapefiles.json",
	// 	"other": "not boundary"
	// },
	// "industrial_corridors": {
	// 	"file": "Boundaries - Industrial Corridors.json",
	// 	"name": "Industrial Corridors",
	// 	"url": "Boundaries+-+Industrial+Corridors.json",
	// },
	// "cps_locations": {
	// 	"file": "CPS School Locations SY 15-16.json",
	// 	"name": "CPS School Locations (2015-2016)",
	// 	"url": "CPS+School+Locations+SY+15-16.json",
	// 	"other": "not boundary"
	// },
	// "pedestrian_streets": {
	// 	"file": "Pedestrian Streets.json",
	// 	"name": "Pedestrian Streets",
	// 	"url": "Pedestrian+Streets.json",
	// 	"other": "not boundary"
	// },
	// "cta_l_train": {
	// 	"file": "CTA - 'L' (Rail) Lines.json",
	// 	"name": "CTA Rail Lines",
	// 	"url": "CTA+-+L+(Rail)+Lines.json",
	// 	"other": "not boundary"
	// },
	// "pedway_route": {
	// 	"file": "Pedway Routes.json",
	// 	"name": "Pedway Routes",
	// 	"url": "Pedway+Routes.json",
	// 	"other": "not boundary"
	// },
	// "cta_bus_routes": {
	// 	"file": "CTA - Bus Routes.json",
	// 	"name": "Bus Routes",
	// 	"url": "CTA+-+Bus+Routes.json",
	// 	"other": "not boundary"
	// },
	// "school_grounds": {
	// 	"file": "School Grounds.json",
	// 	"name": "School Grounds",
	// 	"url": "School+Grounds.json",
	// 	"other": "not boundary"
	// },
	// "cta_bus_stops": {
	// 	"file": "CTA - Bus Stops.json",
	// 	"name": "Bus Stops",
	// 	"url": "CTA+-+Bus+Stops.json",
	// 	"other": "not boundary"
	// },
	// "street_center_lines": {
	// 	"file": "Street Center Lines.json",
	// 	"name": "Street Center Lines",
	// 	"url": "Street+Center+Lines.json",
	// 	"other": "not boundary"
	// },
	// "cta_ventra": {
	// 	"file": "CTA - Ventra .json",
	// 	"name": "Ventra Locations",
	// 	"url": "CTA+-+Ventra.json",
	// 	"other": "not boundary"
	// },
	// "ward_precincts": {
	// 	"file": "Ward Precincts.json",
	// 	"name": "Ward Precincts",
	// 	"url": "Ward+Precincts.json",
	// 	"other": "too big"
	// },
	// "bike_roues": {
	// 	"file": "Chicago Bike Routes.json",
	// 	"name": "Bike Routes",
	// 	"url": "Chicago+Bike+Routes.json",
	// 	"other": "not boundary"
	// }

	// BOUNDARIES
	"state_congressional_districts_senate": {
		"key": "state_congressional_districts_senate",
		"file": "Boundaries - State Congressional Districts (Senate).json",
		"name": "State Congressional Districts (Senate)",
		"url": "Boundaries+-+State+Congressional+Districts+(Senate).json"
	},
	"state_congressional_districts_house": {
		"key": "state_congressional_districts_house",
		"file": "Boundaries - State Congressional Districts (House).json",
		"name": "State Congressional Districts",
		"url": "State+Congressional+Districts+(Senate).json" // mabye wrong
	},
	"police_districts": {
		"key": "police_districts",
		"file": "Boundaries - Police Districts.json",
		"name": "Police Districts",
		"url": "Boundaries+-+Police+Districts.json"
	},
	"police_beats": {
		"key": "police_beats",
		"file": "Boundaries - Police Beats (current).json",
		"name": "Police Beats",
		"url": "Boundaries+-+Police+Beats+(current).json"
	},
	"us_congressional_districts": {
		"key": "us_congressional_districts",
		"file": "Boundaries - U.S. Congressional Districts.json",
		"name": "US Congressional Districts",
		"url": "Boundaries+-+U.S.+Congressional+Districts.json"
	},
	"zip_codes": {
		"key": "zip_codes",
		"file": "Boundaries - ZIP Codes.json",
		"name": "Zip Codes",
		"url": "Boundaries+-+ZIP+Codes.json"
	},
	"census_tracts": {
		"key": "census_tracts",
		"file": "Boundaries - Census Tracts - 2010.json",
		"name": "Census Tracts",
		"url": "Boundaries+-+Census+Tracts+-+2010.json"
	},
	"city": {
		"key": "city",
		"file": "Boundaries - City.json",
		"name": "City",
		"url": "Boundaries+-+City.json"
	},
	"neighborhoods": {
		"key": "neighborhoods",
		"file": "Boundaries - Neighborhoods.json",
		"name": "Neighborhoods",
		"url": "Boundaries+-+Neighborhoods.json"
	},
	"wards": {
		"key": "wards",
		"file": "Boundaries - Wards (2015-).json",
		"name": "Wards",
		"url": "Boundaries+-+Wards+(2015-).json"
	},
}

export default boundaries