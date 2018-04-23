import socketio
import asyncio
from aiohttp import web
from gem.core import Endpoint, Event


class GemNamespace(socketio.AsyncNamespace):
    def __init__(self, namespace=None):
        super().__init__(namespace)
        self.event = Event()

    async def trigger_event(self, event, *args):
        return self.event.notify(event, *args)


class SocketIoEndpoint(Endpoint):
    """Socket.io endpoint."""

    def __init__(self, host, port):
        """
        Initialize new instance of the SocketIoEndpoint class.

        Arguments:
            host {str} -- Host.
            port {int} -- Port.
        """
        super().__init__()
        self.__context = None
        self.__host = host
        self.__port = port

        self.__sio = socketio.AsyncServer()
        self.__app = web.Application()
        self.__sio.attach(self.__app)
        self.__namespace = GemNamespace()
        self.__namespace.event.subscribe(self.__on_event)

        self.__sio.register_namespace(self.__namespace)

    def open(self):
        web.run_app(self.__app, host=self.__host, port=self.__port)

    def close(self):
        pass

    def emit(self, event, data, to=None):
        loop = asyncio.get_event_loop()
        loop.create_task(self.__sio.emit(event, data, room=to))

    def join(self, sid, room):
        self.__sio.enter_room(sid, room)

    def leave(self, sid, room):
        self.__sio.leave_room(sid, room)

    def __on_event(self, event, sid, *data):
        return self.event.notify(event, sid, *data)
