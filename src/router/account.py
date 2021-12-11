import asyncio
import hmac
import os

import fastapi
import fastapi.security

import src.app_state
import src.database.error.error_conflict
import src.database.error.error_not_found
import src.database.account.driver_base
import src.database.account.model
import src.depends.bearer_token
import src.depends.app_state
import src.dto.account
import src.dto.error
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
        account_register_in: src.dto.account.AccountPostRegisterIn = fastapi.Body(
            ...
        )
):
    account: src.database.account.model.Account
    account = await app_state.database.account.find_one_by_email(
        email=account_register_in.username
    )

    if account:
        raise src.error.error.Error(
            code=fastapi.status.HTTP_400_BAD_REQUEST,
            type=src.error.error_type.ACCOUNT_REGISTER_USERNAME_TAKEN
        )

    account = src.database.account.model.Account()

    account.email.primary.value = account_register_in.username
    account.email.primary.confirmed = False
    account.email.records.append(
        account.email.primary
    )

    account.authentication.password.primary.value = app_state.service.password.password_hash(
        password=account_register_in.password
    )

    if not await app_state.database.account.insert_one(
            model=account
    ):
        raise src.error.error.Error(
            code=fastapi.status.HTTP_400_BAD_REQUEST,
            type=src.error.error_type.ACCOUNT_REGISTER_USERNAME_TAKEN
        )

    sub: str
    sub = account.identifier
    data: dict
    data = {}

    account_register_token: str
    account_register_token = app_state.service.jwt.issue(
        sub=sub,
        data=data,
        lifetime=app_state.service.jwt.lifetime_account_register,
        scopes=["type:account-register-confirm"]
    )

    try:
        await app_state.service.mail.send_template(
            to={account.email.primary.value: ""},
            locale=app_state.service.locale.by_request(request),
            template=app_state.service.template.mail_account_register,
            token=account_register_token
        )
    except Exception:
        raise src.error.error.Error(
            code=fastapi.status.HTTP_503_SERVICE_UNAVAILABLE,
            type=src.error.error_type.SERVICE_UNAVAILABLE_MAIL_ACCOUNT_REGISTER_CONFIRM
        )

    return src.dto.account.AccountPostRegisterOut(
        username=account_register_in.username,
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
        token=account_register_confirm_token,
        required_scopes=["type:account-register-confirm"],
        verify_token_error_type=src.error.error_type.UNAUTHORIZED_ACCOUNT_REGISTER_CONFIRM_TOKEN_INVALID,
        verify_iss_error_type=src.error.error_type.UNAUTHORIZED_ACCOUNT_REGISTER_CONFIRM_TOKEN_ISSUER,
        verify_exp_error_type=src.error.error_type.UNAUTHORIZED_ACCOUNT_REGISTER_CONFIRM_TOKEN_EXPIRED,
        verify_scopes_error_type=src.error.error_type.UNAUTHORIZED_ACCOUNT_REGISTER_CONFIRM_TOKEN_SCOPES,
        options=app_state.service.jwt.verify_default_options,
    )

    sub: str
    sub = payload["sub"]

    # TODO

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
    account = await app_state.database.account.find_one_by_email(
        email=account_post_authenticate_in.username
    )

    if not account:
        raise src.error.error.Error(
            code=fastapi.status.HTTP_401_UNAUTHORIZED,
            type=src.error.error_type.UNAUTHORIZED_ACCOUNT_AUTHENTICATE_CREDENTIALS_INVALID
        )

    if not app_state.service.password.password_verify(
            password=account_post_authenticate_in.password,
            password_hash=account.authentication.password.primary.value
    ):
        raise src.error.error.Error(
            code=fastapi.status.HTTP_401_UNAUTHORIZED,
            type=src.error.error_type.UNAUTHORIZED_ACCOUNT_AUTHENTICATE_CREDENTIALS_INVALID
        )

    sub: str
    sub = account.identifier
    data: dict
    data = {}

    access_token: str
    access_token = app_state.service.jwt.issue(
        sub=sub,
        data=data,
        lifetime=app_state.service.jwt.lifetime_access,
        scopes=["type:access"]
    )
    refresh_token: str
    refresh_token = app_state.service.jwt.issue(
        sub=sub,
        data=data,
        lifetime=app_state.service.jwt.lifetime_refresh,
        scopes=["type:refresh"],
        access_token=access_token
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
        token=account_post_authenticate_refresh_in.access_token,
        required_scopes=["type:access"],
        verify_token_error_type=src.error.error_type.UNAUTHORIZED_ACCESS_TOKEN_INVALID,
        verify_iss_error_type=src.error.error_type.UNAUTHORIZED_ACCESS_TOKEN_ISSUER,
        verify_exp_error_type=None,
        verify_scopes_error_type=src.error.error_type.UNAUTHORIZED_ACCESS_TOKEN_SCOPES,
        options=app_state.service.jwt.verify_default_options
    )

    refresh_token_payload: dict
    refresh_token_payload = app_state.service.jwt.verify(
        token=account_post_authenticate_refresh_in.refresh_token,
        required_scopes=["type:refresh"],
        verify_token_error_type=src.error.error_type.UNAUTHORIZED_REFRESH_TOKEN_INVALID,
        verify_iss_error_type=src.error.error_type.UNAUTHORIZED_REFRESH_TOKEN_ISSUER,
        verify_exp_error_type=src.error.error_type.UNAUTHORIZED_REFRESH_TOKEN_EXPIRED,
        verify_scopes_error_type=src.error.error_type.UNAUTHORIZED_REFRESH_TOKEN_SCOPES,
        options=app_state.service.jwt.verify_refresh_options,
        access_token=account_post_authenticate_refresh_in.access_token
    )

    sub: str
    sub = refresh_token_payload["sub"]
    data: dict
    data = refresh_token_payload["data"]

    # TODO
    #  After token verification update token data based on current db state.

    access_token: str
    access_token = app_state.service.jwt.issue(
        sub=sub,
        data=data,
        lifetime=app_state.service.jwt.lifetime_access,
        scopes=access_token_payload["scopes"]
    )
    refresh_token: str
    refresh_token = app_state.service.jwt.issue(
        sub=sub,
        data=data,
        lifetime=app_state.service.jwt.lifetime_refresh,
        scopes=["type:refresh"],
        access_token=access_token
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
    account = await app_state.database.account.find_one_by_email(
        email=account_post_password_forget_in.username
    )

    if not account:
        await asyncio.sleep(
            delay=1
        )
        return src.dto.account.AccountPostPasswordForgetOut()

    old_password_hash: str
    old_password_hash = account.authentication.password.primary.value

    nonce_bytes: bytes
    nonce_bytes = os.urandom(16)
    signature_bytes: bytes
    signature_bytes = hmac.digest(
        key=old_password_hash.encode("utf-8"),
        msg=nonce_bytes,
        digest="sha256"
    )

    sub: str
    sub = account.identifier
    data: dict
    data = {
        "nonce": nonce_bytes.hex(),
        "signature": signature_bytes.hex()
        # TODO
        #  Consider including client source IP.
        #  This can be verified in stateless manner during recovery.
    }

    password_recover_token: str
    password_recover_token = app_state.service.jwt.issue(
        sub=sub,
        data=data,
        lifetime=app_state.service.jwt.lifetime_password_recover,
        scopes=["type:account-password-recover"]
    )

    try:
        await app_state.service.mail.send_template(
            to={account.email.primary.value: ""},
            locale=app_state.service.locale.by_request(request),
            template=app_state.service.template.mail_account_password_recover,
            token=password_recover_token
        )
    except Exception:
        raise src.error.error.Error(
            code=fastapi.status.HTTP_503_SERVICE_UNAVAILABLE,
            type=src.error.error_type.SERVICE_UNAVAILABLE_MAIL_ACCOUNT_PASSWORD_RECOVER
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
        request: fastapi.Request,
        app_state: src.app_state.AppState = src.depends.app_state.depends(),
        password_recover_token: str = src.depends.bearer_token.depends(),
        account_post_password_recover_in: src.dto.account.AccountPostPasswordRecoverIn = fastapi.Body(
            ...
        )
):
    payload: dict
    payload = app_state.service.jwt.verify(
        token=password_recover_token,
        required_scopes=["type:account-password-recover"],
        verify_token_error_type=src.error.error_type.UNAUTHORIZED_PASSWORD_RECOVER_TOKEN_INVALID,
        verify_iss_error_type=src.error.error_type.UNAUTHORIZED_PASSWORD_RECOVER_TOKEN_ISSUER,
        verify_exp_error_type=src.error.error_type.UNAUTHORIZED_PASSWORD_RECOVER_TOKEN_EXPIRED,
        verify_scopes_error_type=src.error.error_type.UNAUTHORIZED_PASSWORD_RECOVER_TOKEN_SCOPES,
        options=app_state.service.jwt.verify_default_options,
    )

    data: dict
    data = payload["data"]

    nonce_str: str
    nonce_str = data.get("nonce", "")

    signature_str: str
    signature_str = data.get("signature", "")

    if not nonce_str or not signature_str:
        raise src.error.error.Error(
            code=fastapi.status.HTTP_401_UNAUTHORIZED,
            type=src.error.error_type.UNAUTHORIZED_PASSWORD_RECOVER_TOKEN_INVALID
        )

    nonce_bytes: bytes
    nonce_bytes = bytes.fromhex(nonce_str)
    signature_bytes: bytes
    signature_bytes = bytes.fromhex(signature_str)

    sub: str
    sub = payload["sub"]

    account: src.database.account.model.Account
    account = await app_state.database.account.find_one_by_identifier(
        identifier=sub
    )

    if not account:
        raise src.error.error.Error(
            code=fastapi.status.HTTP_401_UNAUTHORIZED,
            type=src.error.error_type.UNAUTHORIZED_PASSWORD_RECOVER_TOKEN_INVALID
        )

    old_password_hash: str
    old_password_hash = account.authentication.password.primary.value

    if not hmac.compare_digest(
            signature_bytes,
            hmac.digest(
                key=old_password_hash.encode("utf-8"),
                msg=nonce_bytes,
                digest="sha256"
            )
    ):
        raise src.error.error.Error(
            code=fastapi.status.HTTP_401_UNAUTHORIZED,
            type=src.error.error_type.UNAUTHORIZED_PASSWORD_RECOVER_TOKEN_EXPIRED
        )

    new_password_hash: str

    while True:
        new_password_hash = app_state.service.password.password_hash(
            password=account_post_password_recover_in.password
        )

        if not hmac.compare_digest(old_password_hash, new_password_hash):
            break

    account.authentication.password.primary.value = new_password_hash

    if not await app_state.database.account.update_one(
            model=account
    ):
        raise src.error.error.Error(
            code=fastapi.status.HTTP_503_SERVICE_UNAVAILABLE,
            type=src.error.error_type.SERVICE_UNAVAILABLE
        )

    return src.dto.account.AccountPostPasswordRecoverOut(
        password=None
    )
