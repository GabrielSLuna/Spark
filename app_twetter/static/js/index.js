google.charts.load('current', {
    'packages':['geochart'],
    "mapsApiKey": "AIzaSyC0VzMW0SXEgauESPkZGLEFYsVJVTgFZco",
  });

google.charts.setOnLoadCallback(drawRegionsMap);


function drawRegionsMap() {
    var options = {};

    var chart = new google.visualization.GeoChart(document.getElementById('vmap'));
    var options = {
        region: 'BR',
        resolution: 'provinces',
        width: 850,
        height: 500,
        backgroundColor: '#4569FD',
        colorAxis: {
            colors: ['#FF9999', '#CC0000']
        } // orange to blue 
    };

    $.ajax({
        url: '/shp_layer',
        contentType: 'application/json; charset=utf-8',
        success: function(response) {
            console.log(response);
            // let data = google.visualization.arrayToDataTable([]);
            let data = new google.visualization.DataTable();
            data.addColumn('string', 'State');
            data.addColumn('number', 'Tweet Suicide');
            // let datum = [['State', 'Tweet Suicide']].concat(response);
            // for (var d in datum) {
            //     data.addRows(datum);
            // }
            data.addRows(response);

            chart.draw(data, options);

        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.warn("Erro ao carregar grafico", errorThrown);
        },
    });
    
}