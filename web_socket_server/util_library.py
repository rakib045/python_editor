import os, time, shapefile
from web_socket_server import SERVER, web_port
from json import dumps
import netCDF4 as nc
import numpy as np

result_array = []
path_url = "http://localhost:8000/"

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

def initGeoMap(chart_name):
    global result_array
    data_array = {}
    data_array["id"] = chart_name.replace(' ','')
    data_array["to"] = "master," + chart_name.replace(' ','')
    data_array['name'] = chart_name
    data_array['type'] = 'new_tab'
    data_array["order"] = 1
    path = path_url + "geo_map.html?"

    if chart_name != '':
        path += "name=" + chart_name.replace(' ','') + "&"

    data_array['path'] = path.replace(',', '%2C')
    result_array.append(data_array)
    #print(result_array)
    return

def drawGeoChart(chart_name, layer_name, json_filename, variable_name, connecting_id='id', aggregation_type='average'):
    global result_array
    data_array = {}
    data_array["to"] = chart_name.replace(' ','')
    data_array["draw"] = 1
    data_array["order"] = 1000
    data_array["layer_name"] = layer_name
    data_array["json_filename"] = json_filename
    data_array["variable_name"] = variable_name
    data_array["connecting_id"] = connecting_id
    data_array["aggregation_type"] = aggregation_type

    result_array.append(data_array)
    return

def redrawGeoChart(chart_name):
    global result_array
    data_array = {}
    data_array["to"] = chart_name.replace(' ','')
    data_array["redraw"] = 1
    data_array["order"] = 1000
    result_array.append(data_array)
    return

def addColorListToGeoChart(chart_name, layer_name, color_list):
    global result_array
    data_array = {}
    data_array["to"] = chart_name.replace(' ','')
    data_array["order"] = 1000
    data_array["layer_name"] = layer_name
    data_array["color_list"] = color_list
    result_array.append(data_array)
    return

def addLegendToGeoChart(chart_name, layer_name, legend_info):
    global result_array
    data_array = {}
    data_array["to"] = chart_name.replace(' ','')
    data_array["order"] = 1000
    data_array["layer_name"] = layer_name
    data_array["legend_info"] = legend_info
    result_array.append(data_array)
    return

def addAnimationToGeoChart(chart_name, year_from, year_to, animation_info):
    global result_array
    data_array = {}
    data_array["to"] = chart_name.replace(' ','')
    data_array["order"] = 1000
    data_array["animation"] = 1
    data_array["animation_info"] = animation_info
    data_array["year_from"] = year_from
    data_array["year_to"] = year_to
    result_array.append(data_array)
    return


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

def generateGeoJSON_FromSHPAndNetCDF_WithinTimeRange_FileDist(shp_file_name, bbox, nc_filename, var_name, from_year, to_year, output_filename, isGenerateOnlyJSON=False):    

    start = time.time()

    reader = shapefile.Reader(shp_file_name)

    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    buffer = []
    
    count=0

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


        seg_id = sr.record['seg_id']
        flow_acc = sr.record['flow_acc']
        islake = sr.record['islake']
        if flow_acc < 0 or islake == 1:
            continue

        if not isGenerateOnlyJSON:

            days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]                        

            temp_json = {}
            temp_json_mon = {}

            for year in range(from_year, to_year+1):
                nc_file = nc_filename.replace("****", str(year))
                ds = nc.Dataset(nc_file)
                index = np.where(ds['reachID'][:] == seg_id)[0][0]
                val_per_day = np.array(ds['IRFroutedRunoff'][:,index]).tolist()
                temp_json[year] = np.around(val_per_day, 3).tolist()

                temp_mon_array = {}

                mon_index = 0
                day_index = 0
                for day_mon in days_in_month:                
                    temp_array = {}
                    val_mon = np.around(val_per_day[day_index:(day_index + day_mon)], 3).tolist()
                    day_index += day_mon
                    temp_array['total'] = round(sum(val_mon), 3)
                    temp_array['average'] = round(sum(val_mon)/len(val_mon), 3)
                    temp_array['value'] = val_mon
                    temp_mon_array[mon_index] = temp_array
                    mon_index += 1

                temp_json_mon[year] = temp_mon_array


            #field_names.append(var_name)
            # Writing Variable Files
            file_path_name = "Data\\" + var_name + "\\Daily\\" +str(seg_id) + ".json"
            var_file = open(file_path_name, "w") 
            var_file.write(dumps({'segment_id': seg_id, 'data': temp_json}, indent=2))
            var_file.close()

            file_path_name_mon = "Data\\" + var_name + "\\Monthly\\" +str(seg_id) + ".json"
            var_file_mon = open(file_path_name_mon, "w") 
            #sr.record.append(temp_json)        
            var_file_mon.write(dumps({'segment_id': seg_id, 'data': temp_json_mon}, indent=2))
            var_file_mon.close()


            # Writing Metadata Info
            file_path_name = "Data\\MetaData\\" +str(seg_id) + ".json"
            var_file = open(file_path_name, "w")
            atr = dict(zip(field_names, sr.record))
            var_file.write(dumps({'data': atr}, indent=2))
            var_file.close()
        

        #atr = dict(zip(field_names, sr.record))
        atr = {'seg_id':seg_id}


        geom = sr.shape.__geo_interface__
        buffer.append(dict(type="Feature", geometry=geom, properties=atr))         
        count += 1
    
        # write the GeoJSON file
    
    geojson = open(output_filename, "w")
    geojson.write(dumps({"type": "FeatureCollection", "features": buffer}, indent=2) + "\n")
    geojson.close()
    print("Total Shape Count: " + str(count))
    end = time.time()
    print(f"Processing time of the conversion is {end - start} second")
    print("GeoJSON generation completed !")

def generateGeoJSONLake_FromSHPAndNetCDF_WithinTimeRange_FileDist(lake_shp_file_name, river_shp_file_name, bbox, nc_filename, var_name, from_year, to_year, output_filename, isGenerateOnlyJSON=False):    

    start = time.time()

    reader = shapefile.Reader(lake_shp_file_name, encoding='cp1252')
    reader_river = shapefile.Reader(river_shp_file_name)

    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    buffer = []
    
    count=0

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


        lake_id = sr.record['Hylak_id']
        s_id = -1

        for item in reader_river.shapeRecords():
            if item.record['lakeId'] == lake_id :
                s_id = item.record['seg_id']
                break        

        if s_id == -1:
            continue
        
        if not isGenerateOnlyJSON:

            days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]                        

            temp_json = {}
            temp_json_mon = {}

            for year in range(from_year, to_year+1):
                nc_file = nc_filename.replace("****", str(year))
                ds = nc.Dataset(nc_file)
                index = np.where(ds['reachID'][:] == s_id)[0][0]
                val_per_day = np.array(ds['IRFlakeVol'][:,index]).tolist()
                temp_json[year] = np.around(val_per_day, 3).tolist()

                temp_mon_array = {}

                mon_index = 0
                day_index = 0
                for day_mon in days_in_month:                
                    temp_array = {}
                    val_mon = np.around(val_per_day[day_index:(day_index + day_mon)], 3).tolist()
                    day_index += day_mon
                    temp_array['total'] = round(sum(val_mon), 3)
                    temp_array['average'] = round(sum(val_mon)/len(val_mon), 3)
                    temp_array['value'] = val_mon
                    temp_mon_array[mon_index] = temp_array
                    mon_index += 1

                temp_json_mon[year] = temp_mon_array


            #field_names.append(var_name)
            # Writing Variable Files
            file_path_name = "Data\\" + var_name + "\\Daily\\" +str(s_id) + ".json"
            var_file = open(file_path_name, "w") 
            var_file.write(dumps({'segment_id': s_id, 'data': temp_json}, indent=2))
            var_file.close()

            file_path_name_mon = "Data\\" + var_name + "\\Monthly\\" +str(s_id) + ".json"
            var_file_mon = open(file_path_name_mon, "w") 
            #sr.record.append(temp_json)        
            var_file_mon.write(dumps({'segment_id': s_id, 'data': temp_json_mon}, indent=2))
            var_file_mon.close()


            # Writing Metadata Info
            file_path_name = "Data\\MetaData_Lake\\" +str(s_id) + ".json"
            var_file = open(file_path_name, "w")
            atr = dict(zip(field_names, sr.record))
            var_file.write(dumps({'data': atr}, indent=2))
            var_file.close()
        

        #atr = dict(zip(field_names, sr.record))
        atr = {'seg_id':s_id}


        geom = sr.shape.__geo_interface__
        buffer.append(dict(type="Feature", geometry=geom, properties=atr))         
        count += 1
        print(str(count) + ", ")
    
        # write the GeoJSON file
    
    geojson = open(output_filename, "w")
    geojson.write(dumps({"type": "FeatureCollection", "features": buffer}, indent=2) + "\n")
    geojson.close()
    print("\nTotal Shape Count: " + str(count))
    end = time.time()
    print(f"Processing time of the conversion is {end - start} second")
    print("GeoJSON generation completed !")