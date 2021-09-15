


function drawHistoryLineChartChart(div_name, seg_id, layer_name, year_range, chart_option){
    //alert('Line Series');

   
    var divWidth = 400;
    var divHeight = 400;
    //var year_range = year_range;
    var aggregate_val = "average";
    var chart_title = "";

    if(chart_option.aggreagation_type != undefined)
        aggregate_val = chart_option.aggreagation_type;
    if(chart_option.chart_title != undefined)
        chart_title = chart_option.chart_title;
    
    var chart_title = d3.select(div_name).append("h4").text(chart_title).attr('style', 'text-align: center;padding: 10px;');
    var svg = d3.select(div_name).append("svg").attr('width', divWidth).attr('height', divHeight),
    margin = {top: 20, right: 20, bottom: 110, left: 40},
    margin2 = {top: 320, right: 20, bottom: 20, left: 40},
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom,
    height2 = +svg.attr("height") - margin2.top - margin2.bottom;

    var parseDate = d3.timeParse("%b %Y");

    d3.json("Data/" + data_library.variable_name_list[layer_name] + "/Monthly/id_" + seg_id + ".json").then(function(d) {
        var data = d.data;
        var month_array = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

        var temp_data = [];

        for(var year=year_range[0]; year<=year_range[1]; year++){
            for(var j=0; j<12; j++){
                var temp_obj = {};
                var date_str = month_array[j] + " " + year;
                temp_obj['date'] = parseDate(date_str);
                temp_obj['value'] = data[year][j][aggregate_val];
                temp_data.push(temp_obj);
            }
        }

        
        /*
        var data = [
            {date: parseDate('Jan 2000'), value: 100},
            {date: parseDate('Feb 2000'), value: 110},
            {date: parseDate('Mar 2000'), value: 130},
            {date: parseDate('Apr 2000'), value: 120}
        ];
        */

        drawChart(temp_data);
    });



var x = d3.scaleTime().range([0, width]),
    x2 = d3.scaleTime().range([0, width]),
    y = d3.scaleLinear().range([height, 0]),
    y2 = d3.scaleLinear().range([height2, 0]);

var xAxis = d3.axisBottom(x),
    xAxis2 = d3.axisBottom(x2),
    yAxis = d3.axisLeft(y);

var brush = d3.brushX()
    .extent([[0, 0], [width, height2]])
    .on("brush end", brushed);

var zoom = d3.zoom()
    .scaleExtent([1, Infinity])
    .translateExtent([[0, 0], [width, height]])
    .extent([[0, 0], [width, height]])
    .on("zoom", zoomed);


var area = d3.area()
    .curve(d3.curveMonotoneX)
    .x(function(d) { return x(d.date); })
    .y0(height)
    .y1(function(d) { return y(d.value); });


var area2 = d3.area()
    .curve(d3.curveMonotoneX)
    .x(function(d) { return x2(d.date); })
    .y0(height2)
    .y1(function(d) { return y2(d.value); });


svg.append("defs").append("clipPath")
    .attr("id", "clip")
  .append("rect")
    .attr("width", width)
    .attr("height", height);

var focus = svg.append("g")
    .attr("class", "focus")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var context = svg.append("g")
    .attr("class", "context")
    .attr("transform", "translate(" + margin2.left + "," + margin2.top + ")");



function drawChart(data) {

    x.domain(d3.extent(data, function(d) { return d.date; }));
    y.domain([0, d3.max(data, function(d) { return d.value; })]);
    x2.domain(x.domain());
    y2.domain(y.domain());

    focus.append("path")
        .datum(data)
        .attr("class", "area")
        .attr("d", area);

    focus.append("g")
        .attr("class", "axis axis--x")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    focus.append("g")
        .attr("class", "axis axis--y")
        .call(yAxis);

    context.append("path")
        .datum(data)
        .attr("class", "area")
        .attr("d", area2);

    context.append("g")
        .attr("class", "axis axis--x")
        .attr("transform", "translate(0," + height2 + ")")
        .call(xAxis2);

    context.append("g")
        .attr("class", "brush")
        .call(brush)
        .call(brush.move, x.range());

    svg.append("rect")
        .attr("class", "zoom")
        .attr("width", width)
        .attr("height", height)
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
        .call(zoom);
    };

    function brushed(event) {
        if (event.sourceEvent && event.sourceEvent.type === "zoom") return; // ignore brush-by-zoom
        //if(d3.zoom)
        //    return;
        var s = event.selection || x2.range();
        x.domain(s.map(x2.invert, x2));
        focus.select(".area").attr("d", area);
        focus.select(".axis--x").call(xAxis);
        svg.select(".zoom").call(zoom.transform, d3.zoomIdentity
            .scale(width / (s[1] - s[0]))
            .translate(-s[0], 0));
    }

    function zoomed(event) {
        if (event.sourceEvent && event.sourceEvent.type === "brush") return; // ignore zoom-by-brush
        var t = event.transform;
        x.domain(t.rescaleX(x2).domain());
        focus.select(".area").attr("d", area);
        focus.select(".axis--x").call(xAxis);
        context.select(".brush").call(brush.move, x.range().map(t.invertX, t));
    }

    function type(d) {
        d.date = parseDate(d.date);
        d.value = +d.value;
        return d;
    }
};



/*
* ========================================================================
*  Functions
* ========================================================================
*/

// === tick/date formatting functions ===
// from: https://stackoverflow.com/questions/20010864/d3-axis-labels-become-too-fine-grained-when-zoomed-in



