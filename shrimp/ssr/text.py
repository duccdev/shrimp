from .component import Component
from .color import Color

__all__ = ("Text",)


class Text(Component):
    def __init__(
        self, content: str, font_size: int = 16, color: str | int | None = None
    ) -> None:
        self._content = content
        self._font_size = font_size
        self._color = color

    def render(self) -> str:
        return f"<p style='font-size: {self._font_size}px; color: {Color(self._color).value if self._color else 'black'};'>{self._content}</p>"
