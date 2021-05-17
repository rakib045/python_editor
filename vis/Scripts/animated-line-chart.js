

function drawLineChart(info, var_name){
    //alert(seg_id);
    var year = parseInt(info.split(';##;')[0]);
    var month = parseInt(info.split(';##;')[1])-1;
    var month_name = info.split(';##;')[2];
    var seg_id = parseInt(info.split(';##;')[3]);
    
    var data = [{day:1, value:20}, {day:2, value:10}, {day:3, value:12}, {day:4, value:25}, {day:5, value:5}, {day:6, value:15},
      {day:7, value:20}, {day:8, value:10}, {day:9, value:12}, {day:10, value:25}, {day:11, value:5}, {day:12, value:15},
      {day:13, value:20}, {day:14, value:10}, {day:15, value:12}, {day:16, value:25}, {day:17, value:5}, {day:18, value:15},
      {day:19, value:20}, {day:20, value:10}, {day:21, value:12}, {day:22, value:25}, {day:23, value:5}, {day:24, value:15},
      {day:25, value:20}, {day:26, value:10}, {day:27, value:12}, {day:28, value:25}, {day:29, value:5}, {day:30, value:15}];

      d3.json("Data/" + var_name + "/Monthly/" + seg_id + ".json").then(function(d) {
        var data = d.data;

        var temp_data = [];

        var values = data[year][month].value;
        for(var i=0; i<values.length; i++)
        {
            var temp_obj = {};
            temp_obj['day'] = i+1;
            temp_obj['value'] = values[i];
            temp_data.push(temp_obj);
        }

        drawChart(temp_data, year, month_name);
    });

}

function drawChart(data, year, month){
    var margin = {top: 20, right: 20, bottom: 20, left: 35},
    width = 400 - margin.left - margin.right,
    height = 280 - margin.top - margin.bottom;

    //var parseDate = d3.timeParse("%d-%b-%y");

    var x = d3.scaleLinear()
            .range([0, width]);

    var y = d3.scaleLinear()
            .range([height, 0]);

    var color = d3.scaleOrdinal(d3.schemeCategory10);

    

    x.domain([1, d3.max(data, d=>d.day)]);
    y.domain([d3.min(data, d=>d.value)-50, d3.max(data, d=>d.value)+50]);

    var valueline = d3.line()//.curve(d3.curveBasis).curve(d3.curveLinear)
                    .x(function(d) { return x(d.day); })
                    .y(function(d) { return y(d.value); })
                    .curve(d3.curveMonotoneX);

    var svg = d3.select("#historyHeatMap").append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    svg.append("text")
        .attr("x", (width / 2))             
        .attr("y", 0 - (margin.top / 2))
        .attr("text-anchor", "middle")  
        .style("font-size", "12px") 
        .style("text-decoration", "underline")  
        .text("IRFroutedRunoff - " + month + " " + year);

    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x).ticks(6));
    svg.append("text")             
        .attr("transform",
              "translate(" + (width/2) + " ," + 
                             (height + margin.top + 20) + ")")
        .style("text-anchor", "middle")
        .text("Days");

    svg.append("g")
        .call(d3.axisLeft(y).ticks(7));

    var path = svg.append("path")
                .data([data])
                .attr("class", "line")
                .attr("d", valueline)
                .attr("fill", "none")
                .attr("stroke", "#e31a1c")
                .attr("stroke-width", "2px");

    const pathLength = path.node().getTotalLength();

    path.attr("stroke-dashoffset", pathLength)
    .attr("stroke-dasharray", pathLength);

    const transitionPath = d3.transition().ease(d3.easeSin).duration(2500);

    path.attr("stroke-dashoffset", pathLength)
    .attr("stroke-dasharray", pathLength)
    .transition(transitionPath)
    .attr("stroke-dashoffset", 0);

    var div_tooltip = d3.select("#historyHeatMap").append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

    svg.selectAll("myCircles")
      .data(data)
      .enter()
      .append("circle")
        .attr("fill", "white")
        .attr("stroke", "#e31a1c")
        .attr("stroke-width", "1px")
        .attr("cx", function(d) { return x(d.day) })
        .attr("cy", function(d) { return y(d.value) })
        .attr("r", 3)
        .attr("cursor", "pointer")
        .on("mouseover", function(event,d) {
            div_tooltip.transition()
              .duration(200)
              .style("opacity", .8);
            div_tooltip.html("<div> Day: " + d.day + "<br/>Value: " + d.value.toFixed(2) + " m3/s</div>")
              .style("left", (event.pageX-margin.left-margin.right) + "px")
              .style("top", (event.pageY) + "px");
        })
        .on("mouseout", function(d) {
            div_tooltip.transition()
              .duration(500)
              .style("opacity", 0);
        });
    
}