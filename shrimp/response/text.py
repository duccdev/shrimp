from typing import Mapping
from shrimp.httpstatus import OK, HttpStatus
from shrimp.response import BaseResponse

__all__ = ("TextResponse",)


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
