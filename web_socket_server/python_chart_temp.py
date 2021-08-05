from util_library import *
initGeoMap('Chart1')


animation_info = {
       'title': 'My Animation',
       'position': 'bottomright',
}
addAnimationToGeoChart('Chart1', 2008, 2013, animation_info)

layer_name = 'Scalar SWE'
variable_name = 'scalarSWE'
color_list = ['#ffffe5', '#f7fcb9', '#d9f0a3', '#addd8e', '#82d183', '#78c679', '#41ab5d', '#238443', '#006837', '#004529']
addColorListToGeoChart('Chart1', layer_name, color_list)

legend_info = {
'legend_title': 'Scalar SWE (kg m-2)', 
'legend_position': 'bottomleft',
'scale': 'logarithmic'
}
addLegendToGeoChart('Chart1', layer_name, legend_info)
addOptionButtonToGeoChart('Chart1', layer_name, 'Show Average HeatMap', 'Heatmap', 'average')
addOptionButtonToGeoChart('Chart1', layer_name, 'Show Average Line Chart', 'LineChart', 'average')
drawGeoChart('Chart1', layer_name, 'jeoJSONs/bow_river_catchment.json', variable_name, 'HRU_ID', 'average')
result_array = sorted(result_array, key=lambda x: x['order'], reverse=False)
print(';##;')
print(result_array)