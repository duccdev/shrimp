from typing import Callable
from .httpmethod import HttpMethod
from .request import Request
from .response import BaseResponse

__all__ = ("Route",)


class Route:
    def __init__(
        self,
        method: HttpMethod,
        path: str,
        handler: Callable[[Request], BaseResponse],
    ) -> None:
        """Creates a route

        Args:
            method (HttpMethod): HTTP method
            path (str): HTTP path
            handler (Callable[[Request], BaseResponse]): Request handler
        """

        self.method = method
        self.path = path
        self.handler = handler
