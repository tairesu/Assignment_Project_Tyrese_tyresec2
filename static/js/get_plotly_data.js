/*

Plotly code comes from a getting started tutorial @ https://plotly.com/javascript/
Shortly after that I built a view that returns trace json data (x & y) 
 I'm currently building a handler for Plotly, 
 and I stumbled upon the official documentation (https://plotly.com/javascript/reference/)

*/
/*
I dislike functions > 15 lines of code,
so I made a class to break up the code into readable blocks,
(and handle execution smoothly)

*/
class Plot {
    constructor(graph_data) {
        this.__load_base_layout(),
        this.__load_base_traces(),
        this.__load_base_config(),
        
        this.graph_data = graph_data;
        this.x = graph_data['x'];
        this.y = graph_data['y'];
        this.target_elem = graph_data['target_elem'];
        this.type = graph_data['type'];
        this.traces = this.__get_trace();
        this.layout = this.__get_layout();
        this.config = this.__get_config();

    }
    __load_base_layout() {
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
    __get_layout() {
        return this.layout;
    }
    __load_base_traces(){
        let base_trace = {
            type: this.type,
            x: this.x,
            y: this.y,
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
        this.__set_trace(base_trace);
    }

    __set_trace(trace={}){
        this.trace = trace;
    }

    __load_base_config() {
        let base_config = {};
        this.__set_config(base_config);
    }

    __set_config(config={}) {
        this.config = config
    }

    __get_trace() {
        return this.trace
    }
    __get_target_elem() {
        console.log("__get_target_elem:", this.target_elem);
        return this.target_elem;
    }
    __get_config() {
        return this.config;
    }

    plot() {
        console.log('Plot instance calling plot method w/ graph data:', this.graph_data);
        Plotly.newPlot(this.__get_target_elem(), this.__get_trace(), this.__get_layout(), this.__get_config() );
    }
}

fetch('/stats/fetch_plotly_data')
    .then((res) => res.json())
    .then((data) => { 
        console.log("Data from /stats/fetch_plotly_data: ", data);
        /* Loop through each server provided graph and create new Plot instance*/
        for(var i=0; i< data['graphs'].length; i++) {
            let graph_data = data['graphs'][i];
            let plot = new Plot(graph_data);
            plot.plot();
        }
    })