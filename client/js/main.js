//written by Chieh-An Liang & JingXuan Li
//javascript file for index page, using Vuejs framework
//last revision date: May 26 2018

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
        stadium_coordinates: [ new google.maps.LatLng(55.7158, 37.5537),
                            new google.maps.LatLng(59.9727, 30.2214),
                            new google.maps.LatLng(43.4021, 39.9559),
                            new google.maps.LatLng(56.8325, 60.5736),
                            new google.maps.LatLng(55.8210, 49.1610),
                            new google.maps.LatLng(56.3373, 43.9633),
                            new google.maps.LatLng(47.2098, 39.7391),
                            new google.maps.LatLng(53.2781, 50.2375),
                            new google.maps.LatLng(54.1818, 45.2039),
                            new google.maps.LatLng(48.7345, 44.5485),
                            new google.maps.LatLng(55.4943, 37.26249),
                            new google.maps.LatLng(54.6979, 20.5349)],
        stadium_names: ['Luzhniki Stadium', 'Saint Petersburg Stadium','Olympic Stadium Fisht',
            'Ekaterinburg Arena','Kazan Arena','Stadion Nizhniy Novgorod','Rostov Arena',
        'Cosmos Samara Stadium','Mordovia Arena','Volgograd Arena','Otkritie Arena','Kaliningrad Stadium'],
        stadium_address: ['ул. Лужники, 24, Москва, г. Москва, Russia, 119048',
            'Futbol\'naya Alleya, 1, Sankt-Peterburg, Russia, 197110',
            'Olympic Ave, Adler, Krasnodarskiy kray, Russia, 354340',
            'Ulitsa Repina, 5, Yekaterinburg, Sverdlovskaya oblast\', Russia, 620028',
            'пр-кт Ямашева, 115 А, Kazan, Respublika Tatarstan, Russia, 421001',
            'Ulitsa Dolzhanskaya, 2А корпус 1, Nizhnij Novgorod, Nizhegorodskaya oblast\', Russia, 603159',
            'Rostov-on-Don, Rostov Oblast, Russia, 344002',
            'Ulitsa Dal\'nyaya, Samara, Samarskaya oblast\', Russia, 443072',
            'Volgogradskaya Ulitsa, 1, Saransk, Respublika Mordoviya, Russia, 430009',
            'пр-кт. В.И. Ленина, 76, Volgograd, Volgogradskaya oblast\', Russia, 400005',
            'Volokolamskoye sh., 69, Moskva, Russia, 125424',
            'Solnechnyy Bul\'var, Konigsberg, Kaliningradskaya oblast\', Russia, 236006']
    },
    computed: {
        img_code: function(){
            if(this.code == 'KR/JP'){
                var imgcode= "../client/svg/KR.svg";
                return imgcode;
            }
            var imgcode= "../client/svg/"+this.code+".svg";
            return imgcode;
        },
        korea_check: function(){
            if(this.country == "Korea/Japan"){
                this.country = "Korea&Japan";
                return this.country
            };

            return this.country
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

        //get top10
        $.ajax({
            url: data_publish_url + 'gettop/',
            method: 'GET',
            async: false,
            success: function (data) {
                console.log(data);
                country=[];
                dataset = [];
                for(var i = 0;i< data.length; i++){
                    country.push(data[i]['Country']);
                    dataset.push(data[i]['Count'])
                }

                //chart
                var ctx = document.getElementById("myChart").getContext('2d');
                var myChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels:country,
                        datasets: [{
                            label: '# of qualification from 1930 to 2014',
                            data: dataset,
                            backgroundColor: 'rgba(54, 162, 235, 0.2)',
                            hoverBackgroundColor : 'rgba(54, 162, 235, 0.5)',
                            borderColor: 'rgba(54, 162, 235, 1)',
                            borderWidth: 1,
                            fill: 'red'
                        }],

                    },
                    options: {
                        scales: {
                            yAxes: [{
                                gridLines: {
                                    display : false    //不显示表格线
                                },
                                ticks: {
                                    beginAtZero:true
                                }
                            }]
                        },
                        onClick: function(c,i) {
                            e = i[0];
                            self.country = this.data.labels[e._index];
                            console.log(self.country);

                            //call funtion show country info and map
                            self.mapping();
                        }
                    }

                });
            },
            error : function (error) {
                console.log(error);
            }
        });

        this.info();
        google.maps.event.addDomListener(window, 'load', this.google());


    },

    methods: {
        info : function(){
        	const available=['Russia', 'Brazil','South Africa', 'Germany', 'Korea/Japan', 'France', 'USA', 'Italy',
        					'Mexico', 'Spain', 'Argentina', 'England', 'Chile', 'Sweden', 'Switzerland', 'Uruguay']
        	this.country= this.capitalize(this.country)


        	var index= available.indexOf(this.country)
        	if (index<0){
        			alert("Sorry, country not in record!");
        			return 0
        	};

        	var self = this;
		        $.ajax({
		            url: data_publish_url + 'querybycountry/'+this.korea_check,
		            method: 'GET',
		            success: function (data) {
		                    self.c=data[0];
		                    self.code=data[0]['CountryCode'];
		                    document.getElementById('jpflag').style.display="none";
		                    if(self.code == 'KR/JP'){
		                        document.getElementById('jpflag').style.display="block";
		                    }
		            },
		            error: function (error) {
		                    console.log(error);
		            }
		    });
  
            
        },
        capitalize: function(string){
            return string.charAt(0).toUpperCase() + string.slice(1);
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
                google.maps.event.addListener(map,'click', (function(gmarker,content,infowindow){
                        return function() {
                            infowindow.close(map,gmarker);
                        };
                    })(gmarker,content,infowindow));


            };

            var bounds = new google.maps.LatLngBounds();
            for(var i = 0;i < markers.length;i++){
                bounds.extend(markers[i].getPosition());
            }
            map.fitBounds(bounds);
        },


    }
});
