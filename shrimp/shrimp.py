import multiprocessing, socket
from concurrent.futures import ThreadPoolExecutor
from traceback import print_exc
from threading import Thread
from typing import Callable
from .route import Route
from .httpmethod import HttpMethod
from .httpstatus import NotFound
from .request import Request
from .response import BaseResponse

__all__ = ("Shrimp",)


class Shrimp:
    def __init__(self) -> None:
        """Creates a Shrimp server"""

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.routes: list[Route] = []
        self.max_conns = (multiprocessing.cpu_count() * multiprocessing.cpu_count()) * 4
        self.executor = ThreadPoolExecutor(self.max_conns)

    def _serve(self, ip: str, port: int) -> None:
        """Internal serve function, Shrimp.serve and Shrimp.nbserve is a wrapper on Shrimp._serve

        Args:
            ip (str): IP
            port (int): Port
        """

        self._socket.bind((ip, port))
        self._socket.listen(self.max_conns)

        try:
            while True:
                conn, addr = self._socket.accept()

                try:
                    self._handle(conn, addr)
                except:
                    print_exc()
                    conn.close()
        except KeyboardInterrupt:
            self.close()
        except OSError as e:
            if e.errno == 9:
                return

            raise e

    def _handle(self, conn: socket.socket, addr: tuple[str, int]) -> None:
        """Internal connection handler

        Args:
            conn (socket.socket): TCP client socket
            addr (tuple[str, int]): Client address
        """

        while True:
            data = conn.recv(69420)

            if not data:
                conn.close()
                return

            req = Request(data.decode())

            for route in self.routes:
                if route.path == req.path:
                    conn.sendall(route.handler(req).raw())
                    conn.close()
                    return

            conn.sendall(
                BaseResponse(
                    NotFound, {"Content-Type": "text/html"}, "<h1>Not Found</h1>"
                ).raw()
            )
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

        self._serve(ip, port)

    def nbserve(self, ip: str = "0.0.0.0", port: int = 8080) -> None:
        """Starts serving Shrimp on IP:port (is non-blocking, for blocking serve, use Shrimp.serve)

        Args:
            ip (str, optional): IP. Defaults to "0.0.0.0".
            port (int, optional): Port. Defaults to 8080.
        """

        Thread(target=self._serve, args=(ip, port)).start()

    def close(self) -> None:
        self._socket.close()
