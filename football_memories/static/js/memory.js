/**
 * [displayEvents takes in one parameter , the eventResults object,
 * and displays the event description for the events id]
 * @param eventResults [The event results object]
 */
 function displayStadium() {
 
    try {
      venue = document.getElementById("stadium").innerHTML;
      initMap(venue, "map");
    }catch (err) {
      console.log(err);
    }
  
  }
  /**
  * [initMap takes in one parameter,
  * the eventResults object and displays numbered
  * pagination for the pages of events
  * Credit: https://developers.google.com/maps/documentation/]
  * @param address [Location address]
  * @param mapId [Map ID]
  */
  function initMap(address, mapId) {
    const map = new google.maps.Map(document.getElementById(mapId), {
      zoom: 8,
      center: { lat: -34.397, lng: 150.644 },
    });
    const geocoder = new google.maps.Geocoder();
        geocodeAddress(geocoder, map, address);
  }
  
  /**
   * [geocodeAddress 
   * Credit: https://developers.google.com/maps/documentation/javascript
   * /examples/geocoding-simple#maps_geocoding_simple-javascript]
   * @param  geocoder [The geocoder object]
   * @param resultsMap [Map containing result]
   */
   function geocodeAddress(geocoder, resultsMap, address) {
    geocoder.geocode({ address: address }, (results, status) => {
      if (status === "OK") {
        resultsMap.setCenter(results[0].geometry.location);
        new google.maps.Marker({
          map: resultsMap,
          position: results[0].geometry.location,
        });
      } else {
        alert("Geocode was not successful for the following reason: " + status);
      }
    });
   }
  
   function emptyCommentField() {
    document.getElementById("comment").value = ''
}


  displayStadium()