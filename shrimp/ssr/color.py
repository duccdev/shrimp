import re

__all__ = ("Color",)


class Color:
    def __init__(self, value: str | int) -> None:
        if isinstance(value, str):
            if not bool(re.match(r"^#(?:[0-9a-fA-F]{3}){1,2}$", value)):
                raise ValueError(
                    f"Invalid color value passed in, expected #RRGGBB or rgb(r, g, b) but got {value}"
                )

            self.value = value
            return

        if isinstance(value, int):
            if not (0 <= value <= 0xFFFFFF):
                raise ValueError(
                    "Invalid color value passed in, expected range 0 to 0xFFFFFF (16777215) but got {value}"
                )

            self.value = f"#{value:06X}"
            return
