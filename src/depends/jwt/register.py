import typing

import fastapi

import src.app_state
import src.depends.token
import src.depends.app_state
import src.dto.jwt
import src.error
import src.error.error_type


def depends(
        scopes: typing.Optional[typing.List[str]] = []
) -> src.dto.jwt.Jwt:
    def dependency(
            token: str = src.depends.token.depends(),
            app_state: src.app_state.AppState = src.depends.app_state.depends()
    ) -> src.dto.jwt.Jwt:
        jwt = src.dto.jwt.Jwt()
        jwt.load_register(
            app_state.service.jwt.verify(
                token,
                app_state.service.jwt.verify_register_scopes + scopes,
                src.error.error_type.UNAUTHORIZED_REGISTER_TOKEN_INVALID,
                src.error.error_type.UNAUTHORIZED_REGISTER_TOKEN_ISSUER,
                src.error.error_type.UNAUTHORIZED_REGISTER_TOKEN_EXPIRED,
                src.error.error_type.UNAUTHORIZED_REGISTER_TOKEN_SCOPES,
                app_state.service.jwt.verify_default_options
            )
        )
        return jwt

    return fastapi.Depends(dependency)
