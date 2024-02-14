<!-- MIT LICENSE -->
<!--
MIT License                                                
Copyright (c) 2023-present krillissue                                                                                 Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal                                         in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell                                             copies of the Software, and to permit persons to whom the Software is                                                 furnished to do so, subject to the following conditions:                                                              The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.                                                                       THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
-->

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
*Simple HTTP server using **Shrimp** 🦐*

# Requirements
- [**Python 3.10.x <img src="https://python.org/favicon.ico" alt="Python" height="12"> or above with `pip`**](https://python.org)

To install **Python <img src="https://python.org/favicon.ico" alt="Python" height="12">** with `pip`, check [this file](INSTALL%20PYTHON.md).

# Install Shrimp
To install **Shrimp** 🦐, run the following `pip` command.

```
$ pip install -U shrimp-http
```

**Shrimp** 🦐 is fully made with built-in packages. There's no dependencies, hence being batteries-included.
