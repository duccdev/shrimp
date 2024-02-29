import json
from os import PathLike
from typing import Mapping
from .httpstatus import OK, HttpStatus

__all__ = ("BaseResponse", "FileResponse")


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
        status_line = f"HTTP/1.1 {self.status.code} {self.status.message}"

        headers = "\r\n".join(
            [f"{name}: {self.headers[name]}" for name in self.headers]
        )

        appendix = f"\r\n\r\n{self.body}" if self.body is not None else ""

        return (f"{status_line}\r\n{headers}{appendix}").encode()


class FileResponse(BaseResponse):
    def __init__(
        self,
        filename: str | PathLike,
        mime_type: str = "text/html",
        status: HttpStatus = OK,
        headers: Mapping[str, str] = {},
        is_binary: bool = False,
    ) -> None:
        """Responds with a file

        ## Arguments:
            `filename` (`str | PathLike`): Path to the file you want to send
            `mime_type` (`str = "text/html"`): Mime-type of the data in the file
            `status` (`HttpStatus = OK`): The HTTP response status
            `headers` (`Mapping[str, str] = {}`): The HTTP response headers
            `is_binary` (`bool` = False`): Tells Python whether or not this is binary or text
        """

        final_headers = dict(headers)
        final_headers["Content-Type"] = mime_type

        with open(filename, "rb" if is_binary else "r") as fp:
            super().__init__(status, final_headers, fp.read())


class JSONResponse(BaseResponse):
    def __init__(
        self,
        body: dict | list | tuple | str | int | float,
        status: HttpStatus = OK,
        headers: Mapping[str, str] = {},
    ) -> None:
        """Responds with JSON

        ## Arguments:
            `status` (`HttpStatus = OK`): The HTTP response status
            `headers` (`Mapping[str, str] = {}`): The HTTP response headers
            `body` (`dict | list | tuple | str | int | float`): JSON data
        """

        final_headers = dict(headers)
        final_headers["Content-Type"] = "application/json"

        super().__init__(status, final_headers, json.dumps(body))


class TextResponse(BaseResponse):
    def __init__(
        self,
        body: str,
        status: HttpStatus = OK,
        headers: Mapping[str, str] = {},
    ) -> None:
        """Responds with text

        ## Arguments:
            `status` (`HttpStatus = OK`): The HTTP response status
            `headers` (`Mapping[str, str] = {}`): The HTTP response headers
            `body` (`str`): Text content to send
        """

        final_headers = dict(headers)
        final_headers["Content-Type"] = "text/plain"

        super().__init__(status, final_headers, body)


class HTMLResponse(BaseResponse):
    def __init__(
        self,
        body: str,
        status: HttpStatus = OK,
        headers: Mapping[str, str] = {},
    ) -> None:
        """Responds with HTML

        ## Arguments:
            `status` (`HttpStatus = OK`): The HTTP response status
            `headers` (`Mapping[str, str] = {}`): The HTTP response headers
            `body` (`str`): HTML content to send
        """

        final_headers = dict(headers)
        final_headers["Content-Type"] = "text/html"

        super().__init__(status, final_headers, body)
