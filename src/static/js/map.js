let map; // google.map.Map
let bounds; // bounds for autozooming of map
let locations = []; // google.maps.LatLng array
let markers = []; // google.map.Marker array

function initMap() {
	map = new google.maps.Map(document.getElementById("map"), {
		mapTypeId: 'terrain',
		disableDefaultUI: true,
	});

	const cheyenne = new google.maps.LatLng(41.14, -104.820278);
	const laramie = new google.maps.LatLng(41.311111, -105.593611);
	// const fortCollins = new google.maps.LatLng(40.559167, -105.078056);
	const boundsPadding = 15;

	locations = [cheyenne, laramie];
	bounds = findBounds(locations);
	map.fitBounds(bounds, boundsPadding);

	// This event listener will call addMarker() when the map is clicked.
	// map.addListener("click", (event) => {
	// 	addMarker(event.latLng, "another test");
	// });

	// test of combinded markers
	addMarker(laramie, "<b>April Aguilar</b><br>IN GIS/CADD Services<br>Project GIS Analyst<br>Registered Licenses:");
	addMarker(cheyenne, "<b>Willie Carpenter</b><br>PPS Mid-Continent<br>Senior Geologist/Hydrogeologistt<br>Registered Licenses: PG" +
						"<br><br>" +
						"<b>Anthony Collier</b><br>IN Water Resources<br>Senior Engineer<br>Registered Licenses:");
}

function addMarker(location, label) {
	const marker = new google.maps.InfoWindow();
	marker.setContent(label);
	marker.setPosition(location);
	marker.open(map);
	map.addListener("zoom_changed", () => {
		marker.setContent(label);
		marker.open(map);
	});
	markers.push(marker);
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

function findBounds(locations) {

	if(locations.length <= 0) {
		return;
	}

	let north = locations[0].lat();
	let south = locations[0].lat();
	let east = locations[0].lng();
	let west = locations[0].lng();

	for(i = 0; i < locations.length; i++) {
		let lat = locations[i].lat();
		let lng = locations[i].lng();
		
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