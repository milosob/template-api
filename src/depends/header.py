import typing

import fastapi


def depends(
        header: str,
        default: typing.Any = ...
) -> str:
    return fastapi.Header(default, alias=header)
