var url = "http://127.0.0.1:5000/";

var myCenter=new google.maps.LatLng(55.7558, 37.6173);

function initialize() {
    var mapProp = {
      center:myCenter,
      zoom:10,
      mapTypeId:google.maps.MapTypeId.ROADMAP
      };

    var map=new google.maps.Map(document.getElementById("googleMap"),mapProp);

    var points = [ new google.maps.LatLng(55.810979, 37.523728),
                    new google.maps.LatLng(55.715979, 37.543728)];
    var infowindow = new google.maps.InfoWindow();
    markers = [];
    for(var i = 0;i<points.length; i++){
        var gmarker = new google.maps.Marker({
            position : points[i],
            // title:'dasfasdg',
            map : map
        });
        markers.push(gmarker);
        google.maps.event.addListener(gmarker, 'click', function() {
              infowindow.setContent('<div><strong>' + "Stadium name" + '</strong><br>' +
                'Address: ' + "20 Street..." + '<br></div>');
              infowindow.open(map, this);
        });
    }
    setVeiwPort();
}

var setVeiwPort = function () {
    var bounds = new google.maps.LatLngBounds();
    for(var i = 0;i < markers.length;i++){
        bounds.extend(markers[i].getPosition());
    }
    map.fitBounds(bounds);
};

google.maps.event.addDomListener(window, 'load', initialize);




var v = new Vue({
    el: '#index',
    data: {
        rows: '',
        message: 'hi',
        country: 'russia',
        c : {}
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
        this.info();
    },
  
    methods: {
        info : function(){
            var self = this;
            $.ajax({
                url: url + 'querybycountry/'+this.country,
                method: 'GET',
                success: function (data) {
                    self.c=data[0];
                  
                    self.message='bye'

                },
                error: function (error) {
                    console.log(error);
                }
            });
           
        }
    }
});


