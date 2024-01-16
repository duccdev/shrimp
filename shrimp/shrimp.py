import asyncio, socket, multiprocessing
from concurrent.futures import ThreadPoolExecutor
from typing import Callable
from .route import Route
from .httpmethod import HttpMethod
from .httpstatus import NotFound
from .request import Request
from .response import BaseResponse

__all__ = ("Shrimp",)


async def maybe_coroutine(func, *args, **kwargs):
    if asyncio.iscoroutine(func):
        return await func
    elif asyncio.iscoroutinefunction(func):
        return await func(*args, **kwargs)
    else:
        return func(*args, **kwargs)


class Shrimp:
    routes: list[Route]

    def __init__(self) -> None:
        """Creates a Shrimp server"""

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.routes = []
        self.max_conns = (multiprocessing.cpu_count() * multiprocessing.cpu_count()) * 4
        self.executor = ThreadPoolExecutor(self.max_conns)

    async def _serve(self, ip: str, port: int) -> None:
        """Internal serve function, Shrimp.serve and Shrimp.nbserve is a wrapper on Shrimp._serve

        Args:
            ip (str): IP
            port (int): Port
        """

        self._socket.bind((ip, port))
        self._socket.listen(self.max_conns)

        try:
            while True:
                conn, addr = await self.loop.sock_accept(self._socket)
                asyncio.ensure_future(self._handle(conn, addr))
        except KeyboardInterrupt:
            self.close()
        except OSError as e:
            if e.errno == 9:
                return
            raise e

    async def _handle(self, conn: socket.socket, addr: tuple[str, int]) -> None:
        """Internal connection handler

        Args:
            conn (socket.socket): TCP client socket
            addr (tuple[str, int]): Client address
        """

        data = await self.loop.sock_recv(conn, 69420)

        if not data:
            conn.close()
            return

        req = Request(data.decode())

        for route in self.routes:
            if route.path == req.path:
                response = await maybe_coroutine(route.handler, req)
                await self.loop.sock_sendall(conn, response.raw())
                conn.close()
                return

        response = BaseResponse(
            NotFound, {"Content-Type": "text/html"}, "<h1>Not Found</h1>"
        )
        await self.loop.sock_sendall(conn, response.raw())
        conn.close()
        return

    def get(self, path: str):
        """Decorator for creating a GET route

        Args:
            path (str): Route path

        Decorated function args:
            req (Request): Request data

        Decorated function return: BaseResponse
        """

        def wrapper(handler: Callable[[Request], BaseResponse]):
            self.routes.append(Route(HttpMethod.GET, path, handler))

        return wrapper

    def serve(self, ip: str = "0.0.0.0", port: int = 8080) -> None:
        """Starts serving Shrimp on IP:port (is blocking, for non-blocking serve, use Shrimp.serve)

        Args:
            ip (str, optional): IP. Defaults to "0.0.0.0".
            port (int, optional): Port. Defaults to 8080.
        """

        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self._serve(ip, port))

    def nbserve(self, ip: str = "0.0.0.0", port: int = 8080) -> None:
        """Starts serving Shrimp on IP:port (is non-blocking, for blocking serve, use Shrimp.serve)

        Args:
            ip (str, optional): IP. Defaults to "0.0.0.0".
            port (int, optional): Port. Defaults to 8080.
        """

        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self._serve(ip, port))

    def close(self) -> None:
        self.loop.close()
        self._socket.close()
