// global bullseye chart options
var bullseye_series_options = [{
    dataLabels: {enabled: false},
    data: [{
        id: "school_score",
        name: "School",
        color: Highcharts.getOptions().colors[0],
        innerRadius: '90%',
        radius: '100%',
    }, {
        id: "district_score",
        name: "District",
        color: Highcharts.getOptions().colors[1],
        innerRadius: '80%',
        radius: '89%',
        y: 588
    }, {
        id: "statewide_score",
        name: "Statewide",
        color: Highcharts.getOptions().colors[2],
        innerRadius: '70%',
        radius: '79%',
    }, {
        id: "national_score",
        name: "National",
        color: Highcharts.getOptions().colors[3],
        innerRadius: '60%',
        radius: '69%',
    }]
}];
var bullseye_chart = {
    chart: {
        type: 'solidgauge',
        backgroundColor: 'transparent',
        borderWidth: 0,
        spacing: [0,0,20,0]
    },

    credits: {
        enabled: false
    },

    pane: {
        background: [{
            outerRadius: '100%',
            innerRadius: '90%',
            backgroundColor: Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0.1).get(),
            borderWidth: 0
        }, {
            outerRadius: '80%',
            innerRadius: '89%',
            backgroundColor: Highcharts.Color(Highcharts.getOptions().colors[1]).setOpacity(0.1).get(),
            borderWidth: 0
        }, {
            outerRadius: '70%',
            innerRadius: '79%',
            backgroundColor: Highcharts.Color(Highcharts.getOptions().colors[2]).setOpacity(0.1).get(),
            borderWidth: 0
        }, {
            outerRadius: '60%',
            innerRadius: '69%',
            backgroundColor: Highcharts.Color(Highcharts.getOptions().colors[3]).setOpacity(0.1).get(),
            borderWidth: 0
        }],
        size: '100%',
        startAngle: 180
    },

    title: {
        verticalAlign: 'bottom',
        useHTML: true
    },

    tooltip: {
        borderWidth: 0,
        backgroundColor: 'none',
        hideDelay: 1000000,
        shadow: false,
        style: {
            fontSize: '16px'
        },
        pointFormat: '<span style="font-size: 0.9em; color: {point.color}">{point.name}</span><br><span style="font-size:2em; color: {point.color}; font-weight: bold">{point.y}</span>',
        positioner: function (labelWidth) {
            return {
                x: 60,
                y: 50
            };
        }
    },

    yAxis: {
        labels: {enabled: false},
        lineWidth: 0,
        max: 800,
        min: 200,
        tickPositions: [],
        tickWidth: 0
    }
};

// global column chart options
var column_chart = {yAxis: null, colors: ['#8085e9', 
   '#f15c80', '#e4d354', '#2b908f', '#f45b5b', '#91e8e1']};

// SAT Math Tile
var SAT_math_options = {
    chart: {renderTo:'SAT_math_tile'},
    series: JSON.parse(JSON.stringify(bullseye_series_options)),
    title: {text: 'Math'}
};

SAT_math_options.series[0].data[0].visible = false;
SAT_math_options.series[0].data[0].y = 588;
SAT_math_options.series[0].data[1].y = 588;
SAT_math_options.series[0].data[2].y = 481;
SAT_math_options.series[0].data[3].y = 511;

// SAT Reading Tile
var SAT_reading_options = {
    chart: {renderTo:'SAT_reading_tile'},
    series: JSON.parse(JSON.stringify(bullseye_series_options)),
    title: {text: 'Reading'}
};
SAT_reading_options.series[0].data[0].y = 573;
SAT_reading_options.series[0].data[1].y = 573;
SAT_reading_options.series[0].data[2].y = 480;
SAT_reading_options.series[0].data[3].y = 495;

// SAT Writing Tile
var SAT_writing_options = {
    chart: {renderTo:'SAT_writing_tile'},
    series: JSON.parse(JSON.stringify(bullseye_series_options)),
    title: {text: 'Writing'}
};
SAT_writing_options.series[0].data[0].y = 562;
SAT_writing_options.series[0].data[1].y = 562;
SAT_writing_options.series[0].data[2].y = 468;
SAT_writing_options.series[0].data[3].y = 484;

var sat_overtime_options = {
    chart: {
        backgroundColor: 'white',
        renderTo: 'SAT_over_time_chart',
        type: 'column'
    },

    colors: ['#8085e9', '#f15c80', '#e4d354', '#2b908f', '#f45b5b', '#91e8e1'],
    
    plotOptions: {
        column: {
            dataLabels: {enabled: false},
        },
        line: {
            dashStyle: 'LongDashDotDot',
            linkedTo: ':previous',
        }
    },
        series: [{ 
            name: 'Reading',
            data: [570, 554, 573, 582, 578, 573],
            zIndex: 10
        },  {
            name: 'Reading (Statewide)',
            type: 'line',
            color: '#8085e9',
            data: [485, 482, 477, 478, 483, 480],
            zIndex: 1

        },  {
            name: 'Writing',
            data: [562, 547, 559, 570, 566, 562],
            zIndex: 10
        },  {
            name: 'Writing (Statewide)',
            type: 'line',
            color: '#f15c80',
            data: [478, 474, 470, 473, 471, 468], 
            zIndex: 1                
        }, {
            name: 'Math',
            data: [588, 576, 588, 597, 588, 588], 
            zIndex: 10
        },  {
            name: 'Math (Statewide)',
            type: 'line',
            showInTooltip: true,
            color: '#e4d354',
            data: [488, 482, 480, 479, 484, 481], 
            zIndex: 1   
    }],        
    subtitle: {text: 'Barrington High School'},
    title: {text: 'SAT Exams'},
    tooltip: {
        formatter: function() {
            var s = '<b>' + this.x + '</b>';
            $.each(this.points, function() {
                if (this.series.type != 'line') {
                    s += '<div>' + this.series.name + ': ' + this.y + '</div>';
                }
            });
            return s
        },
        shared: true,
        useHTML: true
    },
    xAxis: {
        categories: [
            '2009-2010',
            '2010-2011',
            '2011-2012',
            '2012-2013',
            '2013-2014',
            '2014-2015'
        ],
        crosshair: true
    },
    yAxis: {
        min: 200,
        max: 800,
        tickInterval: 200,
        title: {text: null}
    }
};


// PARCC ELA Grade 9 Tile
var PARCC_ELA9_options = {
    chart: {renderTo:'PARCC_ELA9_tile'},
    series: JSON.parse(JSON.stringify(bullseye_series_options)),
    title: {text: 'ELA/Literacy Grade 9'},
    tooltip: {pointFormat: '<span style="font-size: 0.9em; color: {point.color}">{point.name}</span><br><span style="font-size:2em; color: {point.color}; font-weight: bold">{point.y}%</span>',
},
    yAxis: {min: 0, max: 100}
};
PARCC_ELA9_options.series[0].data[0].y = 81;
PARCC_ELA9_options.series[0].data[1].y = 81;
PARCC_ELA9_options.series[0].data[2].y = 33;
PARCC_ELA9_options.series[0].data[3].y = 0;

// PARCC ELA Grade 10 Tile
var PARCC_ELA10_options = {
    chart: {renderTo:'PARCC_ELA10_tile'},
    series: JSON.parse(JSON.stringify(bullseye_series_options)),
    title: {text: 'ELA/Literacy Grade 10'},
    tooltip: {pointFormat: '<span style="font-size: 0.9em; color: {point.color}">{point.name}</span><br><span style="font-size:2em; color: {point.color}; font-weight: bold">{point.y}%</span>',
},
    yAxis: {min: 0, max: 100}
};
PARCC_ELA10_options.series[0].data[0].y = 71;
PARCC_ELA10_options.series[0].data[1].y = 71;
PARCC_ELA10_options.series[0].data[2].y = 31;
PARCC_ELA10_options.series[0].data[3].y = 0;

// PARCC Algebra Tile
var PARCC_algebra1_options = {
    chart: {renderTo:'PARCC_algebra1_tile'},
    series: JSON.parse(JSON.stringify(bullseye_series_options)),
    title: {text: 'Algebra 1'},
    tooltip: {pointFormat: '<span style="font-size: 0.9em; color: {point.color}">{point.name}</span><br><span style="font-size:2em; color: {point.color}; font-weight: bold">{point.y}%</span>',
},
    yAxis: {min: 0, max: 100}
};
PARCC_algebra1_options.series[0].data[0].y = 61;
PARCC_algebra1_options.series[0].data[1].y = 61;
PARCC_algebra1_options.series[0].data[2].y = 28;
PARCC_algebra1_options.series[0].data[3].y = 0;

// PARCC Geometry Tile
var PARCC_geometry_options = {
    chart: {renderTo:'PARCC_geometry_tile'},
    series: JSON.parse(JSON.stringify(bullseye_series_options)),
    title: {text: 'Geometry'},
    tooltip: {pointFormat: '<span style="font-size: 0.9em; color: {point.color}">{point.name}</span><br><span style="font-size:2em; color: {point.color}; font-weight: bold">{point.y}%</span>',
},
    yAxis: {min: 0, max: 100}
};
PARCC_geometry_options.series[0].data[0].y = 50;
PARCC_geometry_options.series[0].data[1].y = 50;
PARCC_geometry_options.series[0].data[2].y = 19;
PARCC_geometry_options.series[0].data[3].y = 0;


$(function() {
    Highcharts.setOptions(bullseye_chart);
    var SAT_math_tile = new Highcharts.Chart(SAT_math_options);
    var SAT_reading_tile = new Highcharts.Chart(SAT_reading_options);
    var SAT_writing_tile = new Highcharts.Chart(SAT_writing_options);
    var PARCC_ELA9_tile = new Highcharts.Chart(PARCC_ELA9_options);
    var PARCC_ELA10_tile = new Highcharts.Chart(PARCC_ELA10_options);
    var PARCC_algebra1_tile = new Highcharts.Chart(PARCC_algebra1_options);
    var PARCC_geometry_tile = new Highcharts.Chart(PARCC_geometry_options);
    SAT_math_tile.series[0].points[0].onMouseOver();
    SAT_reading_tile.series[0].points[0].onMouseOver();
    SAT_writing_tile.series[0].points[0].onMouseOver();
    PARCC_ELA9_tile.series[0].points[0].onMouseOver();
    PARCC_ELA10_tile.series[0].points[0].onMouseOver();
    PARCC_algebra1_tile.series[0].points[0].onMouseOver();
    PARCC_geometry_tile.series[0].points[0].onMouseOver();

});