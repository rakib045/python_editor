import sys
import webbrowser

import http.server
import socketserver
from urllib.parse import urlparse
from urllib.parse import parse_qs
import shapefile
from json import dumps

import time
import codecs
import getopt
import requests

import asyncio
import datetime
import random
import websockets


server = '127.0.0.1'
port = '80'
client_name = 'Client'
message = ''
server_type = ''
coversion = ''
input_filename = ''
output_filename = 'jeoJSON.json'

param =False
json_file = ''
color_list = []
refresh=False

bbox_lon_min = 0.00
bbox_lon_max = 0.00
bbox_lat_min = 0.00
bbox_lat_max = 0.00

CLIENTS = set()


def generateGeoJSON(shp_file_name, output_filename):

    
    print("GeoJSON generation started ...")

    start = time.time()

    #myshp = open(shp_file_name, "rb")
    #mydbf = open(dbf_file_name, "rb") 
    #reader = shapefile.Reader(shp=myshp, dbf=mydbf)
    reader = shapefile.Reader(shp_file_name)

    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    buffer = []
    
    index=0

    xmin = bbox_lon_min  # Lon
    xmax = bbox_lon_max
    ymin = bbox_lat_min  #Lat
    ymax = bbox_lat_max

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

def generate_help_msg():
    help_msg =  "To generate JSON file from SHAPE file within a bounding box,\n"
    help_msg += "python RiverBasin.py --conversion=ShapeToGeoJSON --bbox=\"<min_lon>, <max_lon>, <min_lat>, <max_lat>\" --input_filename=<shape_filename> --output_filename=<output_filename>\n"
    help_msg += "It usually took lots of time to finish the job. Sample bbox=\"-107.74566, -105.65277, 51.544626, 52.72631\" \n"
    help_msg += "----------------------------------------------------------------------------------------\n"

    help_msg +=  "To start a Web-Socket,\n"
    help_msg += "python RiverBasin.py --start=web-socket --server=<server_ip> --port=[<port_number>]\n"
    help_msg += "Web socket will be open at ws://<server>:<port> and port number is optional and 80 is default value\n"
    help_msg += "----------------------------------------------------------------------------------------\n"

    help_msg +=  "To start a Web-Server,\n"
    help_msg += "python RiverBasin.py --start=web-server --port=[<port_number>]\n"
    help_msg += "Server would be always localhost and port number is optional and 80 is default value\n"
    help_msg += "----------------------------------------------------------------------------------------\n"
       
    help_msg +=  "To pass param,\n"
    help_msg += "python RiverBasin.py --param=1 --server=<server_ip> --port=<port_number> --color_list=\"<red>, <green>, <blue>, ...\" --json_file=<json_file_path>\n"
    help_msg += "----------------------------------------------------------------------------------------\n"
    
    help_msg +=  "To pass param and refresh page,\n"
    help_msg += "python RiverBasin.py --param=1 --server=<server_ip> --port=<port_number> --refresh=True\n"
    help_msg += "----------------------------------------------------------------------------------------\n"

    return help_msg

def inputParam():
    global server, message, port, server_type, client_name, coversion, input_filename, output_filename
    global bbox_lon_min, bbox_lon_max, bbox_lat_min, bbox_lat_max, param, color_list, json_file, refresh
    try:
        opts, args = getopt.getopt(sys.argv[1:], "v:p:m:s:c:x:i:o:b:a:j:l:r", ["server=", "port=", "message=", "start=", 
        "clientname=", "conversion=", "input_filename=", "output_filename=", "bbox=", "param=", "json_file=", "color_list=", "refresh="])
    except getopt.GetoptError:
        print(generate_help_msg())
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(generate_help_msg())
            sys.exit()
        elif opt in ("-v", "--server"):
            server = arg
        elif opt in ("-m", "--message"):
            message = arg
        elif opt in ("-p", "--port"):
            port = arg
        elif opt in ("-s", "--start"):
            server_type = arg
        elif opt in ("-c", "--clientname"):
            client_name = arg
        elif opt in ("-x", "--conversion"):
            coversion = arg
        elif opt in ("-i", "--input_filename"):
            input_filename = arg
        elif opt in ("-o", "--output_filename"):
            output_filename = arg
        elif opt in ("-b", "--bbox"):
            values = arg.replace('[','').replace(']','').split(',')
            bbox_lon_min = float(values[0])
            bbox_lon_max = float(values[1])
            bbox_lat_min = float(values[2])
            bbox_lat_max = float(values[3])
        elif opt in ("-a", "--param"):
            param = True
        elif opt in ("-j", "--json_file"):
            json_file = arg
        elif opt in ("-l", "--color_list"):
            color_list = arg.replace('[','').replace(']','').split(',')
        elif opt in ("-r", "--refresh"):
            refresh = bool(arg)

async def command_client():
    uri = "ws://" + server + ":" + port
    async with websockets.connect(uri) as websocket:
        msg_json = dumps({"message": message, "json_file": json_file, "color_list": color_list, "refresh": refresh})
        print(msg_json)
        await websocket.send(msg_json)
        return_msg = await websocket.recv()
        print(return_msg)

async def notify_everyone(message):
    if CLIENTS:
        print("Sending message to everyone: " + str(message))
        await asyncio.wait([user.send(message) for user in CLIENTS])

async def register(websocket):
    #await notify_everyone(client_name + " got connected")
    CLIENTS.add(websocket)

async def unregister(websocket):
    #await notify_everyone(client_name + " got disconnected")
    CLIENTS.remove(websocket)

async def message_pass_server(websocket, path):
    await register(websocket)
    try:        
        async for message in websocket:
            await notify_everyone(message)
    finally:
        await unregister(websocket)


if __name__ == "__main__":

    inputParam()
    argv = sys.argv

    if server_type == 'web-server':
        handler_object = http.server.SimpleHTTPRequestHandler
        if port.isnumeric():            
            with socketserver.TCPServer(("", int(port)), handler_object) as httpd:
                print("Serving web-server at : http://localhost:" + port)
                if input_filename == '':
                    input_filename = 'index.html'
                webbrowser.open("http://localhost:" + port + '/' + input_filename)
                httpd.serve_forever()
        else:
            print("Please, provide a valid port number !!")

    elif server_type == 'web-socket':
        start_server = websockets.serve(message_pass_server, server, port)
        asyncio.get_event_loop().run_until_complete(start_server)
        print("Serving web-socket(echo) at : ws://" + server + ":" + port)
        asyncio.get_event_loop().run_forever()
    elif coversion == 'ShapeToGeoJSON':
        generateGeoJSON(input_filename, output_filename)
    elif param:
        asyncio.get_event_loop().run_until_complete(command_client())



    
    
