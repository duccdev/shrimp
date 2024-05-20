from os import PathLike
from typing import Mapping
from shrimp.httpstatus import OK, HttpStatus
from shrimp.response import BaseResponse

__all__ = ("FileResponse",)


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
