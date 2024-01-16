__all__ = ("OK", "NotFound")


class HttpStatus:
    def __init__(self, code: int, message: str) -> None:
        self.code = code
        self.message = message


OK = HttpStatus(200, "OK")
NotFound = HttpStatus(404, "Not Found")
