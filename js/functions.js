function plot(data) {
    var Z = JSON.parse(data['Z']);
    var t = JSON.parse(data['t']);
    var Zh = JSON.parse(data['Zh']);
    var th = JSON.parse(data['th']);
    var Zh_u = JSON.parse(data['Zh_u']);
    var Zh_l = JSON.parse(data['Zh_l']);
    var Zh_res = JSON.parse(data['Zh_res']);

    var lastZ = Z[Z.length - 1];
    Zh.unshift(lastZ);
    Zh_u.unshift(lastZ);
    Zh_l.unshift(lastZ);
    Zh_res.unshift(lastZ);
    th.unshift(t[t.length - 1]);

    traces = [{
            x: th,
            y: Zh_l,
            type: 'scatter',
            mode: 'lines',
            name: 'Conf. Interval',
            'fillcolor': "rgba(0,40,100,0.2)",
            showlegend: false,
            marker: {
                color: '#7f7f7f'
            },
            legendgroup: 'group1',
        },
        {
            x: th,
            y: Zh_u,
            type: 'scatter',
            mode: 'lines',
            name: 'Conf. Interval',
            'fill': 'tonexty',
            'fillcolor': "rgba(0,40,100,0.2)",
            marker: {
                color: '#7f7f7f'
            },
            showlegend: false,
            legendgroup: 'group1',

        },
        {
            x: t,
            y: Z,
            name: 'Data',
            type: 'scatter',
            marker: {
                color: '#1f77b4'
            },
            legendgroup: 'group2',
        },
        {
            x: th,
            y: Zh,
            name: 'Forecast',
            type: 'scatter',
            marker: {
                color: '#2ca02c'
            },
            legendgroup: 'group3',
        },
        {
            x: th,
            y: Zh_res,
            name: 'Restricted Forecast',
            type: 'scatter',
            marker: {
                color: '#ff7f0e'
            },
            legendgroup: 'group4',
        }
    ];
    $output.show();
    Plotly.newPlot('chart', traces);
};

function print(data) {
    $summary.children().html(JSON.parse(data['summary'])['summary']);
    $summary.show();
}

function printError(msg) {
    $summary.children().html(msg);
    $summary.show();
    $output.hide();
}