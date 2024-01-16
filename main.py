import shrimp
from shrimp import httpstatus


krill = shrimp.Shrimp()


@krill.get("/")
def index(req: shrimp.Request) -> shrimp.Response:
    return shrimp.Response(
        httpstatus.OK,
        {"Content-Type": "text/html"},
        f"<h1>{req.method} {req.path}</div>",
    )


krill.serve()
