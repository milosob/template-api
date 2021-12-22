import typing

import fastapi

import src.app_state
import src.depends.token
import src.depends.app_state
import src.dto.account
import src.dto.jwt
import src.error
import src.error.error_type


def depends(
        scopes: typing.Optional[typing.List[str]] = []
) -> src.dto.jwt.Jwt:
    def dependency(
            app_state: src.app_state.AppState = src.depends.app_state.depends(),
            dto: src.dto.account.AccountPostAuthenticateRefreshIn = fastapi.Body(...)
    ) -> src.dto.jwt.Jwt:
        jwt = src.dto.jwt.Jwt()
        jwt.load_access(
            app_state.service.jwt.verify(
                dto.access_token,
                app_state.service.jwt.verify_access_scopes,
                src.error.error_type.UNAUTHORIZED_ACCESS_TOKEN_INVALID,
                src.error.error_type.UNAUTHORIZED_ACCESS_TOKEN_ISSUER,
                None,
                src.error.error_type.UNAUTHORIZED_ACCESS_TOKEN_SCOPES,
                app_state.service.jwt.verify_default_options
            )
        )
        jwt.load_refresh(
            app_state.service.jwt.verify(
                dto.refresh_token,
                app_state.service.jwt.verify_refresh_scopes + scopes,
                src.error.error_type.UNAUTHORIZED_REFRESH_TOKEN_INVALID,
                src.error.error_type.UNAUTHORIZED_REFRESH_TOKEN_ISSUER,
                src.error.error_type.UNAUTHORIZED_REFRESH_TOKEN_EXPIRED,
                src.error.error_type.UNAUTHORIZED_REFRESH_TOKEN_SCOPES,
                app_state.service.jwt.verify_refresh_options,
                dto.access_token
            )
        )
        return jwt

    return fastapi.Depends(dependency)
