import os, time, shapefile
from numpy.lib.function_base import average
#from json import dumps
import json
import netCDF4 as nc
import numpy as np
from datetime import datetime, timedelta


def generateGeoJSON(input, output_file_path, bounding_box, 
                    filters={'param_name': '', 'expression': ''}, 
                    metadata={'is_generate': False, 'id_param': ''}):

    #processing time calculation initialization
    process_time_start = time.time()

    #Reading Shape Files with field names and values
    reader = shapefile.Reader(input['shp_file_path'])
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]

    buffer = []

    # Configuring the bounding box
    xmin, xmax, ymin, ymax = 0, 0, 0, 0

    if bounding_box['apply_bounding_box']:
        xmin = bounding_box['min_longitude']  # Lon
        xmax = bounding_box['max_longitude']
        ymin = bounding_box['min_latitude']  #Lat
        ymax = bounding_box['max_latitude']

    shape_count = 0

    #Iterating all rows within shapefiles
    for sr in reader.shapeRecords():
        
        sxmin, symin, sxmax, symax = sr.shape.bbox
        
        if bounding_box['apply_bounding_box']:
            if sxmin <  xmin: continue
            elif sxmax > xmax: continue
            elif symin < ymin: continue
            elif symax > ymax: continue

        if filters['param_name'] != '':
            param_val = int(sr.record[filters['param_name']])
            if eval('param_val'+ filters['expression']) is False:
                continue

        custom_id = int(sr.record[input['id_param_name']])            
        
        if metadata['is_generate']:                            
            file_path_name = "data_preprocessing\\Data\\MetaData\\" + metadata['filename_init'] + str(custom_id) + ".json"
            metadata_file = open(file_path_name, "w")
            atr = dict(zip(field_names, sr.record))
            metadata_file.write(json.dumps({'data': atr}, indent=2))
            metadata_file.close()

        atr_buff = {'id': custom_id }
        geom = sr.shape.__geo_interface__
        buffer.append(dict(type="Feature", properties=atr_buff, geometry=geom))         
        
        shape_count += 1
    
        # write the GeoJSON file
    
    geojson = open(output_file_path, "w")
    geojson.write(json.dumps({ "id_param_name":input['id_param_name'], "type": "FeatureCollection", "features": buffer}, indent=2) + "\n")
    geojson.close()

    print("Total Shape Count: " + str(shape_count))
    process_time_end = time.time()
    print(f"Processing time of the conversion is {process_time_end - process_time_start} second")
    print("GeoJSON generation completed !")


    return 0


def getIDsFromGeoJSONProperties(file_name, param_name):
    value_array = []
    with open(file_name) as f:
        data = json.load(f)
        for item in data['features']:
            value_array.append(item['properties'][param_name])

    return value_array

def getSecondDiffArray(initial_date_str, start_date_str, end_date_str, steps):
    value_array = []

    init_date = datetime.strptime(initial_date_str, '%Y-%m-%d')
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    date = start_date
    while date < end_date:
        time_diff = (date - init_date)
        value_array.append(time_diff.total_seconds())
        date = date + timedelta(seconds=steps)

    return value_array

def generateDailyDataFromHourlyData(filename, variable_name, column_info, row_info, year_range):
    temp_json_hourly = {}
    print('Reading All NC Files - Started')

    loop_index = 0
    for year in range(year_range[0], year_range[1]+1):
        filename_str = filename.replace("****", str(year))
        
        ds = nc.Dataset(filename_str)

        column_ids_input = np.around(column_info['column_ids']).astype(int)
        column_ids_nc = np.around(ds[column_info['column_name']][:]).astype(int)
        column_indexes = np.where(np.in1d(column_ids_nc, column_ids_input))[0]
        
        row_ids_input = np.around(row_info['row_ids'][loop_index]).astype(int)
        row_ids_nc = np.around(ds[row_info['row_name']][:]).astype(int)
        row_indexes = np.where(np.in1d(row_ids_nc, row_ids_input))[0] 
        loop_index += 1     
        
        val_per_day = np.array(ds[variable_name][row_indexes,column_indexes]).tolist()
        temp_json_hourly[year] = np.around(val_per_day, 3)

    print('Reading All NC Files - Ended')
    return temp_json_hourly, column_indexes, row_indexes


def generateDailyDataFromDailyData(filename, variable_name, column_info, row_info, year_range):
    temp_json_hourly = {}
    print('Reading All NC Files - Started')

    ds = nc.Dataset(filename)

    column_ids_input = np.around(column_info['column_ids']).astype(int)
    column_ids_nc = np.around(ds[column_info['column_name']][:]).astype(int)
    column_indexes = np.where(np.in1d(column_ids_nc, column_ids_input))[0]
    
    row_ids_input = np.around(row_info['row_ids']).astype(int)
    row_ids_nc = np.around(ds[row_info['row_name']][:]).astype(int)
    row_indexes = np.where(np.in1d(row_ids_nc, row_ids_input))[0]

    val_per_day = np.array(ds[variable_name][row_indexes, column_indexes]).tolist()

    day_index = 0
    day_count = 365
    for year in range(year_range[0], year_range[1]+1):

        temp_json_hourly[year] = np.around(val_per_day[day_index:(day_index+day_count)], 3)
        day_index += day_count

    print('Reading All NC Files - Ended')
    return temp_json_hourly, column_indexes, row_indexes

def generateJSONFromNetCDFYearSeparatedFileHourly(filename, year_range, variable_name, column_info, row_info, id_param_name):    
       
    column_ids_input = np.around(column_info['column_ids']).astype(int)

    temp_json_hourly = {}
    temp_json_hourly_full_data, column_indexes, row_indexes = generateDailyDataFromHourlyData(filename, variable_name, column_info, row_info, year_range)

    print("Generating Hourly Data - Start")

    time_multiplier = 24
    for col_index in column_indexes.tolist():    
        for year in range(year_range[0], year_range[1]+1):
            temp_json_hourly[year] = np.around(temp_json_hourly_full_data[year][:,col_index], 3).tolist()

        file_path_name = "data_preprocessing\\Data\\" + variable_name + "\\Hourly\\id_" +str(column_ids_input[col_index]) + ".json"
        var_file = open(file_path_name, "w") 
        var_file.write(json.dumps({id_param_name: str(column_ids_input[col_index]), 'peroid_type':'hourly', 'data': temp_json_hourly}, indent=2))
        var_file.close()

    print("Generating Hourly Data - End")
    print("-----------------------------------")
    
    return 0

def generateJSONFromNetCDFYearSeparatedFileDaily(filename, year_range, variable_name, column_info, row_info, id_param_name):
    
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    temp_json_daily = {}

    column_ids_input = np.around(column_info['column_ids']).astype(int)

    temp_json_hourly, column_indexes, row_indexes = generateDailyDataFromHourlyData(filename, variable_name, column_info, row_info, year_range)

    print("Generating Daily Data - Start")

    time_multiplier = 24
    for col_index in column_indexes.tolist():    
        for year in range(year_range[0], year_range[1]+1):            
            start_index = 0
            daily_temp_array = {}
            t_array = temp_json_hourly[year][:,col_index].tolist()
            
            for index in range(0, 365):
                temp_array = {}   
                 
                hour_array = np.around(t_array[start_index:(start_index+time_multiplier)], 3).tolist()
                start_index += time_multiplier
                #val = round(sum(hour_array)/len(hour_array), 3)
                temp_array['total'] = round(sum(hour_array), 3)
                temp_array['max'] = round(max(hour_array), 3)
                temp_array['min'] = round(min(hour_array), 3)
                temp_array['average'] = round(sum(hour_array)/len(hour_array), 3)
                temp_array['value'] = hour_array

                daily_temp_array[index] = temp_array

            
            temp_json_daily[year] = daily_temp_array

        file_path_name = "data_preprocessing\\Data\\" + variable_name + "\\Daily\\id_" +str(column_ids_input[col_index]) + ".json"
        var_file = open(file_path_name, "w") 
        var_file.write(json.dumps({id_param_name: str(column_ids_input[col_index]), 'peroid_type':'Daily', 'data': temp_json_daily}, indent=2))
        var_file.close()

    print("Generating Daily Data - End")
    print("-----------------------------------")
    
    return 0

def generateJSONFromNetCDFYearSeparatedFileMonthly(filename, year_range, variable_name, column_info, row_info, id_param_name):
    
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    temp_json_daily = {}

    column_ids_input = np.around(column_info['column_ids']).astype(int)

    temp_json_hourly, column_indexes, row_indexes = generateDailyDataFromHourlyData(filename, variable_name, column_info, row_info, year_range)

    print("Generating Monthly Data - Start")

    time_multiplier = 24
    for col_index in column_indexes.tolist():    
        for year in range(year_range[0], year_range[1]+1):            
            start_index = 0
            monthly_temp_array = {}
            t_array = temp_json_hourly[year][:,col_index].tolist() 
            for index in range(0, 12):
                temp_array = {}   
                
                hour_array = np.around(t_array[start_index:(start_index + time_multiplier * days_in_month[index])], 3).tolist()
                start_index += time_multiplier * days_in_month[index]

                daily_array = []
                day_current_index = 0
                for day_index in range(days_in_month[index]):
                    day_avg = np.around(average(hour_array[day_current_index:(day_current_index+24)]), 3)
                    daily_array.append(day_avg)
                    day_current_index += 24


                
                temp_array['total'] = round(sum(daily_array), 3)
                temp_array['max'] = round(max(daily_array), 3)
                temp_array['min'] = round(min(daily_array), 3)
                temp_array['average'] = round(average(daily_array), 3)
                temp_array['value'] = daily_array

                monthly_temp_array[index] = temp_array

            
            temp_json_daily[year] = monthly_temp_array

        file_path_name = "data_preprocessing\\Data\\" + variable_name + "\\Monthly\\id_" +str(column_ids_input[col_index]) + ".json"
        var_file = open(file_path_name, "w") 
        var_file.write(json.dumps({id_param_name: str(column_ids_input[col_index]), 'peroid_type':'Monthly', 'data': temp_json_daily}, indent=2))
        var_file.close()

    print("Generating Monthly Data - End")
    print("-----------------------------------")
    
    return 0


def generateJSONFromNetCDFDaily(filename, year_range, variable_name, column_info, row_info, id_param_name):
    
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    temp_json_daily = {}

    column_ids_input = np.around(column_info['column_ids']).astype(int)

    temp_json_hourly, column_indexes, row_indexes = generateDailyDataFromDailyData(filename, variable_name, column_info, row_info, year_range)

    print("Generating Daily Data - Start")

    time_multiplier = 24
    for col_index in column_indexes.tolist():    
        for year in range(year_range[0], year_range[1]+1):            
            start_index = 0
            daily_temp_array = {}
            t_array = temp_json_hourly[year][:,col_index].tolist()
            
            for index in range(0, 365):
                temp_array = {}   
                 
                #hour_array = np.around(t_array[start_index:(start_index+time_multiplier)], 3).tolist()
                #start_index += time_multiplier              

                #temp_array['total'] = round(sum(hour_array), 3)
                #temp_array['max'] = round(max(hour_array), 3)
                #temp_array['min'] = round(min(hour_array), 3)
                #temp_array['average'] = round(sum(hour_array)/len(hour_array), 3)
                #temp_array['value'] = hour_array

                temp_array['total'] = round(t_array[index], 3)
                temp_array['max'] = round(t_array[index], 3)
                temp_array['min'] = round(t_array[index], 3)
                temp_array['average'] = round(t_array[index], 3)
                temp_array['value'] = [t_array[index]]

                daily_temp_array[index] = temp_array

            
            temp_json_daily[year] = daily_temp_array

        file_path_name = "data_preprocessing\\Data\\" + variable_name + "\\Daily\\id_" +str(column_ids_input[col_index]) + ".json"
        var_file = open(file_path_name, "w") 
        var_file.write(json.dumps({id_param_name: str(column_ids_input[col_index]), 'peroid_type':'Daily', 'data': temp_json_daily}, indent=2))
        var_file.close()

    print("Generating Daily Data - End")
    print("-----------------------------------")
    
    return 0


def generateJSONFromNetCDFMonthly(filename, year_range, variable_name, column_info, row_info, id_param_name):
    
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    temp_json_daily = {}

    column_ids_input = np.around(column_info['column_ids']).astype(int)

    temp_json_hourly, column_indexes, row_indexes = generateDailyDataFromDailyData(filename, variable_name, column_info, row_info, year_range)

    print("Generating Monthly Data - Start")

    time_multiplier = 24
    for col_index in column_indexes.tolist():    
        for year in range(year_range[0], year_range[1]+1):            
            start_index = 0
            monthly_temp_array = {}
            t_array = temp_json_hourly[year][:,col_index].tolist() 
            for index in range(0, 12):
                temp_array = {}   
                
                #hour_array = np.around(t_array[start_index:(start_index + time_multiplier * days_in_month[index])], 3).tolist()
                #start_index += time_multiplier * days_in_month[index]

                #daily_array = []
                #day_current_index = 0
                #for day_index in range(days_in_month[index]):
                #    day_avg = np.around(average(hour_array[day_current_index:(day_current_index+24)]), 3)
                #    daily_array.append(day_avg)
                #    day_current_index += 24

                daily_array = []
                for day_index in range(days_in_month[index]):
                    day_val = np.around(t_array[index], 3)
                    daily_array.append(day_val)

                
                temp_array['total'] = round(sum(daily_array), 3)
                temp_array['max'] = round(max(daily_array), 3)
                temp_array['min'] = round(min(daily_array), 3)
                temp_array['average'] = round(average(daily_array), 3)
                temp_array['value'] = daily_array

                monthly_temp_array[index] = temp_array

            
            temp_json_daily[year] = monthly_temp_array

        file_path_name = "data_preprocessing\\Data\\" + variable_name + "\\Monthly\\id_" +str(column_ids_input[col_index]) + ".json"
        var_file = open(file_path_name, "w") 
        var_file.write(json.dumps({id_param_name: str(column_ids_input[col_index]), 'peroid_type':'Monthly', 'data': temp_json_daily}, indent=2))
        var_file.close()

    print("Generating Monthly Data - End")
    print("-----------------------------------")
    
    return 0

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
        if flow_acc < 1500 or islake == 1:
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
            file_path_name = "vis\\Data\\" + var_name + "\\Daily\\" +str(seg_id) + ".json"
            var_file = open(file_path_name, "w") 
            var_file.write(dumps({'segment_id': seg_id, 'data': temp_json}, indent=2))
            var_file.close()

            file_path_name_mon = "vis\\Data\\" + var_name + "\\Monthly\\" +str(seg_id) + ".json"
            var_file_mon = open(file_path_name_mon, "w") 
            #sr.record.append(temp_json)        
            var_file_mon.write(dumps({'segment_id': seg_id, 'data': temp_json_mon}, indent=2))
            var_file_mon.close()


            # Writing Metadata Info
            file_path_name = "vis\\Data\\MetaData\\" +str(seg_id) + ".json"
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
            file_path_name = "vis\\Data\\" + var_name + "\\Daily\\" +str(s_id) + ".json"
            var_file = open(file_path_name, "w") 
            var_file.write(dumps({'segment_id': s_id, 'data': temp_json}, indent=2))
            var_file.close()

            file_path_name_mon = "vis\\Data\\" + var_name + "\\Monthly\\" +str(s_id) + ".json"
            var_file_mon = open(file_path_name_mon, "w") 
            #sr.record.append(temp_json)        
            var_file_mon.write(dumps({'segment_id': s_id, 'data': temp_json_mon}, indent=2))
            var_file_mon.close()


            # Writing Metadata Info
            file_path_name = "vis\\Data\\MetaData_Lake\\" +str(s_id) + ".json"
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

'''