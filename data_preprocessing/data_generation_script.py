from util_library import *

nc_filename = "D:\OneDrive_USask\OneDrive - University of Saskatchewan\PravinShervan\hybrid_test.mizuRoute.h.****-01-01-00000.nc"

#utf-8 encoding is for river with lake and cp1252 encoding is for hydro lake
#var_name = 'IRFroutedRunoff'
shp_filename = "RData\\river_with_lake_flag4_reorder.shp"
#encoding_name = 'utf-8' 

shp_lake_filename = "RData\\hydrolake_sub100km.shp"
var_name = 'IRFlakeVol'
encoding_name = 'cp1252'

bbox_saskatoon = {
       'min_longitude': -140.18555, 
       'max_longitude': -102.48047, 
       'min_latitude': 51.344339, 
       'max_latitude': 69.687618
}
output_filename = "jeoJSON_west_all_lake.json"

#generateGeoJSON_FromSHPAndNetCDF_WithinTimeRange_FileDist(shp_filename, bbox_saskatoon, nc_filename, var_name, 1995, 2005, output_filename, True)

#generateGeoJSON_FromSHPAndNetCDF_WithinTimeRange_FileDist(shp_filename, bbox_saskatoon, nc_filename, var_name, 1995, 1996, output_filename, False)


generateGeoJSONLake_FromSHPAndNetCDF_WithinTimeRange_FileDist(shp_lake_filename, shp_filename, bbox_saskatoon, nc_filename, var_name, 1995, 2005, output_filename, False)