import asyncio, typing


async def maybe_coroutine(func: typing.Callable, *args, **kwargs):
    if asyncio.iscoroutine(func):
        return await func
    elif asyncio.iscoroutinefunction(func):
        return await func(*args, **kwargs)
    else:
        return func(*args, **kwargs)
