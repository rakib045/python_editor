from util_library import *
# Initialize a Geo map with an unique name of the map
# function : initGeoMap
# param : chart_name - string - name of the chart
chart_name = 'Chart1'
initGeoMap(chart_name)

# Define Animation control once at the beginning and add it into Geo map with chart name
# function : addAnimationToGeoChart
# param 1 : chart_name - string - name of the chart
# param 2 : year_from - int - start year of the animation (e.g. 1 Jan 2008)
# param 3 : year_to - int - end year of the animation (e.g. 31 Dec 2013)
# param 4 : animation_info - object(python Dictionary) - 
#             'title' -> Title of the animation panel
#             'position' -> Position of the animation panel (bottomright, bottomleft, topright, topleft)
animation_info = {
       'title': 'My Animation',
       'position': 'bottomright',
}
addAnimationToGeoChart(chart_name, 2009, 2013, animation_info)

# Define layer name and corresponding variable
layer_name = 'Scalar SWE'
layer_name_1 = 'Scalar Canopy Wat'
variable_name = 'scalarSWE'

# Define Color List for a specific layer of the Geo map with chart name
# function : addColorListToGeoChart
# param 1 : chart_name - string - name of the chart
# param 2 : layer_name - string - name of the layer
# param 3 : color_list - array of string - list of all colors
color_list = ['#ffffe5', '#f7fcb9', '#d9f0a3', '#addd8e', '#93D284', '#78c679', '#41ab5d', '#238443', '#006837', '#004529']
addColorListToGeoChart(chart_name, layer_name, color_list)


# Define Legend Info for a specific layer of the Geo map with chart name
# function : addLegendToGeoChart
# param 1 : chart_name - string - name of the chart
# param 2 : layer_name - string - name of the layer
# param 3 : legend_info - object(python Dictionary) - 
#             'legend_title' -> Title of the legend
#             'legend_position' -> Position of the legend (bottomright, bottomleft, topright, topleft)
#             'scale'(optional) -> Scales of the legend (default - linear)
#             'grade_list'(optional) - array of number - defined the grades of the scale specifically

legend_info = {
'legend_title': 'Scalar SWE (kg m-2)', 
'legend_position': 'bottomleft',
'scale': 'logarithmic'
}
addLegendToGeoChart(chart_name, layer_name, legend_info)

# Define Legend Info for a specific layer of the Geo map with chart name
# function : addLegendToGeoChart
# param 1 : chart_name - string - name of the chart
# param 2 : layer_name - string - name of the layer
# param 3 : sidebar_option - object(python Dictionary) - 
#             'tab_no (optional)' -> Number - The numeric number of the tab in sidebar, we can put multiple chart in the same tab using this. Default is 0.
#             'chart_title (optional)' -> String - Title of the chart
#             'chart_type -> String - The type of chart like heatmap or linechart
#             'layer_name' -> String - Name of the layer
#             'title (optional)' -> String - Title of the tab of the sidebar
#             'aggregation_type' - string - Type of the aggreagation (e.g. average, sum) 
#             'start_month' - string - Name of the month
#             'start_year' - Number - The start of the year 
#             'end_year' - Number - The end of the year
sidebar1_section1_heatmap = {'section_id': 0, 'chart_title': 'Monthly Average of Scalar SWE', 'chart_type': 'Heatmap', 'layer_name': layer_name, 'title': 'Scalar SWE vs Scalar Canopy WAT', 'aggreagation_type' : 'average', 'start_month': 'Nov', 'start_year': 2008, 'end_year': 2013}; 
sidebar1_section2_line_0 = {'chart_title': 'Monthly Average of Scalar Canopy WAT', 'chart_type': 'Heatmap', 'layer_name': layer_name_1, 'title': 'Scalar SWE vs Scalar Canopy WAT', 'aggreagation_type' : 'average', 'start_month': 'Nov', 'start_year': 2008, 'end_year': 2013};
sidebar1_section3_line_1 = {'section_id': 1, 'chart_title': 'Monthly Average of Scalar SWE', 'chart_type': 'LineChart', 'layer_name': layer_name, 'title': 'Average of Scalar SWE', 'aggreagation_type' : 'average'}; 
addSidebarOptionToGeoChart(chart_name, layer_name, sidebar1_section1_heatmap)
addSidebarOptionToGeoChart(chart_name, layer_name, sidebar1_section2_line_0)
addSidebarOptionToGeoChart(chart_name, layer_name, sidebar1_section3_line_1)

# Draw the chart 
# param 1 : chart_name - string - name of the chart
# param 2 : layer_name - string - name of the layer
# param 3 : json_filename - string - path of geo json
# parma 4 : variable_name - string - name of the variable
# parma 5 : connecting_id - string - name of the connecting id in geo json (e.g. HRU_ID, COMID)
# parma 6 : aggregation_type - string - Type of the aggreagation (e.g. average, sum) 
drawGeoChart(chart_name, layer_name, 'jeoJSONs/bow_river_catchment.json', variable_name, 'HRU_ID', 'average')


variable_name = 'scalarCanopyWat'

# Define Color List for a specific layer of the Geo map with chart name
# function : addColorListToGeoChart
# param 1 : chart_name - string - name of the chart
# param 2 : layer_name - string - name of the layer
# param 3 : color_list - array of string - list of all colors
color_list = ['#ffffd9', '#edf8b1', '#c7e9b4', '#7fcdbb', '#60C2C0', '#41b6c4', '#1d91c0', '#225ea8', '#253494', '#081d58']
addColorListToGeoChart(chart_name, layer_name_1, color_list)


# Define Legend Info for a specific layer of the Geo map with chart name
# function : addLegendToGeoChart
# param 1 : chart_name - string - name of the chart
# param 2 : layer_name - string - name of the layer
# param 3 : legend_info - object(python Dictionary) - 
#             'legend_title' -> Title of the legend
#             'legend_position' -> Position of the legend (bottomright, bottomleft, topright, topleft)
#             'scale'(optional) -> Scales of the legend (default - linear)
#             'grade_list'(optional) - array of number - defined the grades of the scale specifically

legend_info = {
'legend_title': 'Scalar Canopy Wat (kg m-2)', 
'legend_position': 'bottomleft',
'scale': 'logarithmic'
}
addLegendToGeoChart(chart_name, layer_name_1, legend_info)

# Define Legend Info for a specific layer of the Geo map with chart name
# function : addLegendToGeoChart
# param 1 : chart_name - string - name of the chart
# param 2 : layer_name - string - name of the layer
# param 3 : sidebar_option - object(python Dictionary) - 
#             'tab_no (optional)' -> Number - The numeric number of the tab in sidebar, we can put multiple chart in the same tab using this. Default is 0.
#             'chart_title (optional)' -> String - Title of the chart
#             'chart_type -> String - The type of chart like heatmap or linechart
#             'layer_name' -> String - Name of the layer
#             'title (optional)' -> String - Title of the tab of the sidebar
#             'aggregation_type' - string - Type of the aggreagation (e.g. average, sum) 
#             'start_month' - string - Name of the month
#             'start_year' - Number - The start of the year 
#             'end_year' - Number - The end of the year
sidebar2_section1_heatmap = {'section_id': 0, 'chart_title': 'Monthly Average of Scalar SWE', 'chart_type': 'Heatmap', 'layer_name': layer_name, 'title': 'Scalar SWE vs Scalar Canopy WAT', 'aggreagation_type' : 'average', 'start_month': 'Nov', 'start_year': 2008, 'end_year': 2013}; 
sidebar2_section2_line_0 = {'chart_title': 'Monthly Average of Scalar Canopy WAT', 'chart_type': 'Heatmap', 'layer_name': layer_name_1, 'title': 'Scalar SWE vs Scalar Canopy WAT', 'aggreagation_type' : 'average', 'start_month': 'Nov', 'start_year': 2008, 'end_year': 2013};
sidebar2_section3_line_1 = {'section_id': 1, 'chart_title': 'Monthly Average of Scalar SWE', 'chart_type': 'LineChart', 'layer_name': layer_name, 'title': 'Average of Scalar SWE', 'aggreagation_type' : 'average'}; 
addSidebarOptionToGeoChart(chart_name, layer_name_1, sidebar2_section1_heatmap)
addSidebarOptionToGeoChart(chart_name, layer_name_1, sidebar2_section2_line_0)
addSidebarOptionToGeoChart(chart_name, layer_name_1, sidebar2_section3_line_1)

# Draw the chart 
# param 1 : chart_name - string - name of the chart
# param 2 : layer_name - string - name of the layer
# param 3 : json_filename - string - path of geo json
# parma 4 : variable_name - string - name of the variable
# parma 5 : connecting_id - string - name of the connecting id in geo json (e.g. HRU_ID, COMID)
# parma 6 : aggregation_type - string - Type of the aggreagation (e.g. average, sum) 
drawGeoChart(chart_name, layer_name_1, 'jeoJSONs/bow_river_catchment.json', variable_name, 'HRU_ID', 'average')



# Define layer name and corresponding variable
layer_name = 'Average KWTroutedRunoff'
variable_name = 'KWTroutedRunoff'

# Define Color List for a specific layer of the Geo map with chart name
# function : addColorListToGeoChart
# param 1 : chart_name - string - name of the chart
# param 2 : layer_name - string - name of the layer
# param 3 : color_list - array of string - list of all colors
color_list = ['#ffffcc', '#ffeda0', '#fed976', '#feb24c', '#fd8d3c', '#fc5735', '#ed4624', '#e31a1c', '#bd0026', '#800026']
addColorListToGeoChart(chart_name, layer_name, color_list)

# Define Legend Info for a specific layer of the Geo map with chart name
# function : addLegendToGeoChart
# param 1 : chart_name - string - name of the chart
# param 2 : layer_name - string - name of the layer
# param 3 : legend_info - object(python Dictionary) - 
#             'legend_title' -> Title of the legend
#             'legend_position' -> Position of the legend (bottomright, bottomleft, topright, topleft)
#             'scale'(optional) -> Scales of the legend (default - linear)
#             'grade_list'(optional) - array of number - defined the grades of the scale specifically
legend_info = {
'legend_title': 'Average KWTroutedRunoff (m3/s)', 
'legend_position': 'bottomleft',
'grade_list': [5, 10, 20, 40, 60, 90, 120, 150, 200]
}
addLegendToGeoChart(chart_name, layer_name, legend_info)

# Define Legend Info for a specific layer of the Geo map with chart name
# function : addLegendToGeoChart
# param 1 : chart_name - string - name of the chart
# param 2 : layer_name - string - name of the layer
# param 3 : sidebar_option - object(python Dictionary) - 
#             'section_id (optional)' -> Number - The numeric number of the tab in sidebar, we can put multiple chart in the same tab using this. Default is 0.
#             'chart_title (optional)' -> String - Title of the chart
#             'chart_type -> String - The type of chart like heatmap or linechart
#             'layer_name' -> String - Name of the layer
#             'title (optional)' -> String - Title of the tab of the sidebar
#             'aggregation_type' - string - Type of the aggreagation (e.g. average, sum) 
#             'start_month' - string - Name of the month
#             'start_year' - Number - The start of the year 
#             'end_year' - Number - The end of the year

sidebar3_section1_heatmap = {'section_id': 0, 'chart_title': 'Monthly Average of KWTroutedRunoff', 'chart_type': 'Heatmap', 'layer_name': layer_name, 'title': 'Monthly Average of KWTroutedRunoff in Heatmap', 'aggreagation_type' : 'average', 'start_month': 'Nov', 'start_year': 2009, 'end_year': 2013}; 
sidebar3_section2_line_1 = {'section_id': 1, 'chart_title': 'Monthly Average of KWTroutedRunoff', 'chart_type': 'LineChart', 'layer_name': layer_name, 'title': 'Monthly Average of KWTroutedRunoff in LineChart', 'aggreagation_type' : 'average'}; 
addSidebarOptionToGeoChart(chart_name, layer_name, sidebar3_section1_heatmap)
addSidebarOptionToGeoChart(chart_name, layer_name, sidebar3_section2_line_1)


# Draw the chart 
# param 1 : chart_name - string - name of the chart
# param 2 : layer_name - string - name of the layer
# param 3 : json_filename - string - path of geo json
# parma 4 : variable_name - string - name of the variable
# parma 5 : connecting_id - string - name of the connecting id in geo json (e.g. HRU_ID, COMID)
# parma 6 : aggregation_type - string - Type of the aggreagation (e.g. average, sum) 
drawGeoChart(chart_name, layer_name, 'jeoJSONs/bow_river_network.json', variable_name, 'COMID', 'average')
result_array = sorted(result_array, key=lambda x: x['order'], reverse=False)
print(';##;')
print(result_array)