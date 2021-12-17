import typing

import fastapi

import src.app_state
import src.depends.token
import src.depends.app_state
import src.dto.account
import src.dto.jwt
import src.error.error_type


class Access:
    scopes: typing.List[str]

    def __init__(
            self,
            scopes: typing.List[str]
    ) -> None:
        self.scopes = scopes

    def __call__(
            self,
            token: str = src.depends.token.depends(),
            app_state: src.app_state.AppState = src.depends.app_state.depends()
    ) -> src.dto.jwt.Jwt:
        jwt = src.dto.jwt.Jwt()
        jwt.load_access(
            app_state.service.jwt.verify(
                token,
                ["type:access"] + self.scopes,
                src.error.error_type.UNAUTHORIZED_ACCESS_TOKEN_INVALID,
                src.error.error_type.UNAUTHORIZED_ACCESS_TOKEN_ISSUER,
                src.error.error_type.UNAUTHORIZED_ACCESS_TOKEN_EXPIRED,
                src.error.error_type.UNAUTHORIZED_ACCESS_TOKEN_SCOPES,
                app_state.service.jwt.verify_default_options
            )
        )
        return jwt


def depends(
        scopes: typing.Optional[typing.List[str]] = None
) -> typing.Any:
    return fastapi.Depends(
        Access(scopes if scopes else [])
    )