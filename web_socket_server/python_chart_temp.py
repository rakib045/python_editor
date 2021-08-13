from util_library import *
# Initialize a Geo map with an unique name of the map
# function : initGeoMap
# param : chart_name - string - name of the chart
initGeoMap('Chart1')

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
addAnimationToGeoChart('Chart1', 2008, 2013, animation_info)

# Define layer name and corresponding variable
layer_name = 'Average KWTroutedRunoff'
variable_name = 'KWTroutedRunoff'

# Define Color List for a specific layer of the Geo map with chart name
# function : addColorListToGeoChart
# param 1 : chart_name - string - name of the chart
# param 2 : layer_name - string - name of the layer
# param 3 : color_list - array of string - list of all colors
color_list = ['#ffffcc', '#ffeda0', '#fed976', '#feb24c', '#fd8d3c', '#fc5735', '#ed4624', '#e31a1c', '#bd0026', '#800026']
addColorListToGeoChart('Chart1', layer_name, color_list)

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
addLegendToGeoChart('Chart1', layer_name, legend_info)

# Define Option Button for a specific layer of the Geo map with chart name (Right click of a shape and pop up options)
# function : addOptionButtonToGeoChart
# param 1 : chart_name - string - name of the chart
# param 2 : layer_name - string - name of the layer
# param 3 : button_display_text - string - Text of the button
# parma 4 : chart_type - string - Type of the chart (e.g. Heatmap, LineChart) 
# parma 4 : aggregation_type - string - Type of the aggreagation (e.g. average, sum) 
addOptionButtonToGeoChart('Chart1', layer_name, 'Show Average HeatMap', 'Heatmap', 'average')
addOptionButtonToGeoChart('Chart1', layer_name, 'Show Average Line Chart', 'LineChart', 'average')

# Draw the chart 
# param 1 : chart_name - string - name of the chart
# param 2 : layer_name - string - name of the layer
# param 3 : json_filename - string - path of geo json
# parma 4 : variable_name - string - name of the variable
# parma 5 : connecting_id - string - name of the connecting id in geo json (e.g. HRU_ID, COMID)
# parma 6 : aggregation_type - string - Type of the aggreagation (e.g. average, sum) 
drawGeoChart('Chart1', layer_name, 'jeoJSONs/bow_river_network.json', variable_name, 'COMID', 'average')
result_array = sorted(result_array, key=lambda x: x['order'], reverse=False)
print(';##;')
print(result_array)