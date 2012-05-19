function make_widget() {
    var map;
    var map_container = this;
    var hidden = $(map_container).siblings("input[type=hidden]");
    var latlng = hidden.val().split(',');
    var lat = parseFloat(latlng[0]);
    var lng = parseFloat(latlng[1]);

    function savePosition(point) {
        hidden.val(point.lat().toFixed(6) + "," + point.lng().toFixed(6));
        map.panTo(point);
    }

    var point = new google.maps.LatLng(lat, lng);

    var options = {
        zoom: 8,
        center: point,
        mapTypeId: google.maps.MapTypeId.ROADMAP
        // mapTypeControl: true,
        // navigationControl: true
    };
    
    console.log(map_container.find);		
    map = new google.maps.Map(map_container, options);

    var marker = new google.maps.Marker({
        map: map,
        position: new google.maps.LatLng(lat, lng),
        draggable: true
        
    });
    /*
    google.maps.event.addListener(marker, 'dragend', function(mouseEvent) {
        savePosition(mouseEvent.latLng);
    });
    */

    /*
    google.maps.event.addListener(map, 'click', function(mouseEvent){
        marker.setPosition(mouseEvent.latLng);
        savePosition(mouseEvent.latLng);
    });
    */
}

$(document).ready(function() {
    $(".googlemap").each(make_widget);
});

    
