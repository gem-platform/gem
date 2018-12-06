import logging
from uuid import uuid4
from socketio import AsyncServer
from aiohttp import web

sio = AsyncServer()
app = web.Application()
sio.attach(app)

orders = []


@sio.on("orders")
async def orders_msg(sid):
    return orders

@sio.on("order")
async def message(sid, data):
    user = data.get("name", "<Unknown>")
    items = data.get("items", [])

    order = {
        "id": str(uuid4()),
        "name": user,
        "items": [{"name": item["name"]} for item in items]
    }

    orders.append(order)
    await sio.emit("add_order", order)
    return {"success": True}

@sio.on("done")
async def message_done(sid, data):
    global orders
    order_id = data.get("id")
    orders = list(filter(lambda x: x["id"] != order_id, orders))
    return {"success": True}

if __name__ == "__main__":
    web.run_app(app, port=8090)
