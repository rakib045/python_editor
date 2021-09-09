

function drawHistoryHeatMapChart(seg_id, layer_name, year_range, chart_option){
    //alert(seg_id);
    

    d3.json("Data/" + data_library.variable_name_list[layer_name] + "/Monthly/id_" + seg_id + ".json").then(function(d) {
        var data = d.data;

        console.log(data);

        var processed_data = [];
        var start_month = "Jan";
        var aggregate_val = "average";

        if(chart_option.start_year != undefined)
            year_range[0] = chart_option.start_year;

        if(chart_option.end_year != undefined)
            year_range[1] = chart_option.end_year;

        if(chart_option.start_month != undefined)
            start_month = chart_option.start_month;
        
        if(chart_option.aggreagation_type != undefined)
            aggregate_val = chart_option.aggreagation_type;

        //var year_list = Object.keys(data);
        var month_list_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        var month_index_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11];

        var index_rotate = month_list_labels.indexOf(start_month) - 12;
        for(var i=index_rotate; i < 0; i++){
            month_list_labels.unshift(month_list_labels.pop());
            month_index_list.unshift(month_index_list.pop());
        }

        var year_list_labels = [];
        var year_list = [];
        for(var index=year_range[0]; index <= year_range[1]; index++)
            year_list.push(index);
        for(var index=year_range[0]; index < year_range[1]; index++)
            year_list_labels.push(index + '/' + (index+1).toString().slice(-2) );
            
        /*
        for(var i=0; i<year_list.length; i++)
        {
            var month_data = data[year_list[i]];
            //var month_list = Object.keys(month_data);

            for(var j=0; j<month_index_list.length; j++){
                var value = month_data[month_index_list[j]][aggregate_val];
                var temp_obj = {};
                temp_obj['y_axis_index'] = i;
                temp_obj['x_axis_index'] = j;
                temp_obj['hover_text'] = month_list_labels[j] + " " + year_list[i] + "<br /> Value : " + value;
                temp_obj['value'] = value;

                processed_data.push(temp_obj);

                if(month_index_list[j] == 11){

                }
            }

        }
        */

        for(var i=0; i<(year_list.length-1);i++){
            year_index = i;
            for(var j=0; j<month_index_list.length; j++){
                                    
                    var temp_obj = {};
                    temp_obj['y_axis_index'] = i;
                    temp_obj['x_axis_index'] = j;
                    

                    var value = data[year_list[year_index]][month_index_list[j]][aggregate_val];
                    temp_obj['hover_text'] = month_list_labels[j] + " " + year_list[year_index] + "<br /> Value : " + value;
                    temp_obj['value'] = value;
                    
                    processed_data.push(temp_obj);
                    //console.log(month_list_labels[j] + ' ' + year_list[i]);

                    if(month_index_list[j] == 11){
                        year_index++;
                    }  
                             
            }
        }

        console.log(processed_data);

        drawHM_BoxChart(seg_id, layer_name, processed_data, year_list_labels, month_list_labels);
    });
   
}

function drawHM_BoxChart(seg_id, layer_name, data, y_axis_labels, x_axis_labels){

    var margin = { top: 20, right: 10, bottom: 30, left: 50 },
    width = 800 - margin.left - margin.right,
    height = 210 - margin.top - margin.bottom,
    gridSize = Math.floor(width / 24),
    legendElementWidth = gridSize,
    buckets = 10,
    colors = map_library.color_list_array[layer_name];

    var svg = d3.select("#historyHeatMap").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var div_tooltip1 = d3.select("#historyHeatMap").append("div")
    .attr("class", "tooltip1")
    .style("opacity", 0);

    
    var yearLabels = svg.selectAll(".yearLabel")
      .data(y_axis_labels)
      .enter().append("text")
        .text(function (d) { return d; })
        .attr("x", 0)
        .attr("y", function (d, i) { return i * gridSize; })
        .style("text-anchor", "end")
        .attr("transform", "translate(-2," + gridSize / 1.5 + ")");
        //.attr("class", function (d, i) { return ((i >= 0 && i <= 4) ? "yearLabel mono axis axis-workweek" : "yearLabel mono axis"); });

    var timeLabels = svg.selectAll(".timeLabel")
      .data(x_axis_labels)
      .enter().append("text")
        .text(function(d) { return d; })
        .attr("x", function(d, i) { return i * gridSize; })
        .attr("y", 0)
        .style("text-anchor", "middle")
        .attr("transform", "translate(" + gridSize / 2 + ", -6)");
        //.attr("class", function(d, i) { return ((i >= 7 && i <= 16) ? "timeLabel mono axis axis-worktime" : "timeLabel mono axis"); });

        
    var heatmapChart = function(data, layer_name) {

        var cards = svg.selectAll(".month")
            .data(data, function (d) { 
                return d.y_axis_index + ':' + d.x_axis_index; 
            });

        cards.append("title");

        cards.enter().append("rect")
            .attr("x", function (d) { return (d.x_axis_index) * gridSize; })
            .attr("y", function (d) { return (d.y_axis_index) * gridSize; })
            .attr("rx", 4)
            .attr("ry", 4)
            .attr("class", "month bordered")
            .attr("dt", function (d) { 
                //return colorScale(d.value);
                var year_str = y_axis_labels[d.y_axis_index];
                var month_str = x_axis_labels[d.x_axis_index];

                return year_str + ";##;" + d.x_axis_index + ";##;" + month_str + ";##;";
            })
            .attr("width", gridSize)
            .attr("height", gridSize)
            .style("fill", function (d) { 
                //return colorScale(d.value); 
                return colors[0];
            })
            .attr("cursor", "pointer")
            .on("mouseover", function(event,d) {
                var month_str = x_axis_labels[d.x_axis_index];

                div_tooltip1.transition()
                  .duration(200)
                  .style("opacity", .8);
                  //div_tooltip1.html("<div> Year: " + d.y_axis_index + ", Month: "+ month_str +"<br/>Value: " + d.value + " m3/s</div>")
                  div_tooltip1.html(d.hover_text)
                  .style("left", (event.pageX-margin.left-margin.right) + "px")
                  .style("top", (event.pageY) + "px");
            })
            .on("mouseout", function(d) {
                div_tooltip1.transition()
                  .duration(200)
                  .style("opacity", 0);
            })
            .on("click", function () { 
                drawLineChart(this.attributes.dt.value + seg_id, layer_name);             
    
            })
            .transition().duration(2000)
            .style("fill", function (d) {
                return colors[data_library.getIndexOfGrades(map_library.grade_list_array[layer_name], d.value)];
            });

        cards.transition().duration(1000)
            .style("fill", function (d) { 
                return colors[data_library.getIndexOfGrades(map_library.grade_list_array[layer_name], d.value)];
            });

        cards.select("title").text(function (d) { return d.value; });

        cards.exit().remove();

    }

    heatmapChart(data, layer_name);

}
