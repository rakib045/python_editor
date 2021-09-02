import asyncio
import json
import websockets
import subprocess
import re
import os, random, string


SERVER = 'localhost'
socket_port = 6789
web_port = 8000

list_stored_command = []

class StoredCommand:
    def __init__(self, id, command_list):
        self.id = id
        self.command_list = command_list


'''
CLIENTS = set()

async def notify_everyone(message):
    if CLIENTS:
        await asyncio.wait([user.send(message) for user in CLIENTS])

async def register(websocket):
    CLIENTS.add(websocket)

async def unregister(websocket):
    CLIENTS.remove(websocket)
'''

CLIENTS = []

async def notify_everyone(message):
    if CLIENTS:
        await asyncio.wait([client['websocket'].send(message) for client in CLIENTS])

async def notify_client(message, user_id):
    if CLIENTS:
        await asyncio.wait([client['websocket'].send(message) for client in CLIENTS if client['user_id'] == user_id])                
        
    #await asyncio.wait([user.send(message) for user in CLIENTS])

async def register(websocket, user_id):
    websocket_obj = {}
    websocket_obj['user_id'] = user_id
    websocket_obj['websocket'] = websocket
    CLIENTS.append(websocket_obj)

async def unregister(websocket):    
    for client in CLIENTS:
        if client['websocket'] == websocket:
            CLIENTS.remove(client)
            break

def set_user_id(websocket, user_id):
    for client in CLIENTS:
        if client['websocket'] == websocket:
            client['user_id'] = user_id
            break



async def python_code_processing(websocket, path):
    #process = subprocess.Popen(['python', '--version'],
    #                 stdout=subprocess.PIPE, 
    #                 stderr=subprocess.PIPE)
    #stdout, stderr = process.communicate()

    user_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    #await register(websocket)

    await register(websocket, user_id)

    #await websocket.send(json.dumps({ 'output': stdout.decode("utf-8"), 'error': stderr.decode("utf-8"), 'chart':'', 'markup':'' }))
    await websocket.send(json.dumps({ 'output': user_id, 'error': '', 'chart':'', 'markup':'', 'message_type': 'connection_establish' }))

    try:
        async for message in websocket:
            #message = '{"temp_id":"ABC123","message_type":"request"}'
            data = json.loads(message)
            
            final_output = ''
            data_code = data.get('code')
            data_return_div = data.get('return_div')
            user_id = data.get('user_id')

            if 'message_type' in data and data['message_type'] == 'request':
                index = 0

                set_user_id(websocket, user_id)

                for item in list_stored_command:
                    if item['temp_id'] == data['temp_id'] and item['user_id'] == user_id:
                        final_output = ';##;' + str(item['commands'])
                        del list_stored_command[index]
                        break
                    index += 1                                        
                        
                await notify_client(json.dumps({ 'output': final_output, 'error': '', 'return_div':data_return_div, 'markup':'', 'message_type': 'stacked_call', 'user_id': user_id}), user_id)
                continue

            
            sent_output = ''
            sent_error = ''
            sent_chart = ''

            
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



            all_outputs = sent_output.split(';##;')
            

            for output in all_outputs:
                if output == '':
                    final_output += ';##;'
                    continue
                
                try:
                    commands = json.loads(output.replace('\'','\"'))
                    temp_obj = {}
                    temp_command = []
                    #flag_temp_obj = False
                    obj = []
                    for command in commands:
                        if 'type' in command and command['type'] == 'new_tab':
                            if 'temp_id' in command:
                                temp_obj['temp_id'] = command['temp_id']
                                temp_obj['user_id'] = user_id
                                final_output += '[' + str(command) + ']' + ';##;'
                                continue                            
                                #flag_temp_obj = True
                        
                        temp_command.append(command)
                    
                    temp_obj['commands'] = temp_command

                    if 'temp_id' in temp_obj:
                        list_stored_command.append(temp_obj)
                    else:
                        final_output += output + ';##;'

                except ValueError:
                    final_output += output + ';##;'
            

            #await notify_everyone(json.dumps({ 'output': sent_output, 'error': sent_error, 'return_div':data_return_div, 'markup':''}) )
            await notify_client(json.dumps({ 'output': final_output, 'error': sent_error, 'return_div':data_return_div, 'markup':'', 'message_type': 'returned_call', 'user_id': user_id}), user_id)
    except Exception as e:
        await websocket.send(json.dumps({ 'output': '', 'error': 'Internal Error Occured', 'chart':'', 'markup':''}) )
    finally:
        await unregister(websocket)


if __name__ == "__main__":
    start_server = websockets.serve(python_code_processing, SERVER, socket_port)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()