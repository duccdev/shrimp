import json
from typing import Mapping
from shrimp.httpstatus import OK, HttpStatus
from shrimp.response import BaseResponse

__all__ = ("JSONResponse",)


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
