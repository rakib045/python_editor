function drawMultiSeriesLineChart()
{
    /*
    var data = [{
        name: "USA",
        values: [{
            date: "2000 01",
            value: "100"
        },
        {
            date: "2000 04",
            value: "110"
        },
        {
            date: "2000 08",
            value: "145"
        },
        {
            date: "2000 12",
            value: "241"
        },
        {
            date: "2001 01",
            value: "101"
        },
        {
            date: "2001 04",
            value: "90"
        },
        {
            date: "2001 08",
            value: "10"
        },
        {
            date: "2001 12",
            value: "35"
        }
        ]
    },
    {
        name: "Canada",
        values: [{
            date: "2000 01",
            value: "150"
        },
        {
            date: "2000 04",
            value: "110"
        },
        {
            date: "2000 08",
            value: "145"
        },
        {
            date: "2000 12",
            value: "241"
        },
        {
            date: "2001 01",
            value: "101"
        },
        {
            date: "2001 04",
            value: "90"
        },
        {
            date: "2001 08",
            value: "10"
        },
        {
            date: "2001 12",
            value: "35"
        }
        ]
    },
    {
        name: "Maxico",
        values: [{
            date: "2000 01",
            value: "50"
        },
        {
            date: "2000 04",
            value: "110"
        },
        {
            date: "2000 08",
            value: "145"
        },
        {
            date: "2000 12",
            value: "241"
        },
        {
            date: "2001 01",
            value: "101"
        },
        {
            date: "2001 04",
            value: "90"
        },
        {
            date: "2001 08",
            value: "10"
        },
        {
            date: "2001 12",
            value: "35"
        }
        ]
    }
    ];
    console.log(data);
    */
    data = sidebar_library.comparison_chart_data;
    console.log(data);
    if(data.length <= 0){
        return;
    }
        
    var width = 900;
    var height = 200;
    //var margin = 50;
    var margin = {'top': 20, 'left': 40, 'right' : 50, 'bottom':40};
    var duration = 250;

    var lineOpacity = "0.6";
    var lineOpacityHover = "0.9";
    var otherLinesOpacityHover = "0.4";
    var lineStroke = "2px";
    var lineStrokeHover = "3px";

    var circleOpacity = '0.9';
    var circleOpacityOnLineHover = "0.35"
    var circleRadius = 3;
    var circleRadiusHover = 6;


    /* Format Data */
    var parseDate = d3.timeParse("%Y %m");
    data.forEach(function(d) {
        d.values.forEach(function(d) {
            if(typeof d.date == "string")
            {
                d.date = parseDate(d.date);
                d.value = +d.value;
            }        
        });
    });


    /* Scale */
    var xScale = d3.scaleTime()
    .domain(d3.extent(data[0].values, d => d.date))
    //.range([0, width - margin]);
    .range([0, width - margin.right]);

    var yScale = d3.scaleLinear()
    .domain([0, d3.max(data[0].values, d => d.value)])
    //.range([height - margin, 0]);
    .range([height - margin.bottom, 0]);

    var color = d3.scaleOrdinal(d3.schemeCategory10);

    /* Add SVG */
    var svg = d3.select("#comparisonChart").append("svg")
    //.attr("width", (width + margin) + "px")
    //.attr("height", (height + margin) + "px")
    .attr("width", (width + margin.right) + "px")
    .attr("height", (height + margin.bottom) + "px")
    .append('g')
    //.attr("transform", `translate(${margin}, ${margin})`);
    .attr("transform", `translate(${margin.left}, ${margin.top})`);


    /* Add line into SVG */
    var line = d3.line()
    .x(d => xScale(d.date))
    .y(d => yScale(d.value));

    let lines = svg.append('g')
    .attr('class', 'lines');

    const index = d3.local();

    lines.selectAll('.line-group')
    .data(data).enter()
    .append('g')
    .attr('id',function(d){ return d.name.replace(/\s+/g, '')+"-line"; })
    .attr('class', 'line-group')
    .each(function(d, i) {
        index.set(this, i);            // Store index in local variable.
      })
    .on("mouseover", function(event, d, i) {
        svg.append("text")
        .attr("class", "title-text")
        .style("fill", d.color)
        .text(d.name)
        .attr("text-anchor", "middle")
        //.attr("x", (width - margin) / 2)
        .attr("x", (width/2 + margin.left))
        .attr("y", 5);
    })
    .on("mouseout", function(d) {
        svg.select(".title-text").remove();
    })
    .append('path')
    .attr('class', 'line')
    .attr('d', d => line(d.values))
    .style('stroke', (d, i) => d.color)
    .style('opacity', lineOpacity)
    .on("mouseover", function(d) {
        d3.selectAll('.line')
        .style('opacity', otherLinesOpacityHover);
        d3.selectAll('.circle')
        .style('opacity', circleOpacityOnLineHover);
        d3.select(this)
        .style('opacity', lineOpacityHover)
        .style("stroke-width", lineStrokeHover)
        .style("cursor", "pointer");
    })
    .on("mouseout", function(d) {
        d3.selectAll(".line")
        .style('opacity', lineOpacity);
        d3.selectAll('.circle')
        .style('opacity', circleOpacity);
        d3.select(this)
        .style("stroke-width", lineStroke)
        .style("cursor", "none");
    });


    /* Add circles in the line */
    lines.selectAll("circle-group")
    .data(data).enter()
    .append("g")
    .attr('id',function(d){ return d.name.replace(/\s+/g, '')+"-circle"; })
    .style("fill", (d, i) => d.color)
    .selectAll("circle")
    .data(d => d.values).enter()
    .append("g")
    .attr("class", "circle")
    .on("mouseover", function(event, d) {
        var txt = `${d.value }` + " (" + moment(d.date).format('MMM YY') + ")";
        d3.select(this)
        .style("cursor", "pointer")
        .append("text")
        .attr("class", "text")
        .text(txt)
        .attr("x", d => xScale(d.date) )
        .attr("y", d => yScale(d.value) - 10);
    })
    .on("mouseout", function(event, d) {
        d3.select(this)
        .style("cursor", "none")
        .transition()
        .duration(duration)
        .selectAll(".text").remove();
    })
    .append("circle")
    .attr("cx", d => xScale(d.date))
    .attr("cy", d => yScale(d.value))
    .attr("r", circleRadius)
    .style('opacity', circleOpacity)
    .on("mouseover", function(d) {
        d3.select(this)
        .transition()
        .duration(duration)
        .attr("r", circleRadiusHover);
    })
    .on("mouseout", function(d) {
        d3.select(this)
        .transition()
        .duration(duration)
        .attr("r", circleRadius);
    });


    /* Add Axis into SVG */
    var xAxis = d3.axisBottom(xScale).ticks(5);
    var yAxis = d3.axisLeft(yScale).ticks(5);

    svg.append("g")
    .attr("class", "x axis")
    //.attr("transform", `translate(0, ${height-margin})`)
    .attr("transform", `translate(0, ${height-margin.bottom})`)
    .call(xAxis);

    svg.append("g")
    .attr("class", "y axis")
    .call(yAxis)
    .append('text')
    .attr("y", 15)
    .attr("transform", "rotate(-90)")
    .attr("fill", "#000")
    .text("Value");


    //var dataNest = d3.nest()
    //.key(function(d) {
    //    return d.name;
    //})
    //.entries(data);
    var dataNest_temp = d3.group(data, d => d.name);

    var dataNest = Array.from(dataNest_temp, ([name, value]) => ({ name, value }));

    var legendSpace = width / dataNest.length;

    // Loop through each symbol / key
    dataNest.forEach(function(d, i) {

    // Add the Legend
    svg.append("text")
        .attr("x", (legendSpace / 2) + i * legendSpace) // space legend
        .attr("y", height)
        .attr("class", "legend") // style the legend
        .style("fill", d.value[0].color)
        .on("click", function() {
        // Determine if current line is visible
        var active = d.active ? false : true,
            newOpacity = active ? 0 : 1;
        var visibility = active ? '' : 'none';
        // Hide or show the elements based on the ID
        d3.select("#" + d.name.replace(/\s+/g, '') + "-line")
            .transition().duration(100)
            //.style("opacity", newOpacity);
            .style("display", visibility)
        d3.select("#" + d.name.replace(/\s+/g, '') + "-circle")
            .transition().duration(100)
            //.style("opacity", newOpacity);
            .style("display", visibility);
        // Update whether or not the elements are active
            d.active = active;
        })
        .text(d.name);
    });
}