import typing

import fastapi

import src.error.error
import src.error.error_type


class Token:
    header: str
    scheme: str

    def __init__(
            self,
            header: str,
            scheme: str
    ) -> None:
        self.header = header.lower()
        self.scheme = scheme.lower()

    def __call__(
            self,
            request: fastapi.Request
    ) -> str:
        header: str
        header = request.headers.get(self.header)

        if not header:
            raise src.error.error.Error(
                fastapi.status.HTTP_401_UNAUTHORIZED,
                src.error.error_type.UNAUTHORIZED_HEADER_MISSING
            )

        scheme, _, parameter = header.partition(" ")

        if scheme.lower() != self.scheme:
            raise src.error.error.Error(
                fastapi.status.HTTP_401_UNAUTHORIZED,
                src.error.error_type.UNAUTHORIZED_HEADER_SCHEME
            )

        return parameter


def depends(
        header: typing.Optional[str] = "authorization",
        scheme: typing.Optional[str] = "bearer"
) -> typing.Any:
    return fastapi.Depends(
        Token(header, scheme)
    )
