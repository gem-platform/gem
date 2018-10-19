import uuid
from multidict import MultiDict
from aiohttp import web
import socketio
import logging

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

orders = []

async def store_image(request):
    data = await request.post()
    mp3 = data['file']
    filename = str(uuid.uuid4()) + mp3.filename
    mp3_file = data['file'].file
    content = mp3_file.read()

    file = open("/usr/shared/downloads/"+filename, "wb")
    file.write(content)
    file.close()

    return web.json_response({"success": True, "path": filename})
    #return web.Response(body={"path": "1234.ololo"}, headers=MultiDict(
    #        {'CONTENT-DISPOSITION': filename}))


@sio.on('connect')
def connect(sid, environ):
    logging.getLogger("root").critical("connect")
    print("connect ", sid)

@sio.on('orders')
async def orders_msg(sid):
    return orders

@sio.on('order')
async def message(sid, data):
    user = data.get("name", "<Unknown>")
    items = data.get("items", [])

    order = {
        "id": str(uuid.uuid4()),
        "name": user,
        "items": [{"name": item["name"]} for item in items]
    }

    orders.append(order)

    logging.getLogger("root").critical(order)

    await sio.emit("add_order", order)

    return {"success": True}

@sio.on('done')
async def message_done(sid, data):
    global orders
    id = data.get("id")
    orders = list(filter(lambda x: x["id"] != id, orders))
    return {"success": True}


if __name__ == '__main__':
    app.router.add_post('/image', store_image)
    web.run_app(app, port=8190)
