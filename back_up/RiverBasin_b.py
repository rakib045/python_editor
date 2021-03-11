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

CLIENTS = set()


def generateGeoJSON(shp_file_name, dbf_file_name):

    #reader = shapefile.Reader(shp_file_name)
    print("GeoJSON generation started")

    start = time.time()

    myshp = open(shp_file_name, "rb")
    mydbf = open(dbf_file_name, "rb") 
    reader = shapefile.Reader(shp=myshp, dbf=mydbf)

    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    buffer = []
    
    index=0

    xmin = -107.74566650390625  # Lon
    xmax = -105.65277099609375
    ymin = 51.544626967214434  #Lat
    ymax = 52.72631243810711

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
        #print(sr.shape.bbox)
    
        # write the GeoJSON file
    
    geojson = open("jeoJSON_river.json", "w")
    geojson.write(dumps({"type": "FeatureCollection", "features": buffer}, indent=2) + "\n")
    geojson.close()
    print("Total Shape Count: " + str(index))
    end = time.time()
    print(f"Runtime of the conversion is {end - start}")
    print("GeoJSON generation completed")


def inputParam():
    global server, message, port, server_type, client_name
    try:
        opts, args = getopt.getopt(sys.argv[1:], "v:p:m:s:c", ["server=", "port=", "message=", "start=", "clientname=",])
    except getopt.GetoptError:
        print ('RiverBasin.py --url=[<url>] --message=[<message>]')
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print ('RiverBasin.py --url=[<url>] --message=[<message>]')
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

async def hello():
    uri = "ws://" + server + ":" + port
    async with websockets.connect(uri) as websocket:
        msg = client_name + ": " + message
        print(msg)
        await websocket.send(msg)
        return_msg = await websocket.recv()
        print(return_msg)


async def notify_everyone(message):
    if CLIENTS:
        print("Sending message to everyone: " + message)
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
                webbrowser.open("http://localhost:" + port + '/a.html')
                httpd.serve_forever()
        else:
            print("Please, provide a valid port number !!")

    elif server_type == 'web-socket':
        start_server = websockets.serve(message_pass_server, server, port)
        asyncio.get_event_loop().run_until_complete(start_server)
        print("Serving web-socket(echo) at : ws://" + server + ":" + port)
        asyncio.get_event_loop().run_forever()
    else:
        asyncio.get_event_loop().run_until_complete(hello())

    #generateGeoJSON(shp_file_name = "HydroRIVERS_v10_na_shp/HydroRIVERS_v10_na.shp", dbf_file_name="HydroRIVERS_v10_na_shp/HydroRIVERS_v10_na.dbf")
    #generateGeoJSON(shp_file_name = "na_riv_30s/na_riv_30s.shp", dbf_file_name="na_riv_30s/na_riv_30s.dbf")


    
    
