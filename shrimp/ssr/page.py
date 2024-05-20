from .component import Component

__all__ = ("Page",)


class Page:
    def __init__(self, head: list[Component], body: list[Component], title: str | None = None) -> None:
        self.head = head
        self.body = body
        self.title = title

    def render(self) -> str:
        return f"<!DOCTYPE html><html><head>{'<title>' + self.title + '</title>' if self.title else ''}{''.join([comp.render() for comp in self.head])}</head><body>{"".join([comp.render() for comp in self.body])}</body></html>"
