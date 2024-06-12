from typing import Coroutine, Any


async def maybe_coroutine(value: Any | Coroutine) -> Any | None:
    """An async function to await a coroutine value and return it or return the value if it's not a coroutine

    ## Arguments:
        `value` (`Any | Coroutine`): Any value or a coroutine

    ## Returns:
        `Any | None`: Any if the coroutine/value has a value or none if no value
    """

    if isinstance(value, Coroutine):
        return await value

    return value
