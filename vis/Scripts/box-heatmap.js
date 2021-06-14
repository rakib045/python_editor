

function drawHistoryHeatMapChart(seg_id, layer_name, year_range, aggregate_val='average'){
    //alert(seg_id);
    

    d3.json("Data/" + data_library.variable_name_list[layer_name] + "/Monthly/id_" + seg_id + ".json").then(function(d) {
        var data = d.data;

        var temp_data = [];

        //var year_list = Object.keys(data);

        var year_list = [];
        for(var index=year_range[0]; index <= year_range[1]; index++)
            year_list.push(index);

        for(var i=0; i<year_list.length; i++)
        {
            var month_data = data[year_list[i]];
            var month_list = Object.keys(month_data);

            for(var j=0; j<month_list.length; j++){
                var value = month_data[month_list[j]][aggregate_val];
                var temp_obj = {};
                temp_obj['year'] = i+1;
                temp_obj['month'] = j+1;
                temp_obj['value'] = value;

                temp_data.push(temp_obj);
            }

        }

        drawHM_BoxChart(temp_data, year_list, seg_id, layer_name);
    });
   
}

function drawHM_BoxChart(data, year_list, seg_id, layer_name){

    var margin = { top: 20, right: 10, bottom: 30, left: 30 },
    width = 800 - margin.left - margin.right,
    height = 380 - margin.top - margin.bottom,
    gridSize = Math.floor(width / 24),
    legendElementWidth = gridSize,
    buckets = 10,
    colors = map_library.color_list_array[layer_name];
    years = year_list,
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

    var svg = d3.select("#historyHeatMap").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var div_tooltip1 = d3.select("#historyHeatMap").append("div")
    .attr("class", "tooltip1")
    .style("opacity", 0);


    var yearLabels = svg.selectAll(".yearLabel")
      .data(years)
      .enter().append("text")
        .text(function (d) { return d; })
        .attr("x", 0)
        .attr("y", function (d, i) { return i * gridSize; })
        .style("text-anchor", "end")
        .attr("transform", "translate(-2," + gridSize / 1.5 + ")");
        //.attr("class", function (d, i) { return ((i >= 0 && i <= 4) ? "yearLabel mono axis axis-workweek" : "yearLabel mono axis"); });

    var timeLabels = svg.selectAll(".timeLabel")
      .data(months)
      .enter().append("text")
        .text(function(d) { return d; })
        .attr("x", function(d, i) { return i * gridSize; })
        .attr("y", 0)
        .style("text-anchor", "middle")
        .attr("transform", "translate(" + gridSize / 2 + ", -6)");
        //.attr("class", function(d, i) { return ((i >= 7 && i <= 16) ? "timeLabel mono axis axis-worktime" : "timeLabel mono axis"); });

    var heatmapChart = function(data, layer_name) {

        var cards = svg.selectAll(".month")
            .data(data, function (d) { return d.year + ':' + d.month; });

        cards.append("title");

        cards.enter().append("rect")
            .attr("x", function (d) { return (d.month - 1) * gridSize; })
            .attr("y", function (d) { return (d.year - 1) * gridSize; })
            .attr("rx", 4)
            .attr("ry", 4)
            .attr("class", "month bordered")
            .attr("dt", function (d) { 
                //return colorScale(d.value);
                var year_str = years[d.year - 1];
                var month_str = months[d.month - 1];

                return year_str + ";##;" + d.month + ";##;" + month_str + ";##;";
            })
            .attr("width", gridSize)
            .attr("height", gridSize)
            .style("fill", function (d) { 
                //return colorScale(d.value); 
                return colors[0];
            })
            .attr("cursor", "pointer")
            .on("mouseover", function(event,d) {
                var year_str = years[d.year - 1];
                var month_str = months[d.month - 1];

                div_tooltip1.transition()
                  .duration(200)
                  .style("opacity", .8);
                  div_tooltip1.html("<div> Year: " + year_str + ", Month: "+ month_str +"<br/>Value: " + d.value + " m3/s</div>")
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
