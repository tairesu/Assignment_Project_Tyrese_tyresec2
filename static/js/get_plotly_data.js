/*

Plotly code comes from a getting started tutorial @ https://plotly.com/javascript/
Shortly after that I built a view that returns trace json data (x & y) 
 I'm currently building a handler for Plotly, 
 and I stumbled upon the official documentation (https://plotly.com/javascript/reference/)

*/

function plot_design_usage(seed_data={},type='bar') {
    if (seed_data == {}) 
        return 
    
    console.log("Plotting Design usage");
    var trace1 = {
        type: type,
        x: seed_data['x'],
        y: seed_data['y'],
        marker: {
            color: 'white'
        },
        line: {
            simplify: true,
            width:6,
            color:'red'
        },
        
      };
      
      var data = [ trace1 ];
      
      var layout = {
        /* I found these two in the official documentation */
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: {size: 18},
        xaxis: {
            type: "date",
            gridcolor: 'transparent',
        },
        yaxis: {
            gridcolor: 'transparent'
        }
    }
  
      
      var config = {
        responsive: true,
        staticPlot: true,
    };
      Plotly.newPlot('__plot_design_usage', data, layout, config );


}

fetch('/stats/fetch_plotly_data')
    .then((res) => res.json())
    .then((data) => { 
        console.log("Data from /stats/fetch_plotly_data: ", data)
        plot_design_usage(seed_data=data, type='line')
    })