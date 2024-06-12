<div align="center">
<h1>🦐 Shrimp</h1>
<a href="#install-shrimp"><img src="https://img.shields.io/badge/Batteries_🔋-Included-yellow?labelColor=000000&style=for-the-badge"></a> <a href="#requirements"><img src="https://img.shields.io/badge/Python-3.10+-FFD43B?labelColor=306998&style=for-the-badge&logo=python&logoColor=white"></a> <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"></a>
</div>

**Shrimp** 🦐 is a batteries-included zero-dependency WSGI/ASGI web-framework for **Python** <img src="https://python.org/favicon.ico" alt="Python" height="12">

# Example

```py
from shrimp import Shrimp, Request
from shrimp.response import HTMLResponse

server = Shrimp()

@server.get("/")
def index(req: Request) -> HTMLResponse:
    return HTMLResponse("<h1>Hello, World!</h1>")

server.serve()
```

_Simple HTTP server using **Shrimp** 🦐_

# Requirements

- [**Python 3.10.x <img src="https://python.org/favicon.ico" alt="Python" height="12"> or above with `pip`**](https://python.org)

# Install Shrimp

To install **Shrimp** 🦐, run the following `pip` command.

```
$ pip install -U shrimp-http
```

**Shrimp** 🦐 is fully made with built-in packages. There's no dependencies, hence being batteries-included.
