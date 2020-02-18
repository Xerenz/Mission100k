var firebaseConfig = {
    apiKey: "AIzaSyABZm6Z_UOFebgfTZCarocPQEErmn9kP7U",
    authDomain: "miniproject-266317.firebaseapp.com",
    databaseURL: "https://miniproject-266317.firebaseio.com",
    projectId: "miniproject-266317",
    storageBucket: "miniproject-266317.appspot.com",
    messagingSenderId: "701603913533",
    appId: "1:701603913533:web:86cc4f92fa8529c7716f54",
    measurementId: "G-5CJF8TW6ML"
  };
  
// Initialize Firebase

firebase.initializeApp(firebaseConfig);

$(document).ready(function() {
	console.log("ready");

	window.lat = 11.637727;
    window.lng = 75.79087;

    function *enumerate(array) {
      for (let i = 0; i < array.length; i += 1){
        yield [i, array[i]];
      }
    }

    function intermediates(p1, p2, nb_points=15){
      var x_spacing = (p2["LAT"] - p1["LAT"]) / (nb_points + 1)
      var y_spacing = (p2["LONG"] - p1["LONG"]) / (nb_points + 1)

      var intermediates_ = [];
      for (let i = 1; i <= nb_points; i += 1){
        new_interim = {
          "LAT": p1["LAT"] + i * x_spacing,
          "LONG":  p1["LONG"] + i * y_spacing
        }
        intermediates_ = intermediates_.concat(new_interim);
      }
      return intermediates_;
    }

    var db = firebase.firestore();
    var json = [];

    db.collection("main_coordinates").get().then((querySnapshot) => {
        querySnapshot.forEach((doc) => {
        json.push(doc.data());
      });

      json_ = [];
      console.log(json);

    json.sort(function(a, b){ return(a.index - b.index) });

        var array = [];
        for ( let i = 0 ; i < json.length - 1; i += 1) {
		    var json_file = json[i];
		    array.push(json_file);

		    p2 = json[i + 1];
		    p1 = json_file;
		    var nb_points = 20;
		    var x_spacing = (p2["LAT"] - p1["LAT"]) / (nb_points + 1);
		    var y_spacing = (p2["LONG"] - p1["LONG"]) / (nb_points + 1);

		    var intermediates_ = [];
		    for (let i = 1; i <= nb_points; i += 1){
		        new_interim = {
		        "LAT": p1["LAT"] + i * x_spacing,
		        "LONG":  p1["LONG"] + i * y_spacing
		        }
		     
		        intermediates_ = intermediates_.concat(new_interim);
		    }

		   
		    for (let i = 0; i < intermediates_.length; i += 1){
		        array.push(intermediates_[i]);
		        // console.log(array);
		    }
     
        }
      
        var iter = { it: 0};
     
        setInterval(function() {
        pubnub.publish({channel:pnChannel, message:testCoords(iter, array)});
        }, 100);
        
    
    }).catch(function (err) {
    	console.log(err);
    })
    

   

var error_found = false;

    function testCoords(iter, coords_){
      
      try {
        window.lat = coords_[iter.it].LAT;
        window.lng = coords_[iter.it].LONG; 
        iter.it += 1;
        return {lat:window.lat, lng:window.lng};
      }
      catch(error) {
        if(error_found == false){
        error_found = true;
        iter.it -= 1;
        // console.error(error);
        console.log(iter.it);
        }
        
      }

    }

    var map;
    var mark;
    var lineCoords = [];
    var image = './../hot-balloon-icon.png';

    var initialize = function() {
      map  = new google.maps.Map(document.getElementById('map-canvas'), {center:{lat:lat,lng:lng},zoom:14});
      mark = new google.maps.Marker({
        position:{lat:lat, lng:lng},
         map:map,
         icon: image
      });
    };

    window.initialize = initialize;

    var redraw = function(payload) {
      lat = payload.message.lat;
      lng = payload.message.lng;

      map.setCenter({lat:lat, lng:lng, alt:0});
      mark.setPosition({lat:lat, lng:lng, alt:0});

      lineCoords.push(new google.maps.LatLng(lat, lng));
    
    var lineCoordinatesPath = new google.maps.Polyline({
      path: lineCoords,
      geodesic: true,
      strokeColor: '#2E10FF'
      
    });
    
    lineCoordinatesPath.setMap(map);
    lineCoordinatesPath.setOptions({strokeWeight: 2});
    };
    

    var pnChannel = "map-channel";

    var pubnub = new PubNub({
      publishKey:   'pub-c-74d501d6-2e24-4737-b432-94442bd83507',
      subscribeKey: 'sub-c-96396ae0-500d-11ea-bf00-e20787371c02'
    });

    pubnub.subscribe({channels: [pnChannel]});
    pubnub.addListener({message:redraw});

    var iter = 0;
});