function initialize() {

    var initialLocation;
    var hongkong = new google.maps.LatLng(22.280490, 114.181512);
    var browserSupportFlag = new Boolean();


    var myOptions = {
        zoom: 12,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById("map"), myOptions);


    // Try W3C Geolocation (Preferred)
    if (navigator.geolocation) {
        browserSupportFlag = true;
        navigator.geolocation.getCurrentPosition(function (position) {
            initialLocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
            map.setCenter(initialLocation);
        }, function () {
            handleNoGeolocation(browserSupportFlag);
        });
    }

    // Browser doesn't support Geolocation
    else {
        browserSupportFlag = false;
        handleNoGeolocation(browserSupportFlag);
    }

    function handleNoGeolocation(errorFlag) {
        if (errorFlag == true) {
            alert("Geolocation service failed.");
            initialLocation = hongkong;
        } else {
            alert("Your browser doesn't support geolocation. We've placed you in Siberia.");
            initialLocation = hongkong;
        }
        map.setCenter(initialLocation);
    }

    // Create the search box and link it to the UI element.
    var input = document.getElementById('mapsearch');
    var searchBox = new google.maps.places.SearchBox(input);
    // map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

    // Bias the SearchBox results towards current map's viewport.
    map.addListener('bounds_changed', function () {
        searchBox.setBounds(map.getBounds());
    });

    var markers = [];
    // Listen for the event fired when the user selects a prediction and retrieve
    // more details for that place.
    searchBox.addListener('places_changed', function () {
        var places = searchBox.getPlaces();

        if (places.length == 0) {
            return;
        }

        // Clear out the old markers.
        markers.forEach(function (marker) {
            marker.setMap(null);
        });
        markers = [];

        // For each place, get the icon, name and location.
        var bounds = new google.maps.LatLngBounds();

        var i = 0;
        // forEach loop
        places.forEach(function (place) {
            i += 1;
            var icon = {
                url: place.icon,
                size: new google.maps.Size(71, 71),
                origin: new google.maps.Point(0, 0),
                anchor: new google.maps.Point(17, 34),
                scaledSize: new google.maps.Size(25, 25)
            };

            var content = '<div class= "window">' +
                '<h3>' + place.name + '</h3>' +
                '<p>' + place.formatted_address + '<br>'
                + place.formatted_phone_number + '</p>'+
                    '<button class="btn btn-info populate" index_id="'
                +i+'" id="populate">Populate</button>'

                '</div>'


            var infowindow = new google.maps.InfoWindow({
                content: content
            });

            // Create a marker for each place.
            var marker = new google.maps.Marker({
                map: map,
                icon: icon,
                title: place.name,
                position: place.geometry.location
            });

            marker.addListener('click', function () {
                infowindow.open(map, marker);
            });

            markers.push(marker)

            if (place.geometry.viewport) {
                // Only geocodes have viewport.
                bounds.union(place.geometry.viewport);
            } else {
                bounds.extend(place.geometry.location);
            }

            console.log(place)
            console.log(place.formatted_address)
        }); // end for


        map.fitBounds(bounds);

        $(document).on('click', '.populate', function(){
            marker_index= $(this).attr("index_id")
            place= places[marker_index-1];
            $('#id_name').val(place.name);
            $("#id_address").val(place.formatted_address);
            

        });



    });

}

google.maps.event.addDomListener(window, 'load', initialize);


