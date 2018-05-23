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


Vue.component('time-eater', {
      template: `
        <button class="btn btn-outline-success my-2 my-sm-0"  v-on:click="unhappy">
          {{title}} </button>`,
      props: ['title','year'],
      methods: {
        unhappy() {
            this.$emit('unhappy', [this.title, this.year]);
        }
      }
});


var v = new Vue({
    el: '#index',
    component: {
        'time-eater': 'time-eater'
    },
    data: {
        rows: '',
        year: '2018',
        country: 'Russia',
        c : {},
        code: 'RU',
        table_country: ''
    },
    computed: {
        img_code: function(){
            var imgcode= "../client/svg/"+this.code+".svg";
            console.log(imgcode);
            return imgcode;
        }
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
                    self.code=data[0]['CountryCode'];

                },
                error: function (error) {
                    console.log(error);
                }
            });
           
        },
        test: function(){
            var self= this;
            console.log(this.country);
        },
        table: function(new_c){
            this.country=new_c[0];
            this.year = new_c[1];
            console.log(this.year);
            this.info();
        }


    }
});


console.log(v.message)