let map; // google.map.Map
let dbReturn = []; // array of employee data
let markers = {}; // google.map.Marker array
let employees = []; // array of employees description and location
let bounds; // bounds for autozooming of map
let latLngs = [];

let citiesDB = {};

function initMap() {
	map = new google.maps.Map(document.getElementById('map'), {
		mapTypeId: 'terrain',
		disableDefaultUI: true,
	});

	// db simulated employee query return:
	let employee1 = {fname: 'April', lname: 'Aguilar', Unit: 'IN GIS/CADD Services', City: 'Laramie', State: 'Wyoming', Title: 'Project GIS Analyst', Licenses: '', Skills: 'Geologist'};
	let employee2 = {fname: 'Isaac', lname: 'Baldwin', Unit: 'ICE Technical Services', City: 'Laramie', State: 'Wyoming', Title: 'Senior Geologist/Hydrogeologist', Licenses: 'PG', Skills: ''};
	let employee3 = {fname: 'Brendan', lname: 'Ball', Unit: 'Business Development and Marketing (BDM)', City: 'Fort Collins', State: 'Colorado', Title: 'Senior BD Specialist', Licenses: '', Skills: 'Contaminant Modeling'};
	let employee4 = {fname: 'Wayne', lname: 'Carlson', Unit: 'PPS Mid-Continent', City: 'Cheyenne', State: 'Wyoming', Title: 'Associate Geologist', Licenses: 'P.G.', Skills: ''};
	dbReturn = [employee1, employee2, employee3, employee4];

	// db simulated query return:
	citiesDB['Laramie, Wyoming'] = {lat: 41.311111, lng: -105.593611};
	citiesDB['Fort Collins, Colorado'] = {lat: 40.559167, lng: -105.078056};
	citiesDB['Cheyenne, Wyoming']  = {lat: 41.14, lng: -104.820278};

	// make employees list
	for(let i = 0; i < dbReturn.length; i++) {
		let employee = {};
		employee.description = getDescription(dbReturn[i]); // employee description shown on map marker
		employee.location = getLocation(dbReturn[i]); // location city, name string
		employee.latLng = getLatLng(dbReturn[i]);
		employees.push(employee);
	}

	// make markers list
	for(let i = 0; i < employees.length; i++) {
		employee = employees[i];
		if(employee.location in markers) {
			// add to existing marker
			markers[employee.location].description += '<br><br>' + employee.description;
		} else {
			// add new marker
			let marker = {};
			marker.description = employee.description;
			marker.latLng = employee.latLng;
			marker.InfoWindow = new google.maps.InfoWindow();
			latLngs.push(employee.latLng);
			markers[employee.location] = marker;
		}
	}

	// display all markers on map
	for(const [key, value] of Object.entries(markers)) {
		addMarker(value);
	}

	// Autofit map
	const boundsPadding = 35;
	bounds = findBounds(latLngs);
	map.fitBounds(bounds, boundsPadding);
}

// generates employee description to be displayed on map
function getDescription(employee) {
	let name = employee.fname + ' ' + employee.lname;
	let results = '<b>' + name + '</b><br>' +
					employee.Unit + '<br>' +
					employee.Title + '<br>' +
					'Licenses: ' + employee.Licenses;
	return results;
}

// returns city, state string from employee db entry
function getLocation(employee) {
	return employee.City + ', ' + employee.State;
}

// return maps.google.LatLng literal
function getLatLng(employee) {
	let city = employee.City + ', ' + employee.State;
	return citiesDB[city];
}

function addMarker(marker) {
	marker.InfoWindow.setContent(marker.description);
	marker.InfoWindow.setPosition(marker.latLng);
	marker.InfoWindow.open(map);
}

// Sets the map on all markers in the array.
function setMapOnAll(map) {
	for (let i = 0; i < markers.length; i++) {
		markers[i].setMap(map);
	}
}

// Removes the markers from the map, but keeps them in the array.
function clearMarkers() {
	setMapOnAll(null);
}

// Shows any markers currently in the array.
function showMarkers() {
	setMapOnAll(map);
}

function deleteMarker() {
	let newMarkers = [];
}

// Deletes all markers in the array by removing references to them.
function deleteMarkers() {
	clearMarkers();
	markers = [];
}

// Takes all locations and finds the min/max of all lat/lngs to find north, south, east, and west bounds
// returns as a google.maps.latLng literal
function findBounds(locations) {

	if(locations.length <= 0) {
		return;
	}

	let north = locations[0].lat;
	let south = locations[0].lat;
	let east = locations[0].lng;
	let west = locations[0].lng;

	for(let i = 0; i < locations.length; i++) {
		let lat = locations[i].lat;
		let lng = locations[i].lng;
		
		// north bounds
		if(lat > north) {
			north = lat;
		}
		// south bounds
		if(lat < south) {
			south = lat;
		}
		// east bounds
		if(lng > east) {
			east = lng;
		}
		// west bounds
		if(lng < west) {
			west = lng;
		}
	}

	return {north: north, south: south, east: east, west: west};
}