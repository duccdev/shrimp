from typing import Mapping
from shrimp.httpstatus import OK, HttpStatus
from shrimp.response import BaseResponse

__all__ = ("HTMLResponse",)


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
