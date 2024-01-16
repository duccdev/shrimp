import multiprocessing, socket
from enum import Enum
from typing import Callable
from concurrent.futures import ThreadPoolExecutor
from threading import Thread


class Method(Enum):
    GET = 1


class Route:
    def __init__(self, method: Method, path: str, handler: Callable) -> None:
        self.method = method
        self.path = path
        self.handler = handler


class Shrimp:
    routes: list[Route]

    def __init__(self) -> None:
        """Creates a Shrimp server"""

        self.routes = []
        self.max_conns = (multiprocessing.cpu_count() * multiprocessing.cpu_count()) * 4
        self.executor = ThreadPoolExecutor(self.max_conns)

    def _serve(self, ip: str, port: int) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_server:
            tcp_server.bind((ip, port))
            tcp_server.listen(self.max_conns)

            while True:
                conn, addr = tcp_server.accept()
                print("Connection from", addr)

                self._handle(conn, addr)

    def _handle(self, conn: socket.socket, addr: tuple[str, int]) -> None:
        while True:
            data = conn.recv(69420)

            if not data:
                break

            conn.sendall(
                bytes(
                    f"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n<h1>{addr[0]}</h1>",
                    "utf-8",
                )
            )

            conn.close()
            break

    def get(self, path: str, handler: Callable) -> None:
        """Creates a GET route

        Args:
            path (str): Route path
            handler (Callable): Route handler
        """

        self.routes.append(Route(Method.GET, path, handler))

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
