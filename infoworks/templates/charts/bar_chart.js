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
				tooltip: { enabled: false },
				plotOptions: {
		            {% if i.set_name.display_type == 'HORZ-BAR-CHART' or i.set_name.display_type == 'HORZ-BAR-CHART-ONLY'%}					
	                series: {
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
		                    color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white'
	                	}
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
                        series: [{% for key, values in i.data.items %}{name:'{{values.dimension_y.name}}',{% if values.dimension_y.color_hex %}color: '{{values.dimension_y.color_hex}}', {% endif %}
                        {% if values.dimension_y.is_positive %}index:{{forloop.counter}},data:[{% for row in values.data %}{% if row.key_value %}{% if row.key_value == '-1' %}null, {% elif row.key_value == ' ' %}null, {% elif row.key_value == '' %}null, {% else %}{{row.key_value}},{% endif %}{% else %}null,{% endif %}{% endfor %}]}
                        {%else%}index:{{forloop.revcounter}},data:[{% for row in values.data %}{% if row.key_value %}{% if row.key_value == '-1' %}null, {% elif row.key_value == ' ' %}null, {% elif row.key_value == '' %}null, {% else %}-{{row.key_value}},{% endif %}{% else %}null,{% endif %}{% endfor %}]}{% endif %},{% endfor %}]
		    });
		});
	{% elif i.set_name.display_type == 'PIE-CHART' or i.set_name.display_type == 'PIE-CHART-ONLY' %}
	$(function () {
	function clone(obj) {
    	if (null == obj || "object" != typeof obj) return obj;
    	var copy = obj.constructor();
    	for (var attr in obj) {
        	if (obj.hasOwnProperty(attr)) copy[attr] = obj[attr];
    	}
    	return copy;
	}
	
	categories = [{% for key, values in i.data.items %}{% if forloop.first %}{% for j in values.names %}'{{j}}',{% endfor %}{% endif %}{% endfor %}]
    data_series = [{% for key, values in i.data.items %}{name:'{{values.dimension_y.name}}',{% if values.dimension_y.color_hex %}color: '{{values.dimension_y.color_hex}}', {% endif %}
                        index:{{forloop.counter}},data:[{% for row in values.data %}{% if row.key_value %}{% if row.key_value == '-1' %}null, {% elif row.key_value == ' ' %}null, {% elif row.key_value == '' %}null, {% else %}{{row.key_value}},{% endif %}{% else %}null,{% endif %}{% endfor %}]}
                        ,{% endfor %}]
    
    series = []
    for (i = 0; i< categories.length; i++){
    	data = [];
    	for (j = 0; j <data_series.length; j++){
    		var tmp = clone(data_series[j]);
    		tmp.y = tmp.data[i];
    		data.push(tmp);
    	}
    	series.push({
    		name:categories[i],
    		colorByPoint: true,
    		data: data
    	})
    	
    }
    $('#'+'{{i.set_name.display_type}}'+'{{forloop.counter}}').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: '{{i.set_name.title}}'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    }
                }
            }
        },
series: series

    });
});
	{% endif %}
	{% endfor %}
	
	</script>

