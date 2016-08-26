{% load config %}
$(function () {
    $('#{{name}}').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: '{{detail.title}}'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.0f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.0f} %',
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    }
                }
            }
        },
        {% if type == 'state' %}
        series: [{% for key, values in series.items %}{
            name: '{{values.name}}',
            colorByPoint: {{values.colorByPoint}},
            data: [{% for row in values.data %}{
                name: '{{ row.name }}',
                {% get_state_value indicator school_year row.y.y row.y.x as data%}
                namey: '{{row.y.y}}',
                namex: '{{row.y.x}}',
                y: {{data.key_value}}
            },{% endfor %}]
        }{% endfor %}]
        {% elif type == 'district' %}
        series: [{% for key, values in series.items %}{
            name: '{{values.name}}',
            colorByPoint: {{values.colorByPoint}},
            data: [{% for row in values.data %}{
                name: '{{ row.name }}',
                {% get_district_value indicator school_year row.y.y row.y.x as data%}
                namey: '{{row.y.y}}',
                namex: '{{row.y.x}}',
                y: {{data.key_value}}
            },{% endfor %}]
        }{% endfor %}]
        {% elif type == 'school' %}
        series: [{% for key, values in series.items %}{
            name: '{{values.name}}',
            colorByPoint: {{values.colorByPoint}},
            data: [{% for row in values.data %}{
                name: '{{ row.name }}',
                {% get_school_value indicator school_year row.y.y row.y.x as data%}
                namey: '{{row.y.y}}',
                namex: '{{row.y.x}}',
                y: {{data.key_value}}
            },{% endfor %}]
        }{% endfor %}]
        {% endif %}
        
    });
});

