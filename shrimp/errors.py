__all__ = ("BadRequestStringError", "InvalidMethodError")


class BadRequestStringError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidMethodError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
