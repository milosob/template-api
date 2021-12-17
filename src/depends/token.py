import typing

import fastapi

import src.depends.header
import src.error.error
import src.error.error_type


def depends(
        header: typing.Optional[str] = "authorization",
        scheme: typing.Optional[str] = "bearer"
) -> str:
    def dependency(
            value: str = src.depends.header.depends(header)
    ) -> str:
        if not value:
            raise src.error.error.Error(
                fastapi.status.HTTP_401_UNAUTHORIZED,
                src.error.error_type.UNAUTHORIZED_HEADER_MISSING
            )

        s, _, p = value.partition(" ")

        if scheme != s.lower():
            raise src.error.error.Error(
                fastapi.status.HTTP_401_UNAUTHORIZED,
                src.error.error_type.UNAUTHORIZED_HEADER_SCHEME
            )

        return p

    return fastapi.Depends(dependency)
