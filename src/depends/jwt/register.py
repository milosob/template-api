import typing

import fastapi

import src.app_state
import src.depends.token
import src.depends.app_state
import src.dto.jwt
import src.error


class Register:
    scopes: typing.List[str]

    def __init__(
            self,
            scopes: typing.List[str]
    ) -> None:
        self.scopes = scopes

    def __call__(
            self,
            token: str = src.depends.token.depends(),
            app_state: src.app_state.AppState = src.depends.app_state.depends(),
    ) -> src.dto.jwt.Jwt:
        jwt = src.dto.jwt.Jwt()
        jwt.load_register(
            app_state.service.jwt.verify(
                token,
                ["type:register"] + self.scopes,
                src.error.error_type.UNAUTHORIZED_ACCOUNT_REGISTER_CONFIRM_TOKEN_INVALID,
                src.error.error_type.UNAUTHORIZED_ACCOUNT_REGISTER_CONFIRM_TOKEN_ISSUER,
                src.error.error_type.UNAUTHORIZED_ACCOUNT_REGISTER_CONFIRM_TOKEN_EXPIRED,
                src.error.error_type.UNAUTHORIZED_ACCOUNT_REGISTER_CONFIRM_TOKEN_SCOPES,
                app_state.service.jwt.verify_default_options,
            )
        )
        return jwt


def depends(
        scopes: typing.Optional[typing.List[str]] = None
) -> typing.Any:
    return fastapi.Depends(
        Register(scopes if scopes else [])
    )
