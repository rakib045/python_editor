from util_library import *
# Add your generated charts here           

shp_filename = "RData\\river_with_lake_flag4_reorder.shp"
nc_filename = "D:\OneDrive_USask\OneDrive - University of Saskatchewan\PravinShervan\hybrid_test.mizuRoute.h.****-01-01-00000.nc"
var_name = 'IRFroutedRunoff'

bbox_saskatoon = {
       'min_longitude': -107.74566,
       'max_longitude': -105.65277, 
       'min_latitude': 51.544626, 
       'max_latitude':  52.72631
}
output_filename = "jeoJSON_saskatoon_1995_1996.json"

generateGeoJSON_FromSHPAndNetCDF_WithinTimeRange(shp_filename, bbox_saskatoon, nc_filename, var_name, 1995, 1996, output_filename)   

