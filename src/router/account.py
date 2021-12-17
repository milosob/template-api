import asyncio
import hmac
import os

import fastapi
import fastapi.security

import src.app_state
import src.database.account.filter
import src.database.account.update
import src.database.account.model
import src.depends.app_state
import src.depends.bearer_token
import src.depends.jwt.password_recover
import src.dto.account
import src.dto.error
import src.dto.jwt
import src.error.error
import src.error.error_type

router = fastapi.APIRouter(
    prefix="/account",
    tags=["account"]
)

error_responses: dict = {
    fastapi.status.HTTP_400_BAD_REQUEST: {
        "model": src.dto.error.ErrorApiOut,
        "description": "Error."
    },
    fastapi.status.HTTP_401_UNAUTHORIZED: {
        "model": src.dto.error.ErrorApiOut,
        "description": "Error."
    },
    fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": src.dto.error.ErrorApiOut,
        "description": "Error."
    },
    fastapi.status.HTTP_503_SERVICE_UNAVAILABLE: {
        "model": src.dto.error.ErrorApiOut,
        "description": "Error."
    }
}


@router.post(
    path="/register",
    summary="Account register.",
    status_code=fastapi.status.HTTP_201_CREATED,
    responses=error_responses | {
        fastapi.status.HTTP_201_CREATED: {
            "model": src.dto.account.AccountPostRegisterOut,
            "description": "Resource created."
        },
    }
)
async def account_post_register(
        request: fastapi.Request,
        app_state: src.app_state.AppState = src.depends.app_state.depends(),
        account_post_register_in: src.dto.account.AccountPostRegisterIn = fastapi.Body(
            ...
        )
):
    account: src.database.account.model.Account
    account = app_state.database.account.find_one(
        src.database.account.filter.emails(
            [account_post_register_in.username]
        )
    )

    if account:
        raise src.error.error.Error(
            fastapi.status.HTTP_400_BAD_REQUEST,
            src.error.error_type.ACCOUNT_REGISTER_USERNAME_TAKEN
        )

    account = src.database.account.model.Account()

    account_email: src.database.account.model.AccountEmail
    account_email = src.database.account.model.AccountEmail()
    account_email.value = account_post_register_in.username
    account_email.primary = True
    account_email.confirmed = False

    account.emails.append(
        account_email
    )

    account.authentication.passwords.primary.value = app_state.service.password.password_hash(
        account_post_register_in.password
    )

    account_inserted: src.database.account.model.Account
    account_inserted = app_state.database.account.insert_one(
        account
    )

    if not account_inserted:
        raise src.error.error.Error(
            fastapi.status.HTTP_400_BAD_REQUEST,
            src.error.error_type.ACCOUNT_REGISTER_USERNAME_TAKEN
        )

    account = account_inserted

    sub: str
    sub = account.identifier
    data: dict
    data = {}

    account_register_token: str
    account_register_token = app_state.service.jwt.issue(
        sub,
        data,
        app_state.service.jwt.lifetime_account_register,
        ["type:account-register-confirm"]
    )

    try:
        await app_state.service.mail.send_template(
            {next(email for email in account.emails if email.primary).value: ""},
            None,
            None,
            app_state.service.locale.by_request(request),
            app_state.service.template.mail_account_register,
            token=account_register_token
        )
    except Exception:
        raise src.error.error.Error(
            fastapi.status.HTTP_503_SERVICE_UNAVAILABLE,
            src.error.error_type.SERVICE_UNAVAILABLE_MAIL_ACCOUNT_REGISTER_CONFIRM
        )

    return src.dto.account.AccountPostRegisterOut(
        username=account_post_register_in.username,
        password=None
    )


@router.post(
    path="/register/confirm",
    summary="Account register.",
    status_code=fastapi.status.HTTP_201_CREATED,
    responses=error_responses | {
        fastapi.status.HTTP_201_CREATED: {
            "model": src.dto.account.AccountPostRegisterConfirmOut,
            "description": "Resource created."
        }
    }
)
async def account_post_register_confirm(
        request: fastapi.Request,
        app_state: src.app_state.AppState = src.depends.app_state.depends(),
        account_register_confirm_token: str = src.depends.bearer_token.depends(),
        account_register_confirm_in: src.dto.account.AccountPostRegisterConfirmIn = fastapi.Body(
            ...
        )
):
    payload: dict
    payload = app_state.service.jwt.verify(
        account_register_confirm_token,
        ["type:account-register-confirm"],
        src.error.error_type.UNAUTHORIZED_ACCOUNT_REGISTER_CONFIRM_TOKEN_INVALID,
        src.error.error_type.UNAUTHORIZED_ACCOUNT_REGISTER_CONFIRM_TOKEN_ISSUER,
        src.error.error_type.UNAUTHORIZED_ACCOUNT_REGISTER_CONFIRM_TOKEN_EXPIRED,
        src.error.error_type.UNAUTHORIZED_ACCOUNT_REGISTER_CONFIRM_TOKEN_SCOPES,
        app_state.service.jwt.verify_default_options,
    )

    sub: str
    sub = payload["sub"]

    account: src.database.account.model.Account
    account = app_state.database.account.find_one(
        src.database.account.filter.identifier(
            sub
        )
    )

    if account.verification.email:
        return src.dto.account.AccountPostRegisterConfirmOut()

    account.verification.email = True

    account_email_primary: src.database.account.model.AccountEmail
    account_email_primary = next((email for email in account.emails if email.primary), None)

    if not account_email_primary:
        raise src.error.error.Error(
            fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
            src.error.error_type.INTERNAL_SERVER_ERROR
        )

    account_email_primary.confirmed = True

    if not app_state.database.account.update_one(
            account,
            {
                "$set": (
                        src.database.account.update.verification,
                        src.database.account.update.emails
                )
            }
    ):
        raise src.error.error.Error(
            fastapi.status.HTTP_503_SERVICE_UNAVAILABLE,
            src.error.error_type.SERVICE_UNAVAILABLE
        )

    return src.dto.account.AccountPostRegisterConfirmOut()


@router.post(
    path="/authenticate",
    summary="Account authenticate.",
    status_code=fastapi.status.HTTP_200_OK,
    responses=error_responses | {
        fastapi.status.HTTP_200_OK: {
            "model": src.dto.account.AccountPostAuthenticateOut,
            "description": "Operation successful."
        }
    }
)
async def account_post_authenticate(
        request: fastapi.Request,
        app_state: src.app_state.AppState = src.depends.app_state.depends(),
        account_post_authenticate_in: src.dto.account.AccountPostAuthenticateIn = fastapi.Body(
            ...
        )
):
    account: src.database.account.model.Account
    account = app_state.database.account.find_one(
        src.database.account.filter.emails(
            [account_post_authenticate_in.username]
        )
    )

    if not account:
        raise src.error.error.Error(
            fastapi.status.HTTP_401_UNAUTHORIZED,
            src.error.error_type.UNAUTHORIZED_ACCOUNT_AUTHENTICATE_CREDENTIALS_INVALID
        )

    if not app_state.service.password.password_verify(
            account_post_authenticate_in.password,
            account.authentication.passwords.primary.value
    ):
        raise src.error.error.Error(
            fastapi.status.HTTP_401_UNAUTHORIZED,
            src.error.error_type.UNAUTHORIZED_ACCOUNT_AUTHENTICATE_CREDENTIALS_INVALID
        )

    sub: str
    sub = account.identifier
    data: dict
    data = {}

    access_token: str
    access_token = app_state.service.jwt.issue(
        sub,
        data,
        app_state.service.jwt.lifetime_access,
        ["type:access"]
    )
    refresh_token: str
    refresh_token = app_state.service.jwt.issue(
        sub,
        data,
        app_state.service.jwt.lifetime_refresh,
        ["type:refresh"],
        access_token
    )

    return src.dto.account.AccountPostAuthenticateOut(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post(
    path="/authenticate/refresh",
    summary="Account authenticate refresh.",
    status_code=fastapi.status.HTTP_200_OK,
    responses=error_responses | {
        fastapi.status.HTTP_200_OK: {
            "model": src.dto.account.AccountPostAuthenticateRefreshOut,
            "description": "Operation successful."
        }
    }
)
async def account_post_authenticate_refresh(
        request: fastapi.Request,
        app_state: src.app_state.AppState = src.depends.app_state.depends(),
        account_post_authenticate_refresh_in: src.dto.account.AccountPostAuthenticateRefreshIn = fastapi.Body(
            ...
        )
):
    access_token_payload: dict
    access_token_payload = app_state.service.jwt.verify(
        account_post_authenticate_refresh_in.access_token,
        ["type:access"],
        src.error.error_type.UNAUTHORIZED_ACCESS_TOKEN_INVALID,
        src.error.error_type.UNAUTHORIZED_ACCESS_TOKEN_ISSUER,
        None,
        src.error.error_type.UNAUTHORIZED_ACCESS_TOKEN_SCOPES,
        app_state.service.jwt.verify_default_options
    )

    refresh_token_payload: dict
    refresh_token_payload = app_state.service.jwt.verify(
        account_post_authenticate_refresh_in.refresh_token,
        ["type:refresh"],
        src.error.error_type.UNAUTHORIZED_REFRESH_TOKEN_INVALID,
        src.error.error_type.UNAUTHORIZED_REFRESH_TOKEN_ISSUER,
        src.error.error_type.UNAUTHORIZED_REFRESH_TOKEN_EXPIRED,
        src.error.error_type.UNAUTHORIZED_REFRESH_TOKEN_SCOPES,
        app_state.service.jwt.verify_refresh_options,
        account_post_authenticate_refresh_in.access_token
    )

    sub: str
    sub = refresh_token_payload["sub"]
    data: dict
    data = refresh_token_payload["data"]

    # TODO
    #  After token verification update token data based on current db state.

    access_token: str
    access_token = app_state.service.jwt.issue(
        sub,
        data,
        app_state.service.jwt.lifetime_access,
        access_token_payload["scopes"]
    )
    refresh_token: str
    refresh_token = app_state.service.jwt.issue(
        sub,
        data,
        app_state.service.jwt.lifetime_refresh,
        ["type:refresh"],
        access_token
    )

    return src.dto.account.AccountPostAuthenticateRefreshOut(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post(
    path="/password/forget",
    summary="Account password forget.",
    status_code=fastapi.status.HTTP_200_OK,
    responses=error_responses | {
        fastapi.status.HTTP_200_OK: {
            "model": src.dto.account.AccountPostPasswordForgetOut,
            "description": "Operation successful."
        }
    }
)
async def account_post_password_forget(
        request: fastapi.Request,
        app_state: src.app_state.AppState = src.depends.app_state.depends(),
        account_post_password_forget_in: src.dto.account.AccountPostPasswordForgetIn = fastapi.Body(
            ...
        )
):
    account: src.database.account.model.Account
    account = app_state.database.account.find_one(
        src.database.account.filter.emails(
            [account_post_password_forget_in.username]
        )
    )

    if not account:
        await asyncio.sleep(2)
        return src.dto.account.AccountPostPasswordForgetOut()

    old_password: str
    old_password = account.authentication.passwords.primary.value

    jwt_password_recover: src.dto.jwt.JwtPasswordRecover
    jwt_password_recover = src.dto.jwt.JwtPasswordRecover(
        account.identifier
    )

    jwt_password_recover.sign(
        old_password
    )

    password_recover_token: str
    password_recover_token = app_state.service.jwt.issue(
        account.identifier,
        jwt_password_recover.to_json_dict(),
        app_state.service.jwt.lifetime_password_recover,
        ["type:account-password-recover"]
    )

    try:
        await app_state.service.mail.send_template(
            {next(email for email in account.emails if email.primary).value: ""},
            None,
            None,
            app_state.service.locale.by_request(request),
            app_state.service.template.mail_account_password_recover,
            token=password_recover_token
        )
    except Exception:
        raise src.error.error.Error(
            fastapi.status.HTTP_503_SERVICE_UNAVAILABLE,
            src.error.error_type.SERVICE_UNAVAILABLE_MAIL_ACCOUNT_PASSWORD_RECOVER
        )

    return src.dto.account.AccountPostPasswordForgetOut()


@router.post(
    path="/password/recover",
    summary="Account password recover.",
    status_code=fastapi.status.HTTP_200_OK,
    responses=error_responses | {
        fastapi.status.HTTP_200_OK: {
            "model": src.dto.account.AccountPostPasswordRecoverOut,
            "description": "Operation successful."
        }
    }
)
async def account_post_password_recover(
        jwt_password_recover: src.dto.jwt.JwtPasswordRecover = src.depends.jwt.password_recover.depends(
            ["type:account-password-recover"]
        ),
        app_state: src.app_state.AppState = src.depends.app_state.depends(),
        account_post_password_recover_in: src.dto.account.AccountPostPasswordRecoverIn = fastapi.Body(...)
):
    account: src.database.account.model.Account
    account = app_state.database.account.find_one(
        src.database.account.filter.identifier(
            jwt_password_recover.identifier
        )
    )

    if not account:
        raise src.error.error.Error(
            fastapi.status.HTTP_401_UNAUTHORIZED,
            src.error.error_type.UNAUTHORIZED_PASSWORD_RECOVER_TOKEN_INVALID
        )

    old_password: str
    old_password = account.authentication.passwords.primary.value

    if not jwt_password_recover.verify(
            old_password
    ):
        raise src.error.error.Error(
            fastapi.status.HTTP_401_UNAUTHORIZED,
            src.error.error_type.UNAUTHORIZED_PASSWORD_RECOVER_TOKEN_EXPIRED
        )

    new_password: str

    while True:
        new_password = app_state.service.password.password_hash(
            account_post_password_recover_in.password
        )

        if not hmac.compare_digest(old_password, new_password):
            break

    account.authentication.passwords.primary.value = new_password

    if not app_state.database.account.update_one(
            account,
            {
                "$set": (
                        src.database.account.update.authentication_passwords_primary
                )
            }
    ):
        raise src.error.error.Error(
            fastapi.status.HTTP_503_SERVICE_UNAVAILABLE,
            src.error.error_type.SERVICE_UNAVAILABLE
        )

    return src.dto.account.AccountPostPasswordRecoverOut(
        password=None
    )
