import typing

import fastapi

import src.app_state
import src.dto.jwt
import src.error


class PasswordRecover:
    scopes: typing.List[str]

    def __init__(
            self,
            scopes: typing.Optional[typing.List[str]] = ()
    ) -> None:
        self.scopes = list(set(scopes))

    def __call__(
            self,
            bearer_token: str = src.depends.bearer_token.depends(),
            app_state: src.app_state.AppState = src.depends.app_state.depends(),
    ) -> src.dto.jwt.JwtPasswordRecover:
        return src.dto.jwt.JwtPasswordRecover.from_json_dict(
            app_state.service.jwt.verify(
                bearer_token,
                self.scopes,
                src.error.error_type.UNAUTHORIZED_PASSWORD_RECOVER_TOKEN_INVALID,
                src.error.error_type.UNAUTHORIZED_PASSWORD_RECOVER_TOKEN_ISSUER,
                src.error.error_type.UNAUTHORIZED_PASSWORD_RECOVER_TOKEN_EXPIRED,
                src.error.error_type.UNAUTHORIZED_PASSWORD_RECOVER_TOKEN_SCOPES,
                app_state.service.jwt.verify_default_options,
            )["data"]
        )


def depends(
        scopes: typing.List[str]
) -> typing.Any:
    return fastapi.Depends(
        PasswordRecover(scopes)
    )
