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
       'filename_init': 'COMID_',
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

#generateJSONFromNetCDFYearSeparatedFileHourly(filename=filename_path, year_range=[2008, 2013], variable_name=variable_name, column_info=column_info, row_info=row_info, id_param_name=id_param_name)
#generateJSONFromNetCDFYearSeparatedFileDaily(filename=filename_path, year_range=[2008, 2013], variable_name=variable_name, column_info=column_info, row_info=row_info, id_param_name=id_param_name)
#generateJSONFromNetCDFYearSeparatedFileMonthly(filename=filename_path, year_range=[2008, 2013], variable_name=variable_name, column_info=column_info, row_info=row_info, id_param_name=id_param_name)


input = {
       'shp_file_path': 'D:\\GWF Data\\shapefiles\\catchment\\bow_distributed_elevation_zone.shp',
       'id_param_name': 'HRU_ID'
}

bbox_al_sk = {
       'apply_bounding_box': False,
       'min_longitude': -119.70703, 
       'max_longitude': -101.77735, 
       'min_latitude': 48.98022, 
       'max_latitude':  59.91098
}

filters = {
       'param_name': 'HRU_ID',
       'expression': '>-1'
}

metadata = {
       'is_generate': True,
       'filename_init': 'HRU_ID_',
       'folder_path': ''
}
'''
generateGeoJSON(     
       input= input,
       output_file_path= "data_preprocessing\\bow_river_catchment.json",
       bounding_box= bbox_al_sk,
       filters= filters,
       metadata=metadata)
'''

ids = getIDsFromGeoJSONProperties("data_preprocessing\\bow_river_catchment.json", "id")

filename_path = "D:\\GWF Data\\simulations\\run1\\SUMMA\\run1_day.nc"

#variable_name = 'scalarSWE'
#variable_name = 'scalarAquiferBaseflow'
#variable_name = 'scalarAquiferStorage'
#variable_name = 'scalarCanopyWat'
#variable_name = 'scalarInfiltration'

#variable_name = 'scalarLatHeatTotal'
#variable_name = 'scalarNetRadiation'
#variable_name = 'scalarRainPlusMelt'
#variable_name = 'scalarSenHeatTotal'
#variable_name = 'scalarSoilBaseflow'

#variable_name = 'scalarSoilDrainage'
#variable_name = 'scalarSurfaceRunoff'
#variable_name = 'scalarTotalET'
#variable_name = 'scalarTotalRunoff'
variable_name = 'scalarTotalSoilWat'

id_param_name = 'HRU_ID'
column_info = {
       'column_ids' : ids,
       'column_name' : 'hruId'
}

time_diff_array = []
time_step = 3600 * 24
for year in range(2008, 2014):
       time_diff_array.extend(getSecondDiffArray(initial_date_str="1990-01-01", start_date_str=str(year)+"-01-01", end_date_str=str(year+1)+"-01-01", steps=time_step))
       item_count += 1

row_info = {
       'row_ids' : time_diff_array,
       'row_name' : 'time',
       'iteration_item_count' : item_count
}

generateJSONFromNetCDFDaily(filename=filename_path, year_range=[2008, 2013], variable_name=variable_name, column_info=column_info, row_info=row_info, id_param_name=id_param_name)
generateJSONFromNetCDFMonthly(filename=filename_path, year_range=[2008, 2013], variable_name=variable_name, column_info=column_info, row_info=row_info, id_param_name=id_param_name)

