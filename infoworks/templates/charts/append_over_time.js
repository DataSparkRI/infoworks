var data_type = '{{indicator.over_time.data_type}}';
var title_text = "";
var series = [];
var current_color = '';
function shadeColor1(color, percent) {  // deprecated. See below.
    var num = parseInt(color.slice(1),16), amt = Math.round(2.55 * percent), R = (num >> 16) + amt, G = (num >> 8 & 0x00FF) + amt, B = (num & 0x0000FF) + amt;
    return "#" + (0x1000000 + (R<255?R<1?0:R:255)*0x10000 + (G<255?G<1?0:G:255)*0x100 + (B<255?B<1?0:B:255)).toString(16).slice(1);
}
function clone(obj) {
    if (null == obj || "object" != typeof obj) return obj;
    var copy = obj.constructor();
    for (var attr in obj) {
        if (obj.hasOwnProperty(attr)) copy[attr] = obj[attr];
    }
    return copy;
}
function getName(){
	var result = "";
	{% for select in indicator.over_time.selects %}
	result = result + document.getElementById("select{{select.id}}").value + " ";
	{% endfor %}
	dataset = [];
	for (i=0; i < data.length; i++){
		dataset.push(result + data[i]);
	}
	return dataset;
}
function highcharts(data){
	this.title_text='';
	{% for select in indicator.over_time.selects %}
	this.title_text = title_text +" "+ $("#select{{select.id}} option:selected").text();
	{% endfor %}
		        //var series = []
            	for (var i = 0; i < data["data"].length;i++){
            		obj = {}
            		obj["name"] = data["data"][i]["name"];
            		obj["data"] = [];
            		
            		positive = true;
				  	for (var j=0; j<negative.length; j++){
						if (obj["name"].endsWith(negative[j])){
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
            		
            		for (var key in lookup){
				  		if (!lookup.hasOwnProperty(key)) continue;
				  		if (data["data"][i]["name"].endsWith(key)){
				  			obj["name"]=title_text+' '+lookup[key];
				  		}
				  	}
            		
            		for (var key in color){
				  		if (!lookup.hasOwnProperty(key)) continue;
				  		if (data["data"][i]["name"].endsWith(key)){
				  		    if (this.current_color=='') this.current_color = color[key];
				  		    else this.current_color = shadeColor1(this.current_color,10);
				  			obj["color"]=this.current_color;
				  		}
				  	}
            		series.push(obj);
            	}
            	{% if indicator.over_time.chart_type == 'PIE-CHART' %}
            	//this.series = [];
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
            		    template.data.push([data.data[j].name, parseInt(data.data[j].row[i])]);
            		}
            		this.series.push(template);
            	}
            	
            	$(function () {
				    $('#highchart').highcharts({
				        chart: {
				            plotBackgroundColor: null,
				            plotBorderWidth: 1,//null,
				            plotShadow: false,
				        },
				        title: {
				            text: '{{indicator.district_indicator_set.district.district_name}}'+title_text
				        },
				        tooltip: {
				            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
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
				    $('#highchart').highcharts({
				        chart: {
				            type: {% if indicator.over_time.chart_type == 'AREA-CHART' %}'area'{% elif indicator.over_time.chart_type == 'HORZ-BAR-CHART' %}'bar'{% elif indicator.over_time.chart_type == 'LINE-CHART' %}'line'{% else %}'column'{% endif %}
				        },
				        title: {
				            text: '{{indicator.state_indicator_set.state.state_name}}'+title_text
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
				                text: '<b>{{indicator.over_time.y_axis_title_text}}</b>'
				            },
                            {% if indicator.over_time.stack_min %}min:{{indicator.over_time.stack_min}},{% endif %}
                            {% if indicator.over_time.stack_max %}max:{{indicator.over_time.stack_max}},{% endif %}
				            labels: {
				                formatter: function () {
				                	data_type = '{{indicator.over_time.data_type}}';
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
				                	if (this.total < 0){if(data_type=='PERCENT')return {% if indicator.over_time.stack_label_negative %}"{{indicator.over_time.stack_label_negative}} "+this.total+"%"{% else %}""{% endif %};
				                	return {% if indicator.over_time.stack_label_negative %}"{{indicator.over_time.stack_label_negative}} "+this.total*-1{% else %}""{% endif %};}
				                	else{if(data_type=='PERCENT')return {% if indicator.over_time.stack_label_positive %}"{{indicator.over_time.stack_label_positive}} "+this.total+"%"{% else %}""{% endif%};
				                	return {% if indicator.over_time.stack_label_positive %}"{{indicator.over_time.stack_label_positive}} "+this.total{% else %}""{% endif %};}
				                },
				                style: {
				                    fontWeight: 'bold',
				                    color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
				                }
				            }
				        },
				        tooltip: { enabled: false },
				        plotOptions: {
				            column: {
				                {% if indicator.over_time.chart_type != 'GROUPED-COLUMN' %}stacking: 'normal',{% endif %}
				                dataLabels: {
				                    enabled: true,
				                    
				                    formatter:function() {
							                    if (this.y < 0){var pcnt = this.y*-1;}
							                    else{var pcnt = this.y;}
							                    if(data_type=='PERCENT')
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
    var mainApp = angular.module('mainApp',[]).config(function($interpolateProvider) {
					        $interpolateProvider.startSymbol('{[{');
					        $interpolateProvider.endSymbol('}]}');
					    });	

    mainApp.controller('tableCtrl', ['$scope', '$http', function($scope, $http) {
		
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
            		dataset:JSON.stringify(getName())},
            		headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            		}).
            success(function(data, status, headers, config) {
                $scope.data = data;
                highcharts(data);
                 var headers=data["school_year"];
				  var rowHtml='';//'<tr><th></th><th>'+headers.join('</th><th>')+'</th></tr>';
				  
				  for (var i =0; i<data["data"].length; i++){
				  		name = data["data"][i]["name"];
				  		for (var key in lookup){
				  			if (!lookup.hasOwnProperty(key)) continue;
				  			var obj = lookup[key];
				  			if (data["data"][i]["name"].endsWith(key)){
				  				name = lookup[key];
				  			}
				  		}
				  		
				  		rowHtml+='<tr><td>'+title_text+' '+name+'</td>';
				  		data_row = []
				  		for (var x=0; x<data["data"][i]["row"].length;x++){
				  			var value = data["data"][i]["row"][x];
							if (data_type=='PERCENT'){
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
				  $('#table tr:last').after(rowHtml);                
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
            		dataset:JSON.stringify(getName())},
            		headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            		}).
            success(function(data, status, headers, config) {            
                $scope.data = data;
                highcharts(data);
                var headers=data["school_year"];
                var rowHtml='<tr><th></th><th>'+headers.join('</th><th>')+'</th></tr>';
				
				for (var i =0; i<data["data"].length; i++){
						name = data["data"][i]["name"];
						for (var key in lookup){
				  			if (!lookup.hasOwnProperty(key)) continue;
				  			var obj = lookup[key];
				  			if (data["data"][i]["name"].endsWith(key)){
				  				name=lookup[key];
				  			}
				  		}
				  		rowHtml+='<tr><td>'+title_text+' '+name+'</td>';
				  		data_row = []
				  		for (var x=0; x<data["data"][i]["row"].length;x++){
				  			var value = data["data"][i]["row"][x];
							if (data_type=='PERCENT'){
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
				$('#table').html(rowHtml);
            }).
            error(function(data, status, headers, config) {});
        });        
        
    }]);
