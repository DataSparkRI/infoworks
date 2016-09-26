function cover_categories(columns){
	var categories = [];
	for (var i = 1; i < columns.length; i++){
		categories.push(columns[i].text)
	}
	return categories;
}

function cover_series(data){
	var series = [];
	for (var i = 0; i < data.length; i++){
		var row_data = [];

		for (var j = 1; j < data[i].length; j++){
			row_data.push(parseFloat(data[i][j]));
		}
		var row = {"name":data[i][0], "data":row_data}
		console.log(row);
		series.push(row);
	}
	console.log("series");
	console.log(series);
	return series;
}

function InforChart (theCategories, theSeries) {
    this.categories = theCategories;
    this.series = theSeries;
    this.title = "";
    this.subtitle = "";
    this.type = 'column';
}

InforChart.prototype = {
	    constructor: InforChart,
	    setType:function (type){
	    	this.type=type
	    },
	    showChart:function ()  {
	        var chart = new Highcharts.Chart({
	            chart: {
	                renderTo: 'container',
	                type: this.type
	            },
	            title: {
	                text: this.title
	            },
	            subtitle: {
	                text: this.subtitle
	            },
	            xAxis: {
	                categories: this.categories,
	                crosshair: true
	            },
	            yAxis: {
	                min: 0,
	                title: {
	                    text: ''
	                }
	            },
	            tooltip: {
	                headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
	                pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
	                    '<td style="padding:0"><b>{point.y:.1f}</b></td></tr>',
	                footerFormat: '</table>',
	                shared: true,
	                useHTML: true
	            },
	            plotOptions: {
	                column: {
	                    pointPadding: 0.2,
	                    borderWidth: 0
	                }
	            },
	            series: this.series
	        });
	    }
	}




function build_chart(categories, series, title, subtitle){
    var chart = new Highcharts.Chart({
        chart: {
            renderTo: 'container',
            type: 'column'
        },
        title: {
            text: title
        },
        subtitle: {
            text: subtitle
        },
        xAxis: {
            categories: categories,
            crosshair: true
        },
        yAxis: {
            min: 0,
            title: {
                text: ''
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f}</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: series
    });
}
