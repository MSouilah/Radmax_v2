// https://github.com/chrispahm/chartjs-plugin-dragdata

var graph_colors = {
    "c_strain": "#ffbf80",
    "c_dw": "#00e6ac",
    "c_data": "#3e95cd",
    "c_fit": "#9999ff",
    "c_fit_live": "#ff0000",
    "graph_colors['PointselectedColor']": "#ff0000",
};

function Read_new_scales(){
    scale_min_strain = strain_chart.scales.x.min;
    scale_max_strain = strain_chart.scales.x.max;
    scale_min_dw = dw_chart.scales.x.min;
    scale_max_dw = dw_chart.scales.x.max;
    dw_chart_zoomed = 1;
    strain_chart_zoomed = 1;
    if(dw_chart.getZoomLevel() == 1){
        dw_chart_zoomed = 0;
    }
    if(strain_chart.getZoomLevel() == 1){
        strain_chart_zoomed = 0;
    }
}

var yAxesDW = "";
var config_strain = {
    type: 'line',
    data: {
        datasets: [
            {
                type: 'scatter',
                xAxisID:'x',
                data: [],
                label: "Strain_line",
                borderColor: graph_colors['c_strain'],
                showLine: true,
                dragData: false
            },
            {
                type: 'scatter',
                xAxisID:'x',
                data: [],
                label: "Strain_scatter",
                borderColor: graph_colors['c_strain'],
                backgroundColor: graph_colors['c_strain'],
                parsing: false,
                fill: false,
                pointRadius: 16,
                pointHoverRadius: 16,
                pointBackgroundColor: [],
                pointBorderColor: []
            }
        ]
    },
    options: {
        onClick(e) {
            if(e.native.ctrlKey){
                const activePoints = strain_chart.getElementsAtEventForMode(
                    e,
                    'nearest',
                    {intersect: true},
                    false
                )
                if(activePoints.length > 0 && activePoints[0].datasetIndex == 1){
                    var ind = activePoints[0].index;
                    var test = strain_chart.data.datasets[1].pointBackgroundColor[ind];
                    if(test != graph_colors['PointselectedColor']){
                        strain_chart.data.datasets[1].pointBackgroundColor[ind] = graph_colors['PointselectedColor'];
                    }else{
                        strain_chart.data.datasets[1].pointBackgroundColor[ind] = graph_colors['c_strain'];
                    }
                    strain_chart.update();
                    test_selected_points(strain_chart);
                }
            }
        },
        responsive: true,
        parsing: false,
        animation: {
            duration: 0
        },
        elements: {
            line: {
                tension: 0.4
            }
        },
        scales: {
            x: [
                {
                    display: true,
                    type: 'linear',
                    ticks: {
                        display: 'auto'
                    },
                    reverse: true,
                    grid: {
                        display: true
                      }
                }
            ],
            y: {
                id: 'yAxis1',
                display: true,
                title: {
                    display: true,
                    text: 'Strain (%)'
                },
                ticks: {
                    callback: function(value, index, values) {
                        return index % 2 === 0 ? value.toFixed(2) : '' ;
                    }
                }
            }
        },
        plugins: {
            zoom: {
                zoom: {
                    drag:{
                        enabled: true,
                        modifierKey: 'ctrl',
                        borderColor: 'rgb(0, 230, 172)'
                    },
                    mode: 'xy',
                    // onZoomComplete: Read_new_scales
                }
            },
            tooltip:{
                enabled: false
            },
            legend: {
                display: false
            },
            dragData: {
                showTooltip: false, // show the tooltip while dragging [default = true]
                dragX: false,
                onDragStart: function(e,  datasetIndex, index) {
                    startingValueDrag = strain_chart.data.datasets[datasetIndex].data[index].y;
                },
                onDrag: function(e, datasetIndex, index, value) {             
                    // you may control the range in which datapoints are allowed to be
                    // dragged by returning `false` in this callback
                    value2add = value.y - startingValueDrag;
                    startingValueDrag = strain_chart.data.datasets[datasetIndex].data[index].y;
                     if(isSelectedPoints){
                        Object.entries(strain_chart.data.datasets[datasetIndex].data).forEach(([key, val]) => {
                            if(SelectedPoints.includes(parseInt(key))){
                                previous_value = strain_chart.data.datasets[datasetIndex].data[key].y; 
                                strain_chart.data.datasets[datasetIndex].data[key].y = previous_value + value2add;
                            }
                        })
                    }else{
                        strain_chart.data.datasets[datasetIndex].data[index] = value;
                    }
                    strain_chart.update();
                },
                onDragEnd: function(e, datasetIndex, index, value) {
                // you may use this callback to store the final datapoint value
                // (after dragging) in a database, or update other UI elements that
                // dependent on it
                    update_contraints_graph("Strain", datasetIndex, index, value);
                    reset_zoom(1);
                }
            },
            scales: {
                y: {
                  dragData: true
                }
              }
        }
    }
}

var config_dw = {
    type: 'line',
    data: {
        datasets: [
            {
                type: 'scatter',
                xAxisID:'x',
                data: [],
                label: "Dw_line",
                borderColor: "#ffbf80",
                showLine: true,
                dragData: false
            },
            {
                type: 'scatter',
                xAxisID:'x',
                data: [],
                label: "Dw_scatter",
                borderColor: graph_colors['c_dw'],
                backgroundColor: graph_colors['c_dw'],
                fill: false,
                pointRadius: 16,
                pointHoverRadius: 16,
                // pointBackgroundColor: [],
                // pointBorderColor: []
            }
        ]
    },
    options: {
        onClick(e) {
            if(e.native.ctrlKey){
                const activePoints = dw_chart.getElementsAtEventForMode(
                    e,
                    'nearest',
                    {intersect: true},
                    false
                )
                if(activePoints.length > 0 && activePoints[0].datasetIndex == 1){
                    var ind = activePoints[0].index;
                    var test = dw_chart.data.datasets[1].pointBackgroundColor[ind];
                    if(test != graph_colors['PointselectedColor']){
                        dw_chart.data.datasets[1].pointBackgroundColor[ind] = graph_colors['PointselectedColor'];
                    }else{
                        dw_chart.data.datasets[1].pointBackgroundColor[ind] = graph_colors['c_dw'];
                    }
                    dw_chart.update();
                    test_selected_points(dw_chart);
                }
            }
        },
        responsive: true,
        parsing: false,
        animation: {
            duration: 0
        },
        elements: {
            line: {
                tension: 0.4
            }
        },
        // layout: {
        //     padding: {
        //         left: 50,
        //         right: 50,
        //     }
        // },
        scales: {
            x: {
                id:'x',
                display: true,
                title: {
                    display: true,
                    text: 'Depth (\u00C5)'
                },
                ticks: {
                    major: {
                    fontStyle: 'bold',
                    fontColor: '#FF0000'
                    }
                },
                // reverse: true
            },
            y: {
                display: true,
                min: 0,
                max: 10,
                title: {
                    display: true,
                    text: 'Debye-Waller factor'
                },
                ticks: {
                    callback: function(value, index, values) {
                        return value.toFixed(2);
                    }
                }
            }
        },
        plugins: {
            zoom: {
                zoom: {
                    drag:{
                        enabled: true,
                        modifierKey: 'ctrl',
                        borderColor: 'rgb(0, 230, 172)'
                    },
                    mode: 'xy',
                    // onZoomComplete: Read_new_scales
                }
            },
            tooltip:{
                enabled: false
            },
            legend: {
                display: false
            },
            dragData: {
                showTooltip: false, // show the tooltip while dragging [default = true],
                dragX: false,
                onDragStart: function(e,  datasetIndex, index) {
                    startingValueDrag = dw_chart.data.datasets[datasetIndex].data[index].y;
                },
                onDrag: function(e, datasetIndex, index, value) {             
                    // you may control the range in which datapoints are allowed to be
                    // dragged by returning `false` in this callback
                    value2add = value.y - startingValueDrag;
                    startingValueDrag = dw_chart.data.datasets[datasetIndex].data[index].y;
                     if(isSelectedPoints){
                        Object.entries(dw_chart.data.datasets[datasetIndex].data).forEach(([key, val]) => {
                            if(SelectedPoints.includes(parseInt(key))){
                                previous_value = dw_chart.data.datasets[datasetIndex].data[key].y; 
                                dw_chart.data.datasets[datasetIndex].data[key].y = previous_value + value2add;
                            }
                        })
                    }else{
                        dw_chart.data.datasets[datasetIndex].data[index] = value;
                    }
                    dw_chart.update();
                },
                onDragEnd: function(e, datasetIndex, index, value) {
                // you may use this callback to store the final datapoint value
                // (after dragging) in a database, or update other UI elements that
                // dependent on it
                    update_contraints_graph("DW", datasetIndex, index, value)
                    reset_zoom(1);
                }
            },
            scales: {
                y: {
                  dragData: true
                }
              }
        }
    }
}

var config_xrd_gaph = {
    // type: 'line',
    data: {
        datasets: [
            {
                type: 'scatter',
                label: "xrd_graph",
                data: [],
                borderColor: "#3e95cd",
                showLine: true,
                xAxisID: "x",
            },
            {
                type: 'scatter',
                label: "xrd_fit",
                data: [],
                borderColor: "#9999ff",
                showLine: true,
                xAxisID: "x",
            }
        ]
    },
    options: {
        responsive: true,
        animation: {
            duration: 0
        },
        elements: {
            line: {
                tension: 0.4
            }
        },
        scales: {
            x: {
                display: true,
                id:'x',
                title: {
                    display: true,
                    text: '2\uD835\uDEB9(deg.)'
                },
                ticks: {
                    major: {
                        fontStyle: 'bold',
                        fontColor: '#FF0000',
                        // precision: 2,
                        // autoSkip: true,
                        // maxRotation: 0,
                        // minRotation: 0,
                    },
                    callback: function(value) {
                        // console.log(this.getLabelForValue(value))                       
                        return value.toFixed(2)
                        // return this.getLabelForValue(value).toFixed(2);
                    }
                }
            },
            y: {
                display: true,
                type: 'logarithmic',
                title: {
                    display: true,
                    text: 'Intensity (a.u.)'
                },
                ticks: {
                    callback: function(val, index, values) {
                        return val;
                    }
                }
            }
        },
        plugins: {
            legend: {
                display: false
            },
            tooltip:{
                enabled: false
            },
            zoom: {
                zoom: {
                    drag:{
                        enabled: true,
                        modifierKey: 'ctrl',
                        borderColor: 'rgb(0, 230, 172)'
                    },
                    mode: 'xy',
                    // onZoomComplete: Read_new_scales
                }
            },
            annotation: {
                annotations: {}
              }
        }
    }
}

function reset_color_points(chart, color){
    chart.data.datasets[1].pointBackgroundColor = [];
    chart.data.datasets[1].pointBorderColor = [];
    for (var i = 0; i <= chart.data.datasets[1].data.length - 1; i++) {
        chart.data.datasets[1].pointBackgroundColor[i] = color;
        chart.data.datasets[1].pointBorderColor[i] = color;
    }
}

function reset_selected_points(chart, color){
    chart.data.datasets[1].pointBackgroundColor = [];
    chart.data.datasets[1].pointBorderColor = [];
    for (var i = 0; i <= chart.data.datasets[1].data.length - 1; i++) {
        chart.data.datasets[1].pointBackgroundColor[i] = color;
        chart.data.datasets[1].pointBorderColor[i] = color;
    }
    SelectedPoints = [];
    isSelectedPoints = false;
    chart.update();
}

function test_selected_points(chart){
    isSelectedPoints = false;
    SelectedPoints = [];
    for (var i = 0; i <= chart.data.datasets[1].data.length - 1; i++) {
        if(chart.data.datasets[1].pointBackgroundColor[i] == graph_colors['PointselectedColor']){
            SelectedPoints.push(i)
            isSelectedPoints = true;
        }
    }
    SelectedPoints = Array.from(new Set(SelectedPoints));
    if(!isSelectedPoints){
        SelectedPoints = [];
    }
}

function reset_zoom(val){
    if(val == 1){
        isROI = false;
        reset_selected_points(strain_chart, graph_colors['c_strain']);
        reset_selected_points(dw_chart, graph_colors['c_dw']);
        selectionContextStrain.clearRect(0, 0, canvas_strain.width, canvas_strain.height);
        selectionContextDw.clearRect(0, 0, canvas_dw.width, canvas_dw.height);
    }
    if(xrd_gaph.isZoomedOrPanned()){
        xrd_gaph.resetZoom();
    }
    if(strain_chart.isZoomedOrPanned()){
        strain_chart.resetZoom();
    }
    if(dw_chart.isZoomedOrPanned()){
        dw_chart.resetZoom();
    }
}
