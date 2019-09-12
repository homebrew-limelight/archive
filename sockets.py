import abc
import asyncio
from typing import Callable


class Socket(abc.ABC):
    TERMINATOR = b'\xDE\xAD\xBE\xEF'

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port

        self.reader: asyncio.StreamReader = None
        self.writer: asyncio.StreamWriter = None

        self._lock = asyncio.Lock()

    @abc.abstractmethod
    async def _reopen(self):
        pass

    async def __check_socket(self) -> None:  # Do not call unless you have the lock
        if self.writer is None or self.writer.is_closing():
            self.reader, self.writer = await self._reopen()

    async def write(self, data: bytes) -> None:
        async with self._lock:
            await self.__check_socket()
            self.writer.write(data)
            self.writer.write(Socket.TERMINATOR)
            await self.writer.drain()

    async def read(self) -> bytes:
        async with self._lock:
            await self.__check_socket()
            data = await self.reader.readuntil(Socket.TERMINATOR)
            data = data[: -len(Socket.TERMINATOR)]

            return data


class ClientSocket(Socket):
    async def _reopen(self):
        return await asyncio.open_connection(host=self.host, port=self.port)


class ServerSocket(Socket):
    def __init__(self, host: str, port: int, reader, writer) -> None:
        super().__init__(host=host, port=port)

        self.reader = reader
        self.writer = writer

    async def _reopen(self):
        raise ConnectionError()


HANDLER_TYPE = Callable[[ServerSocket], None]


async def create_socket_server(handler: HANDLER_TYPE, host: str, port: int):
    async def handler_wrapper(reader, writer):
        socket = ServerSocket(host, port, reader, writer)
        await handler(socket)

    return await asyncio.start_server(handler_wrapper, host=host, port=port)
