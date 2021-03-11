import asyncio
import json
import websockets
import subprocess
import re
import os

def generate_image_markup(data_chart):
    temp_array = data_chart.split('\n')
    result_array = []
    for item in temp_array:
        if 'addToChart' in item:            
            filename = re.search("'(.*)'", item).group(1)
            if os.path.exists(filename):
                temp = {}
                temp['name'] = filename
                temp['path'] = filename
                order_val = re.search(",(.*)\)", item).group(1)
                if order_val.isnumeric():
                    temp['order'] = int(order_val)
                else:
                    temp['order'] = 100
                result_array.append(temp)

    result_array = sorted(result_array, key=lambda x: x['order'], reverse=False)
    return result_array


async def python_code_processing(websocket, path):
    process = subprocess.Popen(['python', '--version'],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    await websocket.send(json.dumps({ 'output': stdout.decode("utf-8"), 'error': stderr.decode("utf-8"), 'chart':'', 'markup':'' }))
    try:
        async for message in websocket:
            data = json.loads(message)

            data_code = data['code']
            data_chart = data['chart']

            f= open("python_temp.py","w+")
            f.write(data_code)
            f.close()

            process = subprocess.Popen(['python', 'python_temp.py'],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            chart_json_data = generate_image_markup(data_chart)
            await websocket.send(json.dumps({ 'output': stdout.decode("utf-8"), 'error': stderr.decode("utf-8"), 'chart':chart_json_data, 'markup':'' }) )
    except Exception as e:
        await websocket.send(json.dumps({ 'output': '', 'error': 'Internal Error Occured', 'chart':'', 'markup':'' }) )


if __name__ == "__main__":
    start_server = websockets.serve(python_code_processing, "127.0.0.1", 6789)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()