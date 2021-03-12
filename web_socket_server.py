import asyncio
import json
import websockets
import subprocess
import re
import os

import util_library

SERVER = '127.0.0.1'
socket_port = 6789
web_port = 8000

'''
def generate_chart(data_chart):
    temp_array = data_chart.split('\n')
    result_array = []
    try:
        for item in temp_array:
            if 'addToChart' in item:            
                filename = re.search("'(.*)'", item).group(1)
                if os.path.exists(filename):
                    temp = {}
                    temp['name'] = filename
                    temp['path'] = filename
                    temp['type'] = 'image'
                    order_val = re.search(",(.*)\)", item.replace(' ','')).group(1)
                    if order_val.isnumeric():
                        temp['order'] = int(order_val)
                    else:
                        temp['order'] = 100
                    result_array.append(temp)
            elif 'addRiverMapToChart' in item:
                filenames = re.search("'(.*)'", item).group(1).replace(' ','').split(',')
                filenames_str = ''
                for filename in filenames:
                    if os.path.exists(filename):
                        filenames_str += filename + ","
                
                if filenames_str != '':
                    temp = {}
                    temp['name'] = "Chart"
                    temp['path'] = 'http://' + SERVER + ":" + str(web_port) + "/river_map.html?geojson=" + filenames_str[:-1]
                    temp['type'] = 'iframe'
                    order_val = re.search(",(.*)\)", item.replace(' ','')).group(1)
                    if order_val.isnumeric():
                        temp['order'] = int(order_val)
                    else:
                        temp['order'] = 100
                    result_array.append(temp)

        result_array = sorted(result_array, key=lambda x: x['order'], reverse=False)
    except:
        result_array = []
    return result_array
'''

async def python_code_processing(websocket, path):
    process = subprocess.Popen(['python', '--version'],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    await websocket.send(json.dumps({ 'output': stdout.decode("utf-8"), 'error': stderr.decode("utf-8"), 'chart':'', 'markup':'' }))
    try:
        async for message in websocket:
            data = json.loads(message)

            sent_output = ''
            sent_error = ''
            sent_chart = ''

            data_code = data.get('code')
            if data_code:                
                f= open("python_temp.py","w+")
                f.write(data_code)
                f.close()

                process = subprocess.Popen(['python', 'python_temp.py'],
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                sent_output = stdout.decode("utf-8")
                sent_error = stderr.decode("utf-8")
            
            data_chart = data.get('chart')
            if data_chart:
                f= open("python_chart_temp.py","w+")
                f.write("from util_library import *")
                f.write(data_chart)
                f.write("\nresult_array = sorted(result_array, key=lambda x: x['order'], reverse=False)\n")
                f.write("print(result_array)")
                f.close()

                #sent_chart = generate_chart(data_chart)
                process = subprocess.Popen(['python', 'python_chart_temp.py'],
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                sent_error = stderr.decode("utf-8")
                sent_chart = stdout.decode("utf-8")

            await websocket.send(json.dumps({ 'output': sent_output, 'error': sent_error, 'chart':sent_chart, 'markup':'' }) )
    except Exception as e:
        await websocket.send(json.dumps({ 'output': '', 'error': 'Internal Error Occured', 'chart':'', 'markup':'' }) )


if __name__ == "__main__":
    start_server = websockets.serve(python_code_processing, SERVER, socket_port)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()