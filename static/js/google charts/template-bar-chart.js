
<script type="text/javascript">
    google.charts.load('current', {packages: ['corechart', 'bar']});
    google.charts.setOnLoadCallback(drawBasic);

    function drawBasic() {
    
        var data = new google.visualization.DataTable();
            data.addColumn('string', 'Topping');
            data.addColumn('number', 'Slices');
            data.addColumn({type: 'string', role: 'style'});
            data.addColumn({type: 'string', role: 'link'});
            
            data.addRows([
                ['Unresolved', 4, 'color: #d9534f; stroke-opacity: 1; stroke-color: #FFFFFF; stroke-width: 2;', '/tickets/search/type/Bug Report'],
                ['In Progress', 1, 'color: #f0ad4e; stroke-opacity: 1; stroke-color: #FFFFFF; stroke-width: 2;', '/tickets/search/type/Feature Request'],
                ['Resolved', 3, 'color: #5cb85c; stroke-opacity: 1; stroke-color: #FFFFFF; stroke-width: 2;', '/tickets/search/priority/Critical'],
                ['More Details Required', 1, 'color: #5bc0de; stroke-opacity: 1; stroke-color: #FFFFFF; stroke-width: 2;', '/tickets/search/status/New']
            ]);
        /*
        var data = google.visualization.arrayToDataTable([
            ['Status', 'Count', { role: 'style' }, { role: 'annotation' } ],
            ['Unresolved', 2, 'color: #d9534f; stroke-opacity: 1; stroke-color: #FFFFFF;', 'Cu' ],
            ['In Progress', 1, 'color: #f0ad4e; stroke-opacity: 1; stroke-color: #FFFFFF;', 'Ag' ],
            ['Resolved', 3, 'color: #5cb85c; stroke-opacity: 1; stroke-color: #FFFFFF;', 'Au' ],
            ['More Details Required', 1, 'color: #333333; stroke-opacity: 1; stroke-color: #FFFFFF;', 'Pt' ]
        ]);
        */

          var options = {
                    'backgroundColor':'none',
                    colors: ['#4e5d6c','#5cb85c', '#5bc0de', '#f0ad4e', '#d9534f', '#333333', '#DDDDDD', '#bd5916'],
                    bar: {
                        groupWidth: "90%"
                    },
                    legend: {
                        'position': 'none'
                    },
                    hAxis: {
                        minorGridlines: {
                            'color':'none'
                        },
                        gridlines: {
                            'color':'none'
                        },
                        textStyle: {
                        'color':'white',
                        'fontName': 'Lato',
                        'fontSize': 12
                        },
                        textPosition: 'in',
                        maxAlternation: 4,
                        maxTextLines: 3
                    },
                    vAxis: {
                        minorGridlines: {
                            'color':'none'
                        },
                        gridlines: {
                            'color':'none'
                        },
                        textPosition: 'none'
                    },
                    bar: {
                        groupWidth: "80%"
                    },
                    chartArea: {
                        width:'85%',
                        height:'85%'
                    }
            };

            var chart = new google.visualization.ColumnChart(document.getElementById('chart_div2'));
            
            google.visualization.events.addListener(chart, 'select', function (e) {
                var selection = chart.getSelection();
                    if (selection.length) {
                        var row = selection[0].row;
                        let link = data.getValue(row, 3);
                        location.href = link;
                    }
                });

            // google.visualization.events.addListener(chart, 'onmouseover', mouseHandlerPointer2);                 
            // google.visualization.events.addListener(chart, 'onmouseout', mouseHandlerDefault2);
            chart.draw(data, options);
        }
</script>