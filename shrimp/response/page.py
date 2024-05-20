from typing import Mapping
from shrimp.httpstatus import OK, HttpStatus
from shrimp.response import BaseResponse
from shrimp.ssr import Page

__all__ = ("PageResponse",)


class PageResponse(BaseResponse):
    def __init__(
        self,
        page: Page,
        status: HttpStatus = OK,
        headers: Mapping[str, str] = {},
    ) -> None:
        """Responds with an SSR page

        ## Arguments:
            `status` (`HttpStatus = OK`): The HTTP response status
            `headers` (`Mapping[str, str] = {}`): The HTTP response headers
            `page` (`Page`): Page to render and send
        """

        final_headers = dict(headers)
        final_headers["Content-Type"] = "text/html"

        super().__init__(status, final_headers, page.render())
