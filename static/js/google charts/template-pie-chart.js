
// Load the Visualization API and the corechart package.
google.charts.load('current', {'packages':['corechart']});

// Set a callback to run when the Google Visualization API is loaded.
google.charts.setOnLoadCallback(drawChart);

// Callback that creates and populates a data table,
// instantiates the pie chart, passes in the data and
// draws it.
function drawChart() {

// Create the data table.
var data = new google.visualization.DataTable();
data.addColumn('string', 'Topping');
data.addColumn('number', 'Slices');
data.addColumn({type: 'string', role: 'link'});
data.addColumn({type: 'string', role: 'style'});

data.addRows([
    ['Projects', project_total_count, '/projects', 'cursor: pointer;'],
    ['Tickets', 3, '/projects', 'cursor: pointer;'],
    ['Bug Reports', 18, '/projects', 'cursor: pointer;'],
    ['Feature Requests', 3, '/projects', 'cursor: pointer;']
]);

// Set chart options
var options = {'backgroundColor':'none',
                colors: ['#5cb85c', '#5bc0de', '#f0ad4e', '#d9534f', '#333333', '#DDDDDD', '#bd5916', '#4e5d6c'],
                pieHole: 0.5,
                pieSliceText: 'value',
                tooltip: {
                    ignoreBounds: false
                },
                pieSliceTextStyle: {
                    'color':'white',
                    'fontName': 'Lato',
                    'fontSize': 16
                },
                legend: {
                    textStyle: {
                        'color':'white',
                        'fontName': 'Lato',
                        'fontSize': 12
                    },
                    alignment: 'center',
                    position: 'right',
                },
                chartArea: {
                    width:'85%',
                    height:'85%'
                }
            };

// Instantiate and draw our chart, passing in some options.
var chartpie = new google.visualization.PieChart(document.getElementById('chart_div1'));
google.visualization.events.addListener(chartpie, 'select', function (e) {
            var selection = chartpie.getSelection();
                if (selection.length) {
                    var row = selection[0].row;
                    let link = data.getValue(row, 2);
                    location.href = link;
                }
            });
// google.visualization.events.addListener(chartpie, 'onmouseover', mouseHandlerPointer1);                 
// google.visualization.events.addListener(chartpie, 'onmouseout', mouseHandlerDefault1);

chartpie.draw(data, options);
}