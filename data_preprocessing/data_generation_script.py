from util_data_preprocess_library import *

shp_file_path = "D:\\GWF Data\\shapefiles\\river_network\\bow_river_network_from_merit_hydro.shp"
input = {
       'shp_file_path': 'D:\\GWF Data\\shapefiles\\river_network\\bow_river_network_from_merit_hydro.shp',
       'id_param_name': 'COMID'
}

bbox_al_sk = {
       'apply_bounding_box': False,
       'min_longitude': -119.70703, 
       'max_longitude': -101.77735, 
       'min_latitude': 48.98022, 
       'max_latitude':  59.91098
}
filters = {
       'param_name': 'COMID',
       'expression': '>-1'
}
metadata = {
       'is_generate': True,
       'filename_init': 'id_',
       'folder_path': ''
}

'''
generateGeoJSON(     
       input= input,
       output_file_path= "data_preprocessing\\bow_river_network.json",
       bounding_box= bbox_al_sk,
       filters= filters,
       metadata=metadata)
'''
ids = getIDsFromGeoJSONProperties("data_preprocessing\\bow_river_network.json", "id")

time_diff_array = []
time_step = 3600
item_count = 0
for year in range(2008, 2014):
       time_diff_array.append(getSecondDiffArray(initial_date_str="1990-01-01", start_date_str=str(year)+"-01-01", end_date_str=str(year+1)+"-01-01", steps=time_step))
       item_count += 1
#print(time_diff_array)

filename_path = "D:\\GWF Data\\data\\mizuRoute\\run1.h.****-01-01-00000.nc"
#variable_name = 'IRFroutedRunoff'
#variable_name = 'KWTroutedRunoff'
#variable_name = 'sumUpstreamRunoff'
variable_name = 'dlayRunoff'
id_param_name = 'COMID'
column_info = {
       'column_ids' : ids,
       'column_name' : 'reachID'
}

row_info = {
       'row_ids' : time_diff_array,
       'row_name' : 'time',
       'iteration_item_count' : item_count
}

generateJSONFromNetCDFYearSeparatedFileHourly(filename=filename_path, year_range=[2008, 2013], variable_name=variable_name, column_info=column_info, row_info=row_info, id_param_name=id_param_name)
generateJSONFromNetCDFYearSeparatedFileDaily(filename=filename_path, year_range=[2008, 2013], variable_name=variable_name, column_info=column_info, row_info=row_info, id_param_name=id_param_name)
generateJSONFromNetCDFYearSeparatedFileMonthly(filename=filename_path, year_range=[2008, 2013], variable_name=variable_name, column_info=column_info, row_info=row_info, id_param_name=id_param_name)

'''
nc_filename = "D:\OneDrive_USask\OneDrive - University of Saskatchewan\PravinShervan\hybrid_test.mizuRoute.h.****-01-01-00000.nc"

#utf-8 encoding is for river with lake and cp1252 encoding is for hydro lake
var_name = 'IRFroutedRunoff'
shp_filename = "data_preprocessing\\RData\\river_with_lake_flag4_reorder.shp"
#encoding_name = 'utf-8' 

shp_lake_filename = "data_preprocessing\\RData\\hydrolake_sub100km.shp"
var_name_lake = 'IRFlakeVol'
#encoding_name = 'cp1252'

bbox_al_sk = {
       'apply_bounding_box': True,
       'min_longitude': -119.70703, 
       'max_longitude': -101.77735, 
       'min_latitude': 48.98022, 
       'max_latitude':  59.91098
}
output_filename_river = "vis\\jeoJSON_al_sk_river_flow_acc_gt_1500.json"
output_filename_lake = "vis\\jeoJSON_al_sk_lake.json"

generateGeoJSON_FromSHPAndNetCDF_WithinTimeRange_FileDist(shp_filename, bbox_al_sk, nc_filename, var_name, 1995, 2005, output_filename_river, False)

generateGeoJSONLake_FromSHPAndNetCDF_WithinTimeRange_FileDist(shp_lake_filename, shp_filename, bbox_al_sk, nc_filename, var_name_lake, 1995, 2005, output_filename_lake, False)

'''