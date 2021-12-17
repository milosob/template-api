import typing

import fastapi

import src.app_state
import src.dto.account
import src.dto.jwt
import src.error


class Refresh:

    def __call__(
            self,
            app_state: src.app_state.AppState = src.depends.app_state.depends(),
            account_post_authenticate_refresh_in: src.dto.account.AccountPostAuthenticateRefreshIn = fastapi.Body(...)
    ) -> typing.Tuple[src.dto.jwt.JwtAccess, src.dto.jwt.JwtRefresh]:
        return src.dto.jwt.JwtAccess.from_json_dict(
            app_state.service.jwt.verify(
                account_post_authenticate_refresh_in.access_token,
                ["type:access"],
                src.error.error_type.UNAUTHORIZED_ACCESS_TOKEN_INVALID,
                src.error.error_type.UNAUTHORIZED_ACCESS_TOKEN_ISSUER,
                None,
                src.error.error_type.UNAUTHORIZED_ACCESS_TOKEN_SCOPES,
                app_state.service.jwt.verify_default_options
            )["data"]
        ), src.dto.jwt.JwtRefresh.from_json_dict(
            app_state.service.jwt.verify(
                account_post_authenticate_refresh_in.refresh_token,
                ["type:refresh"],
                src.error.error_type.UNAUTHORIZED_REFRESH_TOKEN_INVALID,
                src.error.error_type.UNAUTHORIZED_REFRESH_TOKEN_ISSUER,
                src.error.error_type.UNAUTHORIZED_REFRESH_TOKEN_EXPIRED,
                src.error.error_type.UNAUTHORIZED_REFRESH_TOKEN_SCOPES,
                app_state.service.jwt.verify_refresh_options,
                account_post_authenticate_refresh_in.access_token
            )["data"]
        )


def depends() -> typing.Any:
    return fastapi.Depends(
        Refresh()
    )
