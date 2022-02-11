
window.onload = function () {
/* chart.js chart examples */

// chart colors
// var colors = ['#007bff','#28a745','#333333','#c3e6cb','#dc3545','#6c757d'];

// /* 3 donut charts */
var donutOptions = {
  cutoutPercentage: 80, 
  legend: {position:'bottom', padding:1, labels: {pointStyle:'circle', usePointStyle:false}}
};


var ctx = document.getElementById("myChart");
var myChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ["%PL da Carteira"],
        datasets: [{
            label: '# of Votes',
            data: [84.20,15.80],
            text: "ff",
            backgroundColor: [
             
                '#007bff'
            ],
            borderColor: [
               
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: donutOptions
});


new Chart(document.getElementById("bubble-chart"), {
    type: 'bubble',
    data: {
      labels: "Africa",
      datasets: [
        {
          label: ["IBX100"],
          backgroundColor: "rgba(255,221,50,0.2)",
          borderColor: "rgba(255,221,50,1)",
          data: [{
            x: 25,
            y: 150,
            r: 10
          }]
        }, {
          label: ["NCH Maracanã FIA"],
          backgroundColor: "rgba(60,186,159,0.2)",
          borderColor: "rgba(60,186,159,1)",
          data: [{
            x: 13,
            y: 140,
            r: 10
          }]
        }, {
          label: ["Ibovespa"],
          backgroundColor: "rgba(0,0,0,0.2)",
          borderColor: "#000",
          data: [{
            x: 27,
            y: 125,
            r: 10
          }]
        },
      ]
    },
    options: {
      title: {
        display: true,
        text: 'Risco x Retorno'
      }, scales: {
        yAxes: [{ 
          scaleLabel: {
            display: true,
            labelString: "Retorno desde o inicio (%)"
          }
        }],
        xAxes: [{ 
          scaleLabel: {
            display: true,
            labelString: "Risco/Vol Ano (%)"
          }
        }]
      }
    }
});

}