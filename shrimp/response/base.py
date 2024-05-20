from typing import Mapping
from shrimp.httpstatus import OK, HttpStatus

__all__ = ("BaseResponse",)


class BaseResponse:
    def __init__(
        self,
        status: HttpStatus = OK,
        headers: Mapping[str, str] = {},
        body: str | bytes | None = None,
    ) -> None:
        """The base response class that all other responses derive from

        ## Arguments:
            `status` (`HttpStatus = OK`): The HTTP response status
            `headers` (`Mapping[str, str] = {}`): The HTTP response headers
            `body` (`body: str | bytes | None = None`): The HTTP response body
        """

        self.status = status
        self.headers = headers
        self.body = body

    def _raw(self) -> bytes:
        """Converts the response into a HTTP response string in bytes

        ## Returns:
            `bytes`: HTTP response string in bytes
        """
        crlf = "\r\n"

        status_line = f"HTTP/1.1 {self.status.code} {self.status.message}"
        headers = (
            "\r\n".join([f"{name}: {self.headers[name]}" for name in self.headers])
            + f"{crlf}Content-Length: {len(self.body) if self.body else 0}"
        )
        appendix = f"{crlf}{crlf}{self.body}" if self.body else ""

        return (f"{status_line}{crlf}{headers}{appendix}").encode()
