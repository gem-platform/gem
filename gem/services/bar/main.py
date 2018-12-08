from socketio import AsyncServer
from aiohttp import web

from bar_controller import BarController

sio = AsyncServer()
app = web.Application()
sio.attach(app)
controller = BarController()


@sio.on("orders")
async def orders(sid):
    """Return list of orders"""
    # pylint: disable=W0613
    return controller.orders


@sio.on("order")
async def order(sid, data):
    """Make an order"""
    # pylint: disable=W0613
    user = data.get("name", "<Unknown>")
    items = data.get("items", [])

    # add new order
    new_order = controller.add(
        user=user,
        items=[{"name": item["name"]} for item in items])

    # response
    await sio.emit("add_order", new_order)
    return {"success": True}


@sio.on("done")
async def done(sid, data):
    """Order completed"""
    # pylint: disable=W0613
    order_id = data.get("id")
    controller.done(order_id)
    return {"success": True}

if __name__ == "__main__":
    web.run_app(app, port=8090)
