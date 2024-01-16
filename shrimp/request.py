from ._parsers import parse_http_request
from .httpmethod import HttpMethod
from .errors import BadRequestStringError, InvalidMethodError

__all__ = ("Request",)


class Request:
    def __init__(self, reqstring: str) -> None:
        parsed_req = parse_http_request(reqstring.strip().splitlines()[0])

        if not parsed_req:
            raise BadRequestStringError(
                "A request was made but it had an invalid HTTP structure"
            )

        match parsed_req[0]:
            case "GET":
                self.method = HttpMethod.GET

            case _:
                raise InvalidMethodError(f"Invalid request method {parsed_req[0]}")

        self.path = parsed_req[1]
