import uuid
import logging
from socketio import AsyncServer
from aiohttp import web

sio = AsyncServer()
app = web.Application()
sio.attach(app)

orders = []


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
    web.run_app(app, port=8090)
