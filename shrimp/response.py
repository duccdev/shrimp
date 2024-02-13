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
        self.status = status
        self.headers = headers
        self.body = body

    def _raw(self) -> bytes:
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
        final_headers = dict(headers)
        final_headers["Content-Type"] = "text/html"

        super().__init__(status, final_headers, body)
