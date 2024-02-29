import asyncio
from typing import Callable, Coroutine, Any


async def maybe_coroutine(func: Callable | Coroutine, *args, **kwargs) -> Any | None:
    """An async function that can await another function or result or run sync functions

    ## Arguments:
        `func` (`Callable | Coroutine`): The function or coroutine to await or run
        `*args` and `**kwargs`: To be passed to the function

    ## Returns:
        `Any | None`: Any if the function/coroutine has a value or none if no value
    """

    if isinstance(func, Callable):
        if asyncio.iscoroutinefunction(func):
            return await func(*args, **kwargs)

        return func(*args, **kwargs)

    return await func
