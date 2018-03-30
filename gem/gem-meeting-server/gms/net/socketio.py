import socketio
import asyncio
from aiohttp import web

from gem.core import Endpoint


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

        self.__sio.on("connect", self.__on_connect)
        self.__sio.on("disconnect", self.__on_disconnect)
        self.__sio.on("handshake", self.__on_message("handshake"))
        self.__sio.on("switch_stage", self.__on_message("switch_stage"))
        self.__sio.on("vote", self.__on_message("vote"))
        self.__sio.on("comment", self.__on_message("comment"))
        self.__sio.on("request_floor", self.__on_message("request_floor"))
        self.__sio.on("withdraw_from_queue", self.__on_message("withdraw_from_queue"))
        self.__sio.on("remove_from_queue", self.__on_message("remove_from_queue"))
        self.__sio.on("give_voice", self.__on_message("give_voice"))

    def open(self):
        web.run_app(self.__app, host=self.__host, port=self.__port)

    def close(self):
        pass

    def emit(self, event, data, to=None):
        loop = asyncio.get_event_loop()
        loop.create_task(self.__sio.emit(event, data))

    async def __on_connect(self, sid, environ):
        self.event.notify("connect", sid)

    async def __on_disconnect(self, sid):
        self.event.notify("disconnect", sid)

    def __on_message(self, name):
        async def callback(sid, data):
            return self.event.notify(name, sid, data)
        return callback
