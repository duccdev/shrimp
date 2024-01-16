from shrimp import Shrimp, Request
from shrimp.response import FileResponse


krill = Shrimp()


@krill.get("/")
def index(req: Request) -> FileResponse:
    return FileResponse("index.html")


krill.serve()
