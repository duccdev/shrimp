__all__ = ("Route",)

from typing import Callable
from .httpmethod import HttpMethod
from .request import Request
from .response import Response


class Route:
    def __init__(
        self,
        method: HttpMethod,
        path: str,
        handler: Callable[[Request], Response],
    ) -> None:
        """Creates a route

        Args:
            method (HttpMethod): HTTP method
            path (str): HTTP path
            handler (Callable[[Request], Response]): Request handler
        """

        self.method = method
        self.path = path
        self.handler = handler
