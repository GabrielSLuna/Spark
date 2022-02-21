google.charts.load('current', {
    'packages':['geochart'],
    "mapsApiKey": "AIzaSyC0VzMW0SXEgauESPkZGLEFYsVJVTgFZco",
  });

google.charts.setOnLoadCallback(drawRegionsMap);


function drawRegionsMap() {
    var data = google.visualization.arrayToDataTable([
        ['State', 'Tweet Suicide'],
        ["BR-SE", 2]
    //       ['BR-PE', 300],
    //       ['BR-AM', 400]
  
      ]);

    $.ajax({
        url: '/shp_layer',
        contentType: 'application/json; charset=utf-8',
        success: function(response) {
            console.log(response);
            data.addRows(response);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.warn("Erro ao carregar grafico", errorThrown);
        },
    });
    
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

    chart.draw(data, options);
}