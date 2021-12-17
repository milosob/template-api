import typing

import fastapi

import src.app_state
import src.depends.app_state
import src.dto.account
import src.dto.jwt
import src.error.error_type


class Refresh:
    scopes: typing.List[str]

    def __init__(
            self,
            scopes: typing.List[str]
    ) -> None:
        self.scopes = scopes

    def __call__(
            self,
            app_state: src.app_state.AppState = src.depends.app_state.depends(),
            account_post_authenticate_refresh_in: src.dto.account.AccountPostAuthenticateRefreshIn = fastapi.Body(...)
    ) -> src.dto.jwt.Jwt:
        jwt = src.dto.jwt.Jwt()
        jwt.load_access(
            app_state.service.jwt.verify(
                account_post_authenticate_refresh_in.access_token,
                ["type:access"],
                src.error.error_type.UNAUTHORIZED_ACCESS_TOKEN_INVALID,
                src.error.error_type.UNAUTHORIZED_ACCESS_TOKEN_ISSUER,
                None,
                src.error.error_type.UNAUTHORIZED_ACCESS_TOKEN_SCOPES,
                app_state.service.jwt.verify_default_options
            )
        )
        jwt.load_refresh(
            app_state.service.jwt.verify(
                account_post_authenticate_refresh_in.refresh_token,
                ["type:refresh"] + self.scopes,
                src.error.error_type.UNAUTHORIZED_REFRESH_TOKEN_INVALID,
                src.error.error_type.UNAUTHORIZED_REFRESH_TOKEN_ISSUER,
                src.error.error_type.UNAUTHORIZED_REFRESH_TOKEN_EXPIRED,
                src.error.error_type.UNAUTHORIZED_REFRESH_TOKEN_SCOPES,
                app_state.service.jwt.verify_refresh_options,
                account_post_authenticate_refresh_in.access_token
            )
        )
        return jwt


def depends(
        scopes: typing.Optional[typing.List[str]] = None
) -> typing.Any:
    return fastapi.Depends(
        Refresh(scopes if scopes else [])
    )
