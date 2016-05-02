    {% load staticfiles %}
    <script src = "{% static "highcharts-4.2.3/highcharts.js" %}"></script>
    <script src = "{% static "highcharts-4.2.3/modules/exporting.js" %}"></script>

	<script type="text/javascript">
	{% for i in detail_set %}
	    {% if i.set_name.display_type == 'BAR-CHART' or i.set_name.display_type == 'BAR-CHART-ONLY' or i.set_name.display_type == 'HORZ-BAR-CHART' or i.set_name.display_type == 'HORZ-BAR-CHART-ONLY'%}
		$(function () {
			categories = [{% for key, values in i.data.items %}{% if forloop.first %}{% for j in values.names %}'{{j}}',{% endfor %}{% endif %}{% endfor %}]
			
		    $('#'+'{{i.set_name.display_type}}'+'{{forloop.counter}}').highcharts({
		        chart: {
		            {% if i.set_name.display_type == 'HORZ-BAR-CHART' or i.set_name.display_type == 'HORZ-BAR-CHART-ONLY'%}
		            type: 'bar'
		            {% else %}
		            type: 'column'
		            {% endif %}
		        },
		        title: {
		            text: '{{i.set_name.title}}'
		        },
		        xAxis: {
		            categories: categories,
		            {% if i.set_name.plot_setting %}
		              {% if i.set_name.plot_setting.band %}
                      plotBands: [{% for b in i.set_name.plot_setting.band %}{
                        {% if b.background_color %}color:'{{b.background_color}}',{% endif %}
                        from: {{b.setting_from}}, // Start of the plot band
                        to: {{b.setting_to}}, // End of the plot band
                        label: {
                            text: '{{b.label_text|safe}}',
                            style: {
                                color: '{{b.label_color}}'
                            },
                            y: {{b.y_position}}
                        }
                      },{% endfor %}],
                      {% endif %}
                      {% if i.set_name.plot_setting.line %}
                      plotLines: [{% for l in i.set_name.plot_setting.line %}{
                        color: '{{l.line_color}}', // Color value
                        dashStyle: '{{l.dash_style}}', // Style of the plot line. Default to solid
                        value: {{l.value}}, // Value of where the line will appear
                        width: {{l.width}} // Width of the line
                      },{% endfor %}]
                      {% endif %}
		            {% endif %}		            
		        },
		        yAxis: {
		            {% if i.set_name.data_type == 'PERCENT' %}min: -100, max: 100,{% endif %}
		            title: {
		                text: '{{i.set_name.y_axis_title_text}}'
		            },
				            labels: {
				                formatter: function () {
				                	data_type = '{{i.set_name.data_type}}';
				                    if(data_type=='PERCENT'){
				                    if (this.axis.defaultLabelFormatter.call(this) < 0)
				                    return (this.axis.defaultLabelFormatter.call(this)*-1)+'%';
				                    else return this.axis.defaultLabelFormatter.call(this)+'%';}
				                    else {
				                    if (this.axis.defaultLabelFormatter.call(this)[0] == '-'){
				                    return (this.axis.defaultLabelFormatter.call(this).substring(1));}
				                    else {return this.axis.defaultLabelFormatter.call(this);}}
				                }            
				            },
				            gridLineColor: '#197F07',
					        gridLineWidth: 0,
					        lineWidth:1,
					        plotLines: [{
					            color: '#000000',
					            width: 3,
					            value: 0
					        }],
				            stackLabels: {
				                enabled: true,
				                formatter:function() {
				                	data_type = '{{i.set_name.data_type}}';
				                	if (this.total < 0){if(data_type=='PERCENT')return "";
				                	return "";}
				                	else{if(data_type=='PERCENT')return "Total: "+this.total+"%";
				                	return "Total: "+this.total;}
				                },
				                style: {
				                    fontWeight: 'bold',
				                    color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
				                }
				            }
		        },
		        tooltip: {
		            headerFormat: '<b>{point.x}</b><br/>',
		            pointFormat: '{series.name}: {point.y}<br/>Total: {point.stackTotal}',
		            formatter: function() {
				            	if (this.point.y < 0){y=this.point.y*-1}
				            	else{y=this.point.y}
				            	if (this.point.stackTotal < 0){stackTotal=this.point.stackTotal*-1}
				            	else{stackTotal=this.point.stackTotal}
				            	return this.series.name +": "+y;
    				}
		        },
				plotOptions: {
		            {% if i.set_name.display_type == 'HORZ-BAR-CHART' or i.set_name.display_type == 'HORZ-BAR-CHART-ONLY'%}					
					series: {
                    	stacking: 'normal'
                    },
					{% endif %}
				    column: {
				            stacking: 'normal',
				            dataLabels: {
				                 enabled: true,
				                 formatter:function() {
				                    			data_type = '{{i.set_name.data_type}}';
							                    if (this.y < 0){var pcnt = this.y*-1;}
							                    else{var pcnt = this.y;}
							                    if(data_type=='PERCENT'){
							                    	if (pcnt < 9)
							                    		return "";
							                    	else
							                    		return pcnt+'%';
							                    }
							                    else
							                    	return pcnt;
							     },
				                 color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white',
				                 style: {
				                        textShadow: '0 0 3px black'
				                }
				            }
				    }
				},
                        series: [{% for key, values in i.data.items %}{name:'{{values.dimension_y.name}}',{% if values.dimension_y.color_hex %}color: '{{values.dimension_y.color_hex}}',{% endif %}
                        {% if values.dimension_y.is_positive %}data:[{% for row in values.data %}{% if row.key_value %}{% if row.key_value == '-1' %}null, {% else %}{{row.key_value}},{% endif %}{% else %}null,{% endif %}{% endfor %}]}
                        {%else%}data:[{% for row in values.data %}{% if row.key_value %}{% if row.key_value == '-1' %}null, {% else %}-{{row.key_value}},{% endif %}{% else %}null,{% endif %}{% endfor %}]}{% endif %},{% endfor %}]
		    });
		});
	{% endif %}
	{% endfor %}
	
	</script>

    {% comment %}
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
  {% endcomment %}
