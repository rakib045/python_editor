from util_library import *

nc_filename = "D:\OneDrive_USask\OneDrive - University of Saskatchewan\PravinShervan\hybrid_test.mizuRoute.h.****-01-01-00000.nc"

#utf-8 encoding is for river with lake and cp1252 encoding is for hydro lake
var_name = 'IRFroutedRunoff'
shp_filename = "data_preprocessing\\RData\\river_with_lake_flag4_reorder.shp"
#encoding_name = 'utf-8' 

shp_lake_filename = "data_preprocessing\\RData\\hydrolake_sub100km.shp"
var_name_lake = 'IRFlakeVol'
#encoding_name = 'cp1252'

bbox_al_sk = {
       'min_longitude': -119.70703, 
       'max_longitude': -101.77735, 
       'min_latitude': 48.98022, 
       'max_latitude':  59.91098
}
output_filename_river = "vis\\jeoJSON_al_sk_river_flow_acc_gt_1500.json"
output_filename_lake = "vis\\jeoJSON_al_sk_lake.json"

generateGeoJSON_FromSHPAndNetCDF_WithinTimeRange_FileDist(shp_filename, bbox_al_sk, nc_filename, var_name, 1995, 2005, output_filename_river, False)

generateGeoJSONLake_FromSHPAndNetCDF_WithinTimeRange_FileDist(shp_lake_filename, shp_filename, bbox_al_sk, nc_filename, var_name_lake, 1995, 2005, output_filename_lake, False)