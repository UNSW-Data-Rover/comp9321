Vue.component('table-selector', {
      template: `
        
            <button class="btn btn-link my-2 my-sm-0" style="font-weight: bold; color: darkblue" @click="unhappy($event)" >
         {{ country }} </button>

        `,
      props: ['country'],
      methods: {
        unhappy() {
            this.$emit('unhappy', this.country);
        }
      }
});


var s = new Vue({
    el: '#stat',
    props: {
        'table-selector':'table-selector'
    },
    data: {
        compare_country1: 'Brazil',
        compare_country2: 'Germany',
        statistics:[],
        ratio1:0,
        ratio2:0,
        code1:'BR',
        code2: 'DE',
        ctable: ['Brazil', 'Italy', 'Germany', 'Argentina', 'Mexico', 'England', 'Spain', 'France', 'Uruguay', 'Belgium']
    },
    computed: {
        img_code1: function(){
            if(this.compare_country1 == "England"){
                this.code1="GB";
            }
            var imgcode1= "../client/svg/"+this.code1+".svg";
            console.log(imgcode1);
            return imgcode1;
        },
        img_code2: function(){
            if(this.compare_country1 == "England"){
                this.code1="GB";
            }
            var imgcode2= "../client/svg/"+this.code2+".svg";
            console.log(imgcode2);
            return imgcode2;
        }
    },
    methods: {
        capitalize: function(string){
            return string.charAt(0).toUpperCase() + string.slice(1);
        },
        change1: function(c1){
            this.compare_country1= c1;
            this.compare()
        },
        change2: function(c2){
            this.compare_country2= c2;
            this.compare()
        },
        compare: function(){
            var self = this;
            console.log(this.compare_country1);
           
            $.ajax({
                url: 'http://127.0.0.1:5000/getstats/'+this.capitalize(this.compare_country1)+'&'+this.capitalize(this.compare_country2),
                method: 'GET',
                success: function (data) {
                    console.log(data);
                    self.statistics=data.slice(0, data.length-1);
                    var winning1= self.capitalize(self.compare_country1) + ' winning rate';
                    var winning2= self.capitalize(self.compare_country2) + ' winning rate';
                    self.ratio1= (data[data.length-2].winnings[winning1])*100 + '%';
                    self.ratio2= (data[data.length-2].winnings[winning2])*100 + '%';
                    self.code1= data[data.length-1].CountryCode.FirstCode;
                    self.code2= data[data.length-1].CountryCode.SecondCode;
                    

                },
                error: function (error) {
                    console.log(error);
                }
            });
        }
    }
});