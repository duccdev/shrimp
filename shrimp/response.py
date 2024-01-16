__all__ = ("Response",)

from typing import Mapping
from .httpstatus import HttpStatus


class Response:
    def __init__(
        self, status: HttpStatus, headers: Mapping[str, str], body: str
    ) -> None:
        self.status = status
        self.headers = headers
        self.body = body

    def raw(self) -> bytes:
        status_line = f"HTTP/1.1 {self.status.code} {self.status.message}"
        headers = "\r\n".join(
            [f"{name}: {self.headers[name]}" for name in self.headers]
        )

        return (f"{status_line}\r\n{headers}\r\n\r\n{self.body}").encode()
