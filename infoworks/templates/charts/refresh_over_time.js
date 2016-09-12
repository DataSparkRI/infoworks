
var data_type{{over_time.id}} = '{{over_time.data_type}}';

function getName{{over_time.id}}(){
	var result = "";
	{% for select in over_time.selects %}
	result = result + document.getElementById("select{{over_time.id}}_{{select.id}}").value + " ";
	{% endfor %}
	dataset = [];
	for (i=0; i < data{{over_time.id}}.length; i++){
		dataset.push(result + data{{over_time.id}}[i]);
	}
	return dataset;
}

function highcharts{{over_time.id}}(data){
    console.log(data);
    for (var i = 0; i < data["data"].length; i++){
        for (var j=0; j<data["data"][i]["row"].length; j++){
            if (data["data"][i]["row"][j] !== null){
               if (data["data"][i]["row"][j].indexOf('1:') !== -1){
                 data["data"][i]["row"][j] = data["data"][i]["row"][j].replace('1:','');
               }
            }
        }
    }
	var title_text = "";
	{% for select in over_time.selects %}
	title_text = title_text +" "+ $("#select{{over_time.id}}_{{select.id}} option:selected").text();
	{% endfor %}

		        var series = []
            	for (var i = 0; i < data["data"].length;i++){
            		obj = {}
            		obj["name"] = data["data"][i]["name"];

            		
            		obj["data"] = [];
            		
            		positive = true;
				  	for (var j=0; j<negative{{over_time.id}}.length; j++){
						if (obj["name"].endsWith(negative{{over_time.id}}[j])){
			  				positive = false;
			  			}
			  		}
            		
            		for ( var j =0; j < data["data"][i]["row"].length; j++){
            			var value = parseFloat(data["data"][i]["row"][j]);
            			if (isNaN(value))
                            obj["data"].push(null);
            			else if(positive)
            				if (value == -1) obj["data"].push(null);
            				else obj["data"].push(value);
            			else
            				if(value == -1)obj["data"].push(null);
            				else obj["data"].push(value*-1);
            		}
            		
            		for (var key in lookup{{over_time.id}}){
				  		if (!lookup{{over_time.id}}.hasOwnProperty(key)) continue;
				  		if (data["data"][i]["name"].endsWith(key)){
				  			obj["name"]=lookup{{over_time.id}}[key];
				  		}
				  	}
            		
            		for (var key in color{{over_time.id}}){
				  		if (!lookup{{over_time.id}}.hasOwnProperty(key)) continue;
				  		if (data["data"][i]["name"].endsWith(key)){
				  			obj["color"]=color{{over_time.id}}[key];
				  		}
				  	}
            		
            		series.push(obj);
            	}
            	            	
            	{% if over_time.chart_type == 'PIE-CHART' %}
            	series = [];
            	template1 = {
				            type: 'pie',
				            name: 'Browser share',
				            center: ["10%","50%"],
				            size: 100,
				            dataLabels: {
								enabled: false
							},
							showInLegend: true,
				            data: []
				        }
				 template2 = {
				            type: 'pie',
				            name: 'Browser share',
				            center: ["10%","50%"],
				            size: 100,
				            dataLabels: {
								enabled: false
							},
				            data: []
				        }
				base = 100 / data.school_year.length / 2;
            	for(var i = 0; i<data.school_year.length; i++){
            	    center = 100 / data.school_year.length * (i+1) - base;
            	    
            	    if (i==0) {template = template1}
            		else {template = template2}
            		template = clone(template);
            		template.name = data.school_year[i];
            		template.center = [center+"%", "50%"];
            		template.data = [];
            		for(var j = 0; j<data.data.length; j++){
            		    console.log([data.data[j].name, data.data[j].row[i]]);
            		    template.data.push([data.data[j].name, parseInt(data.data[j].row[i])]);
            		}
            		console.log(template);
            		series.push(template);
            	}
            	
            	
            	$(function () {
				    $('#highchart{{over_time.id}}').highcharts({
				        chart: {
				            plotBackgroundColor: null,
				            plotBorderWidth: 1,//null,
				            plotShadow: false,
				        },
				        title: {
				            text: '{{indicator.district_indicator_set.district.district_name}}'+title_text
				        },
				        tooltip: {
				            pointFormat: '{series.name}: <b>{point.percentage:.0f}%</b>'
				        },
				        
				        plotOptions: {
				            pie: {
				                allowPointSelect: true,
				                cursor: 'pointer'
				            }
				        },
				        series: series
				    },function(chart) {
				            
				        $(chart.series[0].data).each(function(i, e) {
				            e.legendItem.on('click', function(event) {
				                var legendItem=e.name;
				                
				                event.stopPropagation();
				                
				                $(chart.series).each(function(j,f){
				                       $(this.data).each(function(k,z){
				                           if(z.name==legendItem)
				                           {
				                               if(z.visible)
				                               {
				                                   z.setVisible(false);
				                               }
				                               else
				                               {
				                                   z.setVisible(true);
				                               }
				                           }
				                       });
				                });
				                
				            });
				        });
				    });
				});
            	{% else %}
            	$(function () {
				    $('#highchart{{over_time.id}}').highcharts({
				        chart: {
				            type: {% if over_time.chart_type == 'AREA-CHART' %}'area'{% elif over_time.chart_type == 'HORZ-BAR-CHART' %}'bar'{% elif over_time.chart_type == 'LINE-CHART' %}'line'{% else %}'column'{% endif %}
				        },
				        title: {
				            text: '{{indicator.district_indicator_set.district.district_name}}'+title_text
				        },
				        xAxis: {
				            categories: data["school_year"],
				            labels: {
				                style: {
				                    fontSize: '13px',
				                    "fontWeight":"bold"
				                }
				            }
				        },
				        yAxis: {
				            title: {
				                text: '<b>{{over_time.y_axis_title_text}}</b>'
				            },
                            {% if over_time.stack_min %}min:{{over_time.stack_min}},{% endif %}
                            {% if over_time.stack_max %}max:{{over_time.stack_max}},{% endif %}
				            labels: {
				                formatter: function () {
				                	data_type{{over_time.id}} = '{{over_time.data_type}}';
				                    if(data_type{{over_time.id}}=='PERCENT'){
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
					        {% if over_time.chart_type == 'AREA-CHART' %}{% else %}
				            stackLabels: {
				                enabled: true,
				                formatter:function() {
				                	if (this.total < 0){if(data_type{{over_time.id}}=='PERCENT')return {% if over_time.stack_label_negative %}"{{over_time.stack_label_negative}} "+this.total+"%"{% else %}""{% endif %};
				                	return {% if over_time.stack_label_negative %}"{{over_time.stack_label_negative}} "+this.total*-1{% else %}""{% endif %};}
				                	else{if(data_type{{over_time.id}}=='PERCENT')return {% if over_time.stack_label_positive %}"{{over_time.stack_label_positive}} "+this.total+"%"{% else %}""{% endif%};
				                	return {% if over_time.stack_label_positive %}"{{over_time.stack_label_positive}} "+this.total{% else %}""{% endif %};}
				                },
				                style: {
				                    fontWeight: 'bold',
				                    color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
				                }
				            }
				            {% endif%}
				        },
				        tooltip: { enabled: false },
				        plotOptions: {
				            {% if over_time.chart_type == 'AREA-CHART' %}area{% else %}column{% endif %}: {
				                {% if over_time.chart_type != 'GROUPED-COLUMN' %}stacking: 'normal',{% endif %}
				                dataLabels: {
				                    enabled: true,
				                    formatter:function() {
							                    if (this.y < 0){var pcnt = this.y*-1;}
							                    else{var pcnt = this.y;}
							                    if(data_type{{over_time.id}}=='PERCENT')
							                    	return pcnt+'%';
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
				        series: series
				    });
				});
				{% endif %}

}

    mainApp.controller('tableCtrl{{over_time.id}}', ['$scope', '$http', function($scope, $http) {
		
		$scope.change = function() {
            $.ajax({method: 'POST', 
            		url: '{% url 'overtime' %}', 
            		data: {csrfmiddlewaretoken: "{{ csrf_token }}",
            		{% if indicator.state_indicator_set%}
            		type:"state", 
            		slug:"{{indicator.state_indicator_set.state.slug}}", 
            		{% endif %}
            		{% if indicator.district_indicator_set %}
            		type:"district", 
            		slug:"{{indicator.district_indicator_set.district.slug}}", 
            		{% endif %}
            		{% if indicator.school_indicator_set%}
            		type:"school", 
            		slug:"{{indicator.school_indicator_set.school.slug}}", 
            		{% endif %}
            		category:"{{indicator.title.title}}", 
            		school_year:[],
            		dataset:JSON.stringify(getName{{over_time.id}}())},
            		headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            		}).
            success(function(data, status, headers, config) {
                $scope.data = data;
                highcharts{{over_time.id}}(data);
                 var headers=data["school_year"];
				  var rowHtml='<tr><th></th><th>'+headers.join('</th><th>')+'</th></tr>';
				  
				  for (var i =0; i<data["data"].length; i++){
				  		name = data["data"][i]["name"];
				  		for (var key in lookup{{over_time.id}}){
				  			if (!lookup{{over_time.id}}.hasOwnProperty(key)) continue;
				  			var obj = lookup{{over_time.id}}[key];
				  			if (data["data"][i]["name"].endsWith(key)){
				  				name = lookup{{over_time.id}}[key];
				  			}
				  		}
				  		
				  		rowHtml+='<tr><td>'+name+'</td>';
				  		data_row = []
				  		for (var x=0; x<data["data"][i]["row"].length;x++){
				  			var value = data["data"][i]["row"][x];
							if (data_type{{over_time.id}}=='PERCENT'){
								if (value == -1) data_row.push("too few data");
								else if (value == null || value == "") data_row.push("no data");
								else data_row.push(value+"%");}
							else{
								if (value == -1) data_row.push("too few data");
								else if (value == null || value == "") data_row.push("no data");
								else data_row.push(value);}
				  		}
				  		rowHtml +='<td>'+data_row.join('</td><td>')+'</td></tr>';
				  }
				  $('#table{{over_time.id}}').html(rowHtml);                
            }).
            error(function(data, status, headers, config) {});
        };
        
        $scope.$watch('search', function() {
			
            $.ajax({method: 'POST', 
            		url: '{% url 'overtime' %}', 
            		data: {csrfmiddlewaretoken: "{{ csrf_token }}",
            		{% if indicator.state_indicator_set%}
            		type:"state", 
            		slug:"{{indicator.state_indicator_set.state.slug}}", 
            		{% endif %}
            		{% if indicator.district_indicator_set %}
            		type:"district", 
            		slug:"{{indicator.district_indicator_set.district.slug}}", 
            		{% endif %}
            		{% if indicator.school_indicator_set%}
            		type:"school", 
            		slug:"{{indicator.school_indicator_set.school.slug}}", 
            		{% endif %}
            		category:"{{indicator.title.title}}", 
            		school_year:[],
            		dataset:JSON.stringify(getName{{over_time.id}}())},
            		headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            		}).
            success(function(data, status, headers, config) {
            	
            
                $scope.data = data;
                
                var headers=data["school_year"];
                var rowHtml='<tr><th></th><th>'+headers.join('</th><th>')+'</th></tr>';
				
				for (var i =0; i<data["data"].length; i++){
						name = data["data"][i]["name"]
						for (var key in lookup{{over_time.id}}){
				  			if (!lookup{{over_time.id}}.hasOwnProperty(key)) continue;
				  			var obj = lookup{{over_time.id}}[key];
				  			if (data["data"][i]["name"].endsWith(key)){
				  				name=lookup{{over_time.id}}[key];
				  			}
				  		}
				  		rowHtml+='<tr><td>'+name+'</td>';
				  		data_row = []
				  		for (var x=0; x<data["data"][i]["row"].length;x++){
				  			var value = data["data"][i]["row"][x];
							if (data_type{{over_time.id}}=='PERCENT'){
								if (value == -1) data_row.push("too few data");
								else if (value == null) data_row.push("no data");
								else data_row.push(value+"%");}
							else{
								if (value == -1) data_row.push("too few data");
								else if (value == null) data_row.push("no data");
								else data_row.push(value);}
				  		}
				  		rowHtml +='<td>'+data_row.join('</td><td>')+'</td></tr>';
				}
				$('#table{{over_time.id}}').html(rowHtml);
                highcharts{{over_time.id}}(data);
            }).
            error(function(data, status, headers, config) {});
        });        
        
    }]);
