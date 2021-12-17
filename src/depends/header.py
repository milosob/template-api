import typing

import fastapi


def depends(
        header: str,
        default: typing.Any = ...
) -> typing.Any:
    return fastapi.Header(default, alias=header)
