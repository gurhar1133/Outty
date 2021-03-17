// var x = document.getElementById("demo");
var y = document.getElementById("demo2");

// https://www.w3schools.com/html/html5_geolocation.asp
// use this to convert to city, state, country, location:
// https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=29.739770399999998&longitude=-95.3797993&localityLanguage=en

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else {
    y.innerHTML = "Geolocation is not supported by this browser.";
  }
}

function showPosition(position) {
  // x.innerHTML = "Latitude: " + position.coords.latitude +
  //   "<br>Longitude: " + position.coords.longitude;

  fetch('https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=' + '29.739770399999998' + '&longitude=' + '-95.3797993' + '&localityLanguage=en')
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      // Work with JSON data here
      console.log(data.city);
      console.log(data.principalSubdivision);
      y.innerHTML = 'Detected location: ' + data.city + ', ' + data.principalSubdivision;

    })
    .catch((err) => {
      // Do something for an error here
    })
}

getLocation();