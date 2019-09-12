import asyncio

from config import CONFIG
from settings import Settings, load_settings, dump_settings
from sockets import ServerSocket, create_socket_server

SETTINGS = Settings()
SETTINGS_LOCK = asyncio.Lock()


async def client_handler(socket: ServerSocket):
    print('New client')
    # await socket.write(dump_settings(SETTINGS)) # Eventually: Send initial condition

    while True:
        data = await socket.read()
        new_settings = load_settings(data)
        print('Recieved settings:', new_settings)

        async with SETTINGS_LOCK:
            SETTINGS.number = new_settings.number


async def start_server():
    print('Starting socket server')
    await create_socket_server(client_handler, CONFIG['HOST'], CONFIG['PORT'])


async def processing_loop():
    # Simulate long running vision processing loop
    print('Starting processing loop')
    while True:
        async with SETTINGS_LOCK:
            print('number:', SETTINGS.number)
        await asyncio.sleep(1)


async def main():
    print('Starting backend')

    # List of all threads to run concurrently
    threads = (start_server(), processing_loop())

    try:
        await asyncio.gather(*threads)
        print('Exited all threads, but shouldn\'t have!')
    finally:
        print('Closing')


if __name__ == '__main__':
    asyncio.run(main())
