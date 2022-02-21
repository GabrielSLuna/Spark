
(function ($) {
  // USE STRICT
  "use strict";
  try {
    let data_graph, labels;
    $.ajax({
      url: '/graph_tweet',
      contentType: 'application/json; charset=utf-8',
      // data: json_data,
      success: function(response) {
          data_graph = response['tweet_per_day'];
          callchart(data_graph);
      },
      error: function (jqXHR, textStatus, errorThrown) {
          console.warn("Erro ao carregar grafico", errorThrown);
          alertaErro("Erro ao carregar grafico");
      },
    });

    //Team chart
    function callchart(params) {
      var ctx = document.getElementById("team-chart");
      if (ctx) {
        ctx.height = 150;
        var myChart = new Chart(ctx, {
          type: 'line',
          data: {
            // labels: labels,
            type: 'line',
            defaultFontFamily: 'Poppins',
            datasets: [{
              data: params,
              label: "Tweet suicide",
              backgroundColor: 'rgba(0,103,255,.15)',
              borderColor: 'rgba(0,103,255,0.5)',
              borderWidth: 3.5,
              pointStyle: 'circle',
              pointRadius: 5,
              pointBorderColor: 'transparent',
              pointBackgroundColor: 'rgba(0,103,255,0.5)',
            },]
          },
          options: {
            responsive: true,
            tooltips: {
              mode: 'index',
              titleFontSize: 12,
              titleFontColor: '#000',
              bodyFontColor: '#000',
              backgroundColor: '#fff',
              titleFontFamily: 'Poppins',
              bodyFontFamily: 'Poppins',
              cornerRadius: 3,
              intersect: false,
            },
            legend: {
              display: false,
              position: 'top',
              labels: {
                usePointStyle: true,
                fontFamily: 'Poppins',
              },
  
  
            },
            scales: {
              xAxes: [{
                display: true,
                type: 'time',
                time: {
                  unit: 'day'
                },
                gridLines: {
                  display: false,
                  drawBorder: false
                },
                scaleLabel: {
                  display: false,
                  labelString: 'Day'
                },
                ticks: {
                  fontFamily: "Poppins"
                }
              }],
              yAxes: [{
                display: true,
                gridLines: {
                  display: false,
                  drawBorder: false
                },
                scaleLabel: {
                  display: true,
                  labelString: 'Value',
                  fontFamily: "Poppins"
                },
                ticks: {
                  fontFamily: "Poppins",
                  beginAtZero: true
                }
              }]
            },
            title: {
              display: false,
            }
          }
        });
      }
    }


  } catch (error) {
    console.log(error);
  }

})(jQuery);

