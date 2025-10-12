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
            size:15,
            color:'white',
        },
        line: {
            simplify: true,
            width:6,
            color:'transparent',
        },
        
      };
      
      var data = [ trace1 ];
      
      var layout = {
        /* I found these two in the official documentation */
        autosize:false,
        automargin: false,
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: {size: 12},
        margin: {b: '30',t:'0', l:'25', r:'0'},
        xaxis: {
            type: "date",
            gridcolor: '#151c3057',
            tickformat: '%m/%d',
            color: 'white',
        },
        yaxis: {
            
            gridcolor: '#151c3057',
            color: '#0091CA',
        },
        width: 300,
        height:200
    }
  
      
      var config = {
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