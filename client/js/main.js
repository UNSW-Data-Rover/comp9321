
// url constant
const data_publish_url = "http://127.0.0.1:5000/";
const google_url= "http://127.0.0.1:8080/";



// child component of row array/ table element
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

// Vuejs framework
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
        map_center: [55.7558, 37.6173],
        stadium_coordinates: [ new google.maps.LatLng(55.810979, 37.523728),
                            new google.maps.LatLng(55.715979, 37.543728)],
        stadium_names: ['stadium 1', 'stadium2'],
        stadium_address: ['street 1', 'street2']

    },
    computed: {
        img_code: function(){
            var imgcode= "../client/svg/"+this.code+".svg";
            return imgcode;
        }
    },
    mounted: function () {
        var self = this;
        
        $.ajax({
            url: data_publish_url + 'getallevents/',
            method: 'GET',
            success: function (data) {
                self.rows = data;
            },
            error: function (error) {
                console.log(error);
            }
        });
        this.info();
        google.maps.event.addDomListener(window, 'load', this.google());

    },
  
    methods: {
        info : function(){

            var self = this;
            $.ajax({
                url: data_publish_url + 'querybycountry/'+this.country,
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

        mapping: function(){

            this.info();

            var self= this;
            $.ajax({
                url: google_url + 'country/'+this.country,
                method: 'GET',
                async: false,
                success: function (data) {
                    var country_coordinate=data[data.length-1]['Country Coordinate'].split(',');
                    self.map_center=[parseFloat(country_coordinate[0]), parseFloat(country_coordinate[1])];
                    
                    self.stadium_coordinates=[];

                    self.stadium_names=[];
                    self.stadium_address=[];
                    
                    for(var i = 0;i<data.length-1; i++){
                        if (data[i]["Coordinate"] == null){
                            continue;
                        };
                            var latlong=data[i]["Coordinate"].split(',');
                            var gloc = new google.maps.LatLng(parseFloat(latlong[0]), parseFloat(latlong[1]));
                            self.stadium_coordinates.push(gloc);
                            self.stadium_names.push(data[i]["Stadium"]);
                            self.stadium_address.push(data[i]["Address"]);
                       
                    };

                 
                },
                error : function (error) {
                    console.log(error);
                }
           
            });
            this.google();
        },
        table: function(new_c){
            this.country=new_c[0];
            this.year = new_c[1];
            this.mapping();
        },

        google: function () {
            console.log('googling');
            var myCenter=new google.maps.LatLng(this.map_center[0], this.map_center[1]);
            var mapProp = {
              center:myCenter,
              zoom:10,
              mapTypeId:google.maps.MapTypeId.ROADMAP
              };

            var map=new google.maps.Map(document.getElementById("googleMap"),mapProp);
            var infowindow = new google.maps.InfoWindow();
            console.log(this.stadium_coordinates);
            var markers = [];
          
            for(var i = 0;i< this.stadium_coordinates.length; i++){
                var gmarker = new google.maps.Marker({
                                            position : this.stadium_coordinates[i],
                                            map : map});
                markers.push(gmarker);
                
                var content= '<div><strong>' + this.stadium_names[i] + '</strong><br>' +
                            'Address: ' + this.stadium_address[i] + '<br></div>';

                var infowindow = new google.maps.InfoWindow();

                google.maps.event.addListener(gmarker,'click', (function(gmarker,content,infowindow){ 
                        return function() {
                            infowindow.setContent(content);
                            infowindow.open(map,gmarker);
                        };
                    })(gmarker,content,infowindow)); 


            };
            
            var bounds = new google.maps.LatLngBounds();
            for(var i = 0;i < markers.length;i++){
                bounds.extend(markers[i].getPosition());
            }
            map.fitBounds(bounds);
        }



    }
});

