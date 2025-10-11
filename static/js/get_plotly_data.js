/*

Plotly code comes from following https://plotly.com/javascript/configuration-options/

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
        }
      };
      
      var data = [ trace1 ];
      
      var layout = {
        title: {
          text: ''
        },
        /* I found these two in the plotly javascript documentation */
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',

        font: {size: 18}
      };
      
      var config = {
        responsive: true
    };
      Plotly.newPlot('__plot_design_usage', data, layout, config );


}

fetch('/stats/fetch_plotly_data')
    .then((res) => res.json())
    .then((data) => { 
        console.log("Data from /stats/fetch_plotly_data: ", data)
        plot_design_usage(seed_data=data, type='line')
    })