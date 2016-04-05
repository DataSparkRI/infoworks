    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/modules/exporting.js"></script>

    <script type="text/javascript">
      $(function() {
//        var title = $('#barchart').attr("value")
        {% for i in detail_set %}
          var category = [];
          var series = [];
          var stack_index = [0,1,3,2];
          var legend_index = [0,1,2,3];
          var selector = '#'+'{{i.set_name.display_type}}'+'{{forloop.counter}}';
          console.log(selector);
          var title = $(selector).attr("value");
          console.log(title);
          var tname = '{{i.set_name.title}}';
//          console.log("tname"+tname);
          if (tname == title) {
            var len = '{{i.data.items|length}}';
          var mid = parseInt(len/2);
          var count = len;
  //        console.log(mid);
          {% for key, values in i.data.items %}
            var series_name = '{{key}}';
  //          console.log(key);
            {% if forloop.first %}
              {% for j in values.names %}
                  var cat = '{{j}}';
                  category.push(cat);
  //                console.log(category);
              {% endfor %}
            {% endif %}
            
            var series_data = [];
            
            {% for row in values.data %}
              var data = '{{row.key_value}}';
              
              if (count > mid) {
                  series_data.push(Number(data));
              } else {
                  var neg = -Math.abs(Number(data));
                  series_data.push(neg);
              }
            {% endfor %}
            
            var data_point = {'name': series_name, 'data': series_data, 'index':stack_index[len-count], 'legendIndex':legend_index[len-count]};
//            console.log(data_point);
            series.push(data_point);
            count--;
          {% endfor %}
          
          }
        
        for (i in series) {
          console.log(series[i].name);
          console.log(series[i].data);
        }
//        console.log(category);
       
        $(selector).highcharts({
          chart: {
            type: 'column'
          },
          title: {
            text: 'Nayatt School'
          },
          xAxis: {
            categories: category
          },
          yAxis: {
            min: -100,
            max: 100,
            reversedStack: false,
            title: {
              text: '% Proficient'
            }
          },
          legend: {
            reversed: false,
            align: 'right',
            layout: 'vertical',
            verticalAlign: 'middle'
          },
          plotOptions: {
            column: {
              stacking: 'normal',
              dataLabels: {
                enabled: true,
        				formatter: function() {
                	return Math.abs(this.y);
                },
                color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white',
                style: {
                  textShadow: '0 0 3px black'
                }
              }
            }
          },
          series: series
  
        });
        {% endfor %}
      });
  </script>
