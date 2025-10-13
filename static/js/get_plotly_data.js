/*

Plotly code comes from a getting started tutorial @ https://plotly.com/javascript/
Shortly after that I built a view that returns trace json data (x & y) 
 I'm currently building a handler for Plotly, and I stumbled upon the official documentation (https://plotly.com/javascript/reference/)

I want my application to display multiple Plotly graphs given a list of graph data.
The original function for plotting a single graph was too long for my taste
I dislike functions >15 lines of code,
so I made a class to break up the code into readable blocks,

*/
class Plot {
    constructor(graph_data={}) {
        /* Process data from JSON object into class attributes  */
        this.traces = graph_data['traces'];
        this.target_elem = graph_data['target_elem'];
        /* Initialize the default values */
        this.__init_layout();
        this.__init_traces();
        this.__init_config();

    }
    /* Sets this class' layout attribute to a default layout object */
    __init_layout() {
        this.__set_layout({
            /* I found these two in the official documentation */
            autosize:false,
            automargin: false,
            paper_bgcolor: 'transparent',
            plot_bgcolor: 'transparent',
            font: {size: 12},
            margin: {b: '30',t:'0', l:'25', r:'0'},
            xaxis: {
                gridcolor: '#151c3057',
                color: 'white',
            },
            yaxis: {
                gridcolor: '#151c3057',
                color: '#0091CA',
            },
            width: 300,
            height:200,
        })
    }

    __set_layout(layout) {
        this.layout = layout;
    }
    /* Sets this class' trace attribute to a default trace object */
    __init_traces(){
        for (var i = 0; i < this.traces.length; i++) {
            var trace = this.traces[i];
            trace['marker'] = {
                size:15,
                color:'red',
            };
            trace['line'] = {
                simplify: true,
                width:6,
                color:'transparent',
            }
        }
    }

    /* Sets config to base configuration */
    __init_config() {
        let base_config = {};
        this.__set_config(base_config);
    }
    /* Set config class attribute to new config object */
    __set_config(config={}) { this.config = config }

    /* Plot the graph using the attributes of this class */
    plot(debug=false) {
        console.log('Plot instance calling plot method w/ graph data');

        Plotly.newPlot(this.target_elem, this.traces, this.layout, this.config );
    }
}

fetch('/stats/fetch_plotly_data')
    .then((res) => res.json())
    .then((data) => { 
        console.log("Data from /stats/fetch_plotly_data: ", data);
        /* Loop through each server provided graph and create new Plot instance*/
        for(var i=0; i< data.length; i++) {
            let graph_data = data[i];
            let plot = new Plot(graph_data);
            plot.plot(debug=true);
        }
    })