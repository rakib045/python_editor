import pygrib
import wget
from datetime import date
import os
import numpy as np

baseurl = 'https://dd.weather.gc.ca/model_hrdps/prairies/grib2/00/'
# Maximum 48 hour for prairies
forcasted_hour_range = [0, 48]
output_filename = 'snow_depth_20230323-00.csv'

filename_first_part = 'CMC_hrdps_prairies'
filename_second_part = '_SNOD_SFC_0_ps2.5km_'
filename_third_part = '[date]00_P***-00.grib2'

latitude_longitude_file_name = 'lamprairiepoints'
#first one is the row and second one is the column
size = (570, 655)
lat_info = np.zeros(size)
long_info = np.zeros(size)

lat_lon_text = open(latitude_longitude_file_name, 'r')
lines = lat_lon_text.readlines()
for k in range(1, len(lines)):
    columns = lines[k].replace('\n','').split(' ')
    i = int(columns[0])-1
    j = int(columns[1])-1
    lat_info[j][i] = float(columns[2])
    long_info[j][i] = float(columns[3]) 
lat_lon_text.close()


o_file = open(output_filename, "w")
o_file.write("date, hour, value, grid_i, grid_j, latitude, longitude\n")
o_file.close()


for index in range(forcasted_hour_range[0], forcasted_hour_range[1]+1):
    hour = f'{index:03d}'
    today = date.today()
    date_str = today.strftime("%Y%m%d") 
    filename_third_part_temp = filename_third_part.replace('[date]', date_str).replace('***', hour)
    file_name = filename_first_part + filename_second_part + filename_third_part_temp 
    url = baseurl + hour + '/' + file_name
    wget.download(url)
    o_file = open(output_filename, "a+")

    gr = pygrib.open(file_name)
    for g in gr:
        array_values = g.values
        for j in range(array_values.shape[0]):
            for i in range(array_values.shape[1]):
                value = array_values[j][i]
                grid_i = i+1
                grid_j = j+1
                lat = lat_info[j][i] 
                long = long_info[j][i] 
                o_file.write(f"{today}, {hour}, {value}, {grid_i}, {grid_j}, {lat}, {long}\n")
    gr.close()
    o_file.close()
    os.remove(file_name)

    print("File Completed:" + str(index+1) + "/" + str(forcasted_hour_range[1] + 1)) 

