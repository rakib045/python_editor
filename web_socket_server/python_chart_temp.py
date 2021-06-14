from util_library import *
animation_info = {
       'title': 'My Animation',
       'position': 'bottomright',
}
addAnimationToGeoChart('Chart1', 2009, 2013, animation_info)

layer_name = 'River IRFroutedRunoff Average'
variable_name = 'IRFroutedRunoff'
color_list = ['#ffffe5', '#f7fcb9', '#d9f0a3', '#addd8e', '#82d183', '#78c679', '#41ab5d', '#238443', '#006837', '#004529']
addColorListToGeoChart('Chart1', layer_name, color_list)

legend_info = {
'legend_title': 'River IRFroutedRunoff Average (m3/s)', 
'legend_position': 'bottomleft',
'scale': 'logarithmic'
}
addLegendToGeoChart('Chart1', layer_name, legend_info)
drawGeoChart('Chart1', layer_name, 'jeoJSONs/bow_river_network.json', variable_name, 'COMID', 'average')




layer_name = 'River KWTroutedRunoff Average'
variable_name = 'KWTroutedRunoff'

color_list = ['#ffffcc', '#ffeda0', '#fed976', '#feb24c', '#fd8d3c', '#fc5735', '#ed4624', '#e31a1c', '#bd0026', '#800026']
addColorListToGeoChart('Chart1', layer_name, color_list)

legend_info = {
'legend_title': 'River KWTroutedRunoff (m3/s) Average', 
'legend_position': 'bottomleft',
'scale': 'logarithmic'
}

addLegendToGeoChart('Chart1', layer_name, legend_info)
drawGeoChart('Chart1', layer_name, 'jeoJSONs/bow_river_network.json', variable_name, 'COMID', 'average')





layer_name = 'River dlayRunoff Average'
variable_name = 'dlayRunoff'

color_list = ['red', 'blue', 'green']
addColorListToGeoChart('Chart1', layer_name, color_list)

legend_info = {
'legend_title': 'River dlayRunoff (m3/s) Total', 
'legend_position': 'bottomleft',
'grade_list': [5, 40]
}

addLegendToGeoChart('Chart1', layer_name, legend_info)
drawGeoChart('Chart1', layer_name, 'jeoJSONs/bow_river_network.json', variable_name, 'COMID', 'sum')
result_array = sorted(result_array, key=lambda x: x['order'], reverse=False)
print(';##;')
print(result_array)