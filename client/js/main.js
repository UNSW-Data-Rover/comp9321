var url = "http://127.0.0.1:5000/";

function initialize() {
    var mapProp = {
        center: new google.maps.LatLng(55.7558, 37.6173),
        zoom: 5,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
    };
    var map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
}

google.maps.event.addDomListener(window, 'load', initialize);

var v = new Vue({
    el: '#table1',
    data: {
        rows: ''
    },
    mounted: function () {
        var self = this;
        $.ajax({
            url: url + 'getallevents/',
            method: 'GET',
            success: function (data) {
                self.rows = data;
                console.log(self.rows);
            },
            error: function (error) {
                console.log(error);
            }
        });
    }
});
