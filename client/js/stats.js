var s = new Vue({
    el: '#stat',
    data: {
        compare_country1: 'Brazil',
        compare_country2: 'Germany',
        statistics:[],
        ratio1:0,
        ratio2:0
    },
    methods: {
        compare: function(){
            var self = this;
            console.log(this.compare_country1);
           
            $.ajax({
                url: 'http://127.0.0.1:5000/getstats/'+this.compare_country1+'&'+this.compare_country2,
                method: 'GET',
                success: function (data) {
                    console.log(data);
                    self.statistics=data.slice(0, data.length-1);
                    var winning1= self.compare_country1 + ' winning rate';
                    var winning2= self.compare_country2 + ' winning rate';
                    self.ratio1= data[data.length-1].winnings[winning1];
                    self.ratio2= data[data.length-1].winnings[winning2];
                    

                },
                error: function (error) {
                    console.log(error);
                }
            });
        }
    }
});