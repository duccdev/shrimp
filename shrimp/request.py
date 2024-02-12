from ._parsers import parse_http_request
from .httpmethod import http_method_from_str
from .errors import BadRequestStringError

__all__ = ("Request",)


class Request:
    def __init__(self, reqstring: str) -> None:
        parsed_req = parse_http_request(reqstring.strip().splitlines()[0])

        if not parsed_req:
            raise BadRequestStringError(
                "A request was made but it had an invalid HTTP structure"
            )

        self.method = http_method_from_str(parsed_req[0])

        self.path = parsed_req[1]
