import typing

import fastapi

import src.error.error
import src.error.error_type


class BearerToken:

    def __init__(
            self
    ) -> None:
        pass

    def __call__(
            self,
            request: fastapi.Request
    ) -> str:
        authorization: str
        authorization = request.headers.get("authorization")

        if not authorization:
            raise src.error.error.Error(
                code=fastapi.status.HTTP_401_UNAUTHORIZED,
                type=src.error.error_type.UNAUTHORIZED_HEADER_MISSING
            )

        scheme, _, parameter = authorization.partition(" ")

        if scheme.lower() != "bearer":
            raise src.error.error.Error(
                code=fastapi.status.HTTP_401_UNAUTHORIZED,
                type=src.error.error_type.UNAUTHORIZED_HEADER_SCHEME
            )

        return parameter


def depends() -> typing.Any:
    return fastapi.Depends(
        BearerToken()
    )
