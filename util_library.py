import os, time, shapefile
from web_socket_server import SERVER, web_port
from json import dumps
import netCDF4 as nc
import numpy as np

result_array = []

def addToChart(chart_name, filename, order=100):
    global result_array
    if os.path.exists(filename):
        data_array = {}
        data_array["id"] = chart_name.replace(' ','')
        data_array["to"] = "master," + chart_name.replace(' ','')
        data_array["name"] = chart_name
        data_array["path"] = filename
        data_array["type"] = 'image'
        data_array["order"] = order
        result_array.append(data_array)
    #print(result_array)
    return

def addRiverMapToChart(chart_name, order=100, jsonfilename='', color_list=''):
    global result_array
    data_array = {}
    data_array["id"] = chart_name.replace(' ','')
    data_array["to"] = "master," + chart_name.replace(' ','')
    data_array['name'] = chart_name
    data_array['type'] = 'iframe'
    data_array["order"] = order
    path = 'http://' + SERVER + ":" + str(web_port) + "/river_map.html?"
    if chart_name != '':
        path += "name=" + chart_name.replace(' ','') + "&"

    if jsonfilename != '':
        path += "geojson=" + filenames_str[:-1] + "&"
    
    if color_list != '':
        color_list_array = color_list.replace(' ','').replace('#','%23')
        path += "colorlist=" + color_list_array + "&"
    data_array['path'] = path.replace(',', '%2C')
    result_array.append(data_array)
    #print(result_array)
    return

def addJSONRiverMap(chart_name, jsonfilenames):
    global result_array
    data_array = {}
    data_array["to"] = chart_name.replace(' ','')
    data_array["order"] = 1000

    filenames_str = ''
    for filename in jsonfilenames:
        if os.path.exists(filename):
            filenames_str += filename + ","
    if filenames_str != '':
        data_array["geojson"] = filenames_str[:-1]
    result_array.append(data_array)
    return

def addColorListRiverMap(chart_name, color_list):
    global result_array
    data_array = {}
    data_array["to"] = chart_name.replace(' ','')
    data_array["order"] = 1000

    color_str = ''
    for color in color_list:
        color_str += color + ","
    if color_str != '':
        data_array["colorlist"] = color_str[:-1]
    result_array.append(data_array)
    return

def drawChart(chart_name):
    global result_array
    data_array = {}
    data_array["to"] = chart_name.replace(' ','')
    data_array["draw"] = 1
    data_array["order"] = 1000
    result_array.append(data_array)
    return

'''
def addRiverMapToChart(chart_name, files, color_list='', order=100):
    global result_array
    filenames = files.replace(' ','').split(',')
    filenames_str = ''
    for filename in filenames:
        if os.path.exists(filename):
            filenames_str += filename + ","
    data_array = {}
    data_array["id"] = chart_name.strip()
    data_array['name'] = chart_name
    data_array['type'] = 'iframe'
    data_array["order"] = order
    path = 'http://' + SERVER + ":" + str(web_port) + "/river_map.html?"
    if chart_name != '':
        path += "name=" + chart_name.strip() + "&"

    if filenames_str != '':
        path += "geojson=" + filenames_str[:-1] + "&"
    
    if color_list != '':
        color_list_array = color_list.replace(' ','').replace('#','%23')
        path += "colorlist=" + color_list_array + "&"
    data_array['path'] = path.replace(',', '%2C')
    result_array.append(data_array)
    #print(result_array)
    return
'''

def generateGeoJSON(shp_file_name, bbox, output_filename):    

    start = time.time()

    reader = shapefile.Reader(shp_file_name)

    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    buffer = []
    
    index=0

    #xmin = bbox_lon_min  # Lon
    #xmax = bbox_lon_max
    #ymin = bbox_lat_min  #Lat
    #ymax = bbox_lat_max

    xmin = bbox['min_longitude']  # Lon
    xmax = bbox['max_longitude']
    ymin = bbox['min_latitude']  #Lat
    ymax = bbox['max_latitude']

    for sr in reader.shapeRecords():
        
        sxmin, symin, sxmax, symax = sr.shape.bbox
        
        if sxmin <  xmin: continue
        elif sxmax > xmax: continue
        elif symin < ymin: continue
        elif symax > ymax: continue

        atr = dict(zip(field_names, sr.record))
        geom = sr.shape.__geo_interface__
        buffer.append(dict(type="Feature", \
        geometry=geom, properties=atr)) 
        
        index += 1
    
        # write the GeoJSON file
    
    geojson = open(output_filename, "w")
    geojson.write(dumps({"type": "FeatureCollection", "features": buffer}, indent=2) + "\n")
    geojson.close()
    print("Total Shape Count: " + str(index))
    end = time.time()
    print(f"Processing time of the conversion is {end - start} second")
    print("GeoJSON generation completed !")


def generateGeoJSON_FromSHPAndNetCDF_WithinTimeRange(shp_file_name, bbox, nc_filename, var_name, from_year, to_year, output_filename):    

    start = time.time()

    reader = shapefile.Reader(shp_file_name)

    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    buffer = []
    
    index=0

    #xmin = bbox_lon_min  # Lon
    #xmax = bbox_lon_max
    #ymin = bbox_lat_min  #Lat
    #ymax = bbox_lat_max

    xmin = bbox['min_longitude']  # Lon
    xmax = bbox['max_longitude']
    ymin = bbox['min_latitude']  #Lat
    ymax = bbox['max_latitude']

    for sr in reader.shapeRecords():
        
        sxmin, symin, sxmax, symax = sr.shape.bbox
        
        if sxmin <  xmin: continue
        elif sxmax > xmax: continue
        elif symin < ymin: continue
        elif symax > ymax: continue

        field_names.append(var_name)
        seg_id = sr.record['seg_id']
        temp_json = {}
        for year in range(from_year, to_year+1):
            nc_file = nc_filename.replace("****", str(year))
            ds = nc.Dataset(nc_file)
            index = np.where(ds['reachID'][:] == seg_id)[0][0]
            temp_json[year] = np.array(ds['IRFroutedRunoff'][:,index]).tolist()

        sr.record.append(temp_json)

        atr = dict(zip(field_names, sr.record))
        geom = sr.shape.__geo_interface__
        buffer.append(dict(type="Feature", \
        geometry=geom, properties=atr)) 
        
        index += 1
    
        # write the GeoJSON file
    
    geojson = open(output_filename, "w")
    geojson.write(dumps({"type": "FeatureCollection", "features": buffer}, indent=2) + "\n")
    geojson.close()
    print("Total Shape Count: " + str(index))
    end = time.time()
    print(f"Processing time of the conversion is {end - start} second")
    print("GeoJSON generation completed !")