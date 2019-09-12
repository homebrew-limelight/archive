import asyncio
from starlette.applications import Starlette
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocketDisconnect
import uvicorn
from config import CONFIG
from settings import Settings, dump_settings
from sockets import ClientSocket

app = Starlette(debug=True)
app.mount('/static', StaticFiles(directory='static'))

SOCKET = ClientSocket(CONFIG['HOST'], CONFIG['PORT'])


async def send_daemon(data: bytes):
    await SOCKET.write(data)


async def send_settings(number: int):
    settings = Settings(number)
    print('Sending data:', settings)
    data = dump_settings(settings)
    return await send_daemon(data)


@app.route('/')
async def main_page(request):
    return FileResponse('static/index.html')


@app.websocket_route('/ws')
async def ws_loop(ws):
    await ws.accept()
    print('New websocket:', ws.client.host)

    while True:
        try:
            data = await ws.receive_json()
        except WebSocketDisconnect:
            print('Disconnect websocket:', ws.client.host)
            return
        try:
            number = data['number']
        except KeyError:
            print('JSON doesn\'t have \'number\' key:\'', data)
            await ws.send_json({'status': 'error', 'text': 'Missing \'number\' key'})
        else:
            try:
                # Todo: cannot accept more data until finished processing settings
                # Find a way to fork into background
                await send_settings(number)
            except ConnectionError as e:
                print(e)
                await ws.send_json({'status': 'error', 'text': e.args})
            else:
                await ws.send_json({'status': 'ok', 'text': 'OK'})


async def test():
    for x in range(100):
        await send_settings(x)
        await asyncio.sleep(2)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5000)
