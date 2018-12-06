import logging
from uuid import uuid4
from socketio import AsyncServer
from aiohttp import web

sio = AsyncServer()
app = web.Application()
sio.attach(app)

ORDERS_QUEUE = []


@sio.on("orders")
async def orders_msg(sid):
    """Return list of orders"""
    return ORDERS_QUEUE

@sio.on("order")
async def order(sid, data):
    """Make an order"""
    user = data.get("name", "<Unknown>")
    items = data.get("items", [])

    new_order = {
        "id": str(uuid4()),
        "name": user,
        "items": [{"name": item["name"]} for item in items]
    }

    ORDERS_QUEUE.append(new_order)
    await sio.emit("add_order", new_order)
    return {"success": True}

@sio.on("done")
async def done(sid, data):
    """Order completed"""
    global ORDERS_QUEUE
    order_id = data.get("id")
    ORDERS_QUEUE = list(filter(lambda x: x["id"] != order_id, ORDERS_QUEUE))
    return {"success": True}

if __name__ == "__main__":
    web.run_app(app, port=8090)
