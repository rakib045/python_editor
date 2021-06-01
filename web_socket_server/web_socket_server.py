import asyncio
import json
import websockets
import subprocess
import re
import os


SERVER = 'localhost'
socket_port = 6789
web_port = 8000

CLIENTS = set()

async def notify_everyone(message):
    if CLIENTS:
        await asyncio.wait([user.send(message) for user in CLIENTS])

async def register(websocket):
    CLIENTS.add(websocket)

async def unregister(websocket):
    CLIENTS.remove(websocket)


async def python_code_processing(websocket, path):
    process = subprocess.Popen(['python', '--version'],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    await register(websocket)
    await websocket.send(json.dumps({ 'output': stdout.decode("utf-8"), 'error': stderr.decode("utf-8"), 'chart':'', 'markup':'' }))
    try:
        async for message in websocket:
            data = json.loads(message)

            sent_output = ''
            sent_error = ''
            sent_chart = ''

            data_code = data.get('code')
            data_return_div = data.get('return_div')
            f= open("python_chart_temp.py","w+")
            f.write("from util_library import *\n")
            f.write(data_code)
            f.write("\nresult_array = sorted(result_array, key=lambda x: x['order'], reverse=False)\n")
            f.write("print(';##;')\n")
            f.write("print(result_array)")
            f.close()

            #sent_chart = generate_chart(data_chart)
            process = subprocess.Popen(['python', 'python_chart_temp.py'],
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            sent_error = stderr.decode("utf-8")
            sent_output = stdout.decode("utf-8")

            '''
            data_code = data.get('code')
            if data_code:                
                f= open("python_temp.py","w+")
                f.write("from util_library import *")
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
            '''

            await notify_everyone(json.dumps({ 'output': sent_output, 'error': sent_error, 'return_div':data_return_div, 'markup':''}) )
    except Exception as e:
        await websocket.send(json.dumps({ 'output': '', 'error': 'Internal Error Occured', 'chart':'', 'markup':''}) )
    finally:
        await unregister(websocket)


if __name__ == "__main__":
    start_server = websockets.serve(python_code_processing, SERVER, socket_port)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()