import asyncio
import os
import json
from datetime import *
import subprocess


# функция Олеси Ем
def save_to_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


# функция Олеси Ем
async def em():
    paths = os.environ.get('PATH').split(os.pathsep)
    executables = {}
    for path in paths:
        for root, dirs, files in os.walk(path):
            for file in files:
                if os.access(os.path.join(root, file), os.X_OK):
                    executables.setdefault(root, []).append(file)

    if not os.path.exists('tree.json'):
        save_to_json(executables, 'tree.json')
    else:
        os.remove('tree.json')
        save_to_json(executables, 'tree.json')

    print('файл сохранен в директории ', os.getcwd())


# Функция Кати Аб
async def ab():
    info = []
    for process in os.popen('tasklist').readlines()[4:]:
        process_data = process.split()
        process_info = {
            'Name': process_data[0],
            'PID': process_data[1],
            'Session Name': process_data[2],
            'Session Number': process_data[3],
            'Mem Usage (KB)': process_data[4]
        }
        info.append(process_info)
    now = datetime.now()
    folder_path = now.strftime('%d-%m-%Y')
    os.makedirs(folder_path, exist_ok=True)
    file_path = f'{folder_path}/{now.strftime("%H-%M-%S")}.json'
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f'Файл будет сохранен в: {current_dir}/{folder_path}')
    save_to_json(info, file_path)


async def handle_client(reader, writer):
    data = await reader.read(100)
    message = data.decode()

    if message == 'Client 1':
        await em()

    elif message == 'Client 2':
        await ab()

    response = f"Server received: {message}"
    writer.write(response.encode())
    await writer.drain()

    writer.close()


async def main():

    server = await asyncio.start_server(
        handle_client, '127.0.0.1', 8888)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())