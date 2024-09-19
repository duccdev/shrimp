import signal, socket, sys
from concurrent.futures import ThreadPoolExecutor
from traceback import print_exc
from threading import Thread
from typing import Callable

from .route import Route
from .httpmethod import HttpMethod
from .httpstatus import InternalServerError, NotFound, ContentTooLarge
from .request import Request
from .response import BaseResponse, HTMLResponse

__all__ = ("Shrimp",)


class Shrimp:
    def __init__(self, max_req_size: int = 16384) -> None:
        """Creates a Shrimp server

        ## Arguments:
            `max_conns` (`int`, optional, `100000`): Max connections and threads. (Set to 0 for no limit)
            `max_req_size` (`int`, optional, `16384`): Max request size.
        """

        self.routes: list[Route] = []
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.max_req_size = max_req_size

    def _serve(self, ip: str, port: int, max_conns: int = 100000) -> None:
        """Internal serve function, Shrimp.serve and Shrimp.serve_non_blocking is a wrapper on Shrimp._serve

        ## Arguments:
            `ip` (`str`): IP
            `port` (`int`): Port
            `max_conns` (`int`, optional, `100000`): Max connections and threads. (Set to 0 for no limit)

        ## Raises:
            `OSError`: When there is an error trying to create the socket
        """

        self._socket.bind((ip, port))
        self._socket.listen(max_conns)

        if max_conns == 0:
            unlimited_conns = True
        else:
            unlimited_conns = False
            executor = ThreadPoolExecutor(max_workers=max_conns)

        def sigint_handler(s, f) -> None:
            if not unlimited_conns:
                executor.shutdown(wait=True)

            self._socket.close()
            exit(0)

        signal.signal(signal.SIGINT, sigint_handler)

        try:
            while True:
                conn, addr = self._socket.accept()

                def handler() -> None:
                    try:
                        self._handle(conn, addr)
                    except:
                        print_exc()
                        conn.close()

                if unlimited_conns:
                    Thread(target=handler).start()
                    continue

                executor.submit(handler)
        except OSError as e:
            if e.errno == 9:
                return

            raise e

    def _handle(self, conn: socket.socket, addr: tuple[str, int]) -> None:
        """Internal connection handler

        ## Arguments:
            `conn` (`socket.socket`): TCP client socket
            `addr` (`tuple[str, int]`): Client address

        ## Raises:
            `TypeError`: When the route returns something other than a BaseResponse
        """

        while True:
            try:
                data = conn.recv(self.max_req_size + 1)
            except:
                conn.close()
                return

            if not data:
                conn.close()
                return

            if len(data) >= (self.max_req_size + 1):
                try:
                    conn.sendall(
                        HTMLResponse(
                            "<h1>Content Too Large</h1>", ContentTooLarge
                        )._raw()
                    )
                except:
                    pass

            try:
                req = Request(data.decode())
            except:
                print_exc(file=sys.stderr)
                try:
                    conn.sendall(
                        HTMLResponse(
                            "<h1>Internal Server Error</h1>", InternalServerError
                        )._raw()
                    )
                except:
                    pass
                conn.close()
                return

            for route in self.routes:
                if route.path == req.path and route.method == req.method:
                    res = route.handler(req)

                    if not isinstance(res, BaseResponse):
                        raise TypeError(
                            f"Expected BaseResponse-derived value from route, got {type(res)}"
                        )

                    try:
                        conn.sendall(res._raw())
                    except:
                        pass
                    conn.close()
                    return

            try:
                conn.sendall(HTMLResponse("<h1>Not Found</h1>", NotFound)._raw())
            except:
                pass
            conn.close()
            return

    def get(self, path: str):
        """Decorator for creating a GET route

        ## Arguments:
            `path` (`str`): Route path

        ## Decofunction arguments:
            `req` (`Request`): Request data

        ## Decofunction returns:
            `BaseResponse` or any subclass
        """

        def wrapper(handler: Callable[[Request], BaseResponse]):
            self.routes.append(Route(HttpMethod.GET, path, handler))

        return wrapper

    def serve(
        self, ip: str = "0.0.0.0", port: int = 8080, max_conns: int = 100000
    ) -> None:
        """Starts serving Shrimp on IP:port (is blocking, for non-blocking serve, use Shrimp.serve_non_blocking)

        ## Arguments:
            `ip` (`str`, optional, `"0.0.0.0"`): Server IP.
            `port` (`int`, optional, `8080`): Server port.
            `max_conns` (`int`, optional, `100000`): Max connections and threads. (Set to 0 for no limit)
        """

        self._serve(ip, port)

    def serve_non_blocking(
        self, ip: str = "0.0.0.0", port: int = 8080, max_conns: int = 100000
    ) -> None:
        """Starts serving Shrimp on IP:port (is non-blocking, for blocking serve, use Shrimp.serve)

        ## Arguments:
            `ip` (`str`, optional, `"0.0.0.0"`): Server IP.
            `port` (`int`, optional, `8080`): Server port.
            `max_conns` (`int`, optional, `100000`): Max connections and threads. (Set to 0 for no limit)
        """

        Thread(
            target=self._serve,
            args=(ip, port),
        ).start()
