import asyncio

message_inp = 0
while message_inp != 1:
    try:
        message_inp = int(input('Введите 1, если хотите получить файл tree, в котором хранятся файлы текущей директории: '))
    except ValueError:
        print('Некорректный ввод')


async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)

    print(f'Сообщение {message} отправлено.')

    writer.write(message.encode())

    msg = ''
    while True:
        data = await reader.read(1)
        if not data:
            break
        else:
            msg += data.decode()
    print(msg)
    print(f'Сообщение от сервера получено. Файл для клиента Олеся Ем сохранен.')

    writer.close()
    await writer.wait_closed()

asyncio.run(tcp_echo_client('Олеся Ем'))
