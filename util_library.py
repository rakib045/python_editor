import os
from web_socket_server import SERVER, web_port

result_array = []

def addToChart(chart_name, filename, order=100):
    global result_array
    if os.path.exists(filename):
        data_array = {}
        data_array["name"] = chart_name
        data_array["path"] = filename
        data_array["type"] = 'image'
        data_array["order"] = order
        result_array.append(data_array)
    #print(result_array)
    return

def addRiverMapToChart(chart_name, files, order=100):
    global result_array
    filenames = files.replace(' ','').split(',')
    filenames_str = ''
    for filename in filenames:
        if os.path.exists(filename):
            filenames_str += filename + ","
    if filenames_str != '':
        data_array = {}
        data_array['name'] = chart_name
        data_array['path'] = 'http://' + SERVER + ":" + str(web_port) + "/river_map.html?geojson=" + filenames_str[:-1]
        data_array['type'] = 'iframe'
        data_array["order"] = order
        result_array.append(data_array)
    #print(result_array)
    return