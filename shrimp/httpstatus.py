__all__ = ("OK", "NotFound", "ContentTooLarge")


class HttpStatus:
    def __init__(self, code: int, message: str) -> None:
        self.code = code
        self.message = message


OK = HttpStatus(200, "OK")
NotFound = HttpStatus(404, "Not Found")
ContentTooLarge = HttpStatus(413, "Content Too Large")
InternalServerError = HttpStatus(500, "Internal Server Error")
