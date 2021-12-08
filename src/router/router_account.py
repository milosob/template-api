import asyncio
import datetime
import hmac
import os

import fastapi
import fastapi.security

import src.database.error.database_error_conflict
import src.database.error.database_error_not_found
import src.database.account.database_account_driver_base
import src.database.account.database_account_model
import src.database.confirm.database_confirm_driver_base
import src.database.confirm.database_confirm_model
import src.depends.depends_bearer_token
import src.depends.depends_state_app
import src.error.error
import src.error.error_type
import src.dto.dto_account
import src.dto.dto_error
import src.state.state_app
import src.state.state_request

router = fastapi.APIRouter(
    prefix="/account",
    tags=["account"]
)


@router.post(
    path="/register",
    summary="Account register.",
    status_code=fastapi.status.HTTP_201_CREATED,
    responses={
        fastapi.status.HTTP_201_CREATED: {
            "model": src.dto.dto_account.DtoPostAccountRegisterOut,
            "description": "Resource created."
        },
        fastapi.status.HTTP_400_BAD_REQUEST: {
            "model": src.dto.dto_error.DtoErrorApiOut,
            "description": "Error."
        },
        fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": src.dto.dto_error.DtoErrorApiOut,
            "description": "Error."
        },
        fastapi.status.HTTP_503_SERVICE_UNAVAILABLE: {
            "model": src.dto.dto_error.DtoErrorApiOut,
            "description": "Error."
        }
    }
)
async def post_account_register(
        request: fastapi.Request,
        state_app: src.state.state_app.StateApp = src.depends.depends_state_app.depends(),
        account_register_in: src.dto.dto_account.DtoPostAccountRegisterIn = fastapi.Body(
            ...
        )
):
    db_account_model: src.database.account.database_account_model.DatabaseAccountModel
    db_account_model = src.database.account.database_account_model.DatabaseAccountModel()

    db_confirm_model: src.database.confirm.database_confirm_model.DatabaseConfirmModel
    db_confirm_model = src.database.confirm.database_confirm_model.DatabaseConfirmModel()

    db_confirm_model_context: src.database.confirm.database_confirm_model.DatabaseConfirmEmailModel
    db_confirm_model_context = src.database.confirm.database_confirm_model.DatabaseConfirmEmailModel()

    date_now: datetime.datetime
    date_now = datetime.datetime.utcnow()

    try:
        # Verify that email is available.
        _ = await state_app.database.database_account.find_by_email(
            email=account_register_in.username
        )

        raise src.error.error.Error(
            code=fastapi.status.HTTP_400_BAD_REQUEST,
            type=src.error.error_type.ACCOUNT_REGISTER_USERNAME_TAKEN
        )

    except src.database.error.database_error_not_found.DatabaseErrorNotFound:
        pass

    # Assign email.
    db_account_model.email.reg.primary.email = account_register_in.username
    # Mark email as primary.
    db_account_model.email.reg.primary.primary = True
    # Mark account to require authentication.
    db_account_model.email.reg.primary.confirmed_at = None
    # Append email record to registry.
    db_account_model.email.reg.records.append(
        db_account_model.email.reg.primary
    )

    # Hash user password.
    db_account_model.authentication.password_reg.primary.password = state_app.service.service_password.password_hash(
        password=account_register_in.password
    )

    try:
        # Save account.
        db_account_model = await state_app.database.database_account.insert(
            model=db_account_model
        )
    except src.database.error.database_error_conflict.DatabaseErrorConflict:
        raise src.error.error.Error(
            code=fastapi.status.HTTP_400_BAD_REQUEST,
            type=src.error.error_type.ACCOUNT_REGISTER_USERNAME_TAKEN
        )

    # Configure confirm model.
    db_confirm_model.token = os.urandom(32).hex()
    db_confirm_model.issued_at = date_now
    db_confirm_model.expires_at = date_now + datetime.timedelta(
        minutes=15
    )
    db_confirm_model.confirmed_at = None
    db_confirm_model.type = "account-confirm-email"

    # Configure confirm model context.
    db_confirm_model_context.email = account_register_in.username

    # Assign context to confirm model.
    db_confirm_model.context = db_confirm_model_context

    try:
        # Save account confirm.
        db_confirm_model = await state_app.database.database_confirm.insert(
            model=db_confirm_model
        )
    except src.database.error.database_error_conflict.DatabaseErrorConflict:
        raise src.error.error.Error(
            code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
            type=src.error.error_type.INTERNAL_SERVER_ERROR
        )

    try:
        await state_app.service.service_email.send_template_account_register_confirm(
            language=state_app.service.service_locale.by_request(
                request=request
            ),
            parameters={
                "to": {
                    db_account_model.email.reg.primary.email: None
                },
                "subject": {},
                "body": {
                    "token": db_confirm_model.token
                }
            }
        )
    except Exception as e:
        raise src.error.error.Error(
            code=fastapi.status.HTTP_503_SERVICE_UNAVAILABLE,
            type=src.error.error_type.SERVICE_UNAVAILABLE_EMAIL_ACCOUNT_REGISTER
        )

    return src.dto.dto_account.DtoPostAccountRegisterOut(
        username=account_register_in.username,
        password=None
    )


@router.post(
    path="/authenticate",
    summary="Account authenticate.",
    status_code=fastapi.status.HTTP_200_OK,
    responses={
        fastapi.status.HTTP_200_OK: {
            "model": src.dto.dto_account.DtoPostAccountAuthenticateOut,
            "description": "Operation successful."
        },
        fastapi.status.HTTP_401_UNAUTHORIZED: {
            "model": src.dto.dto_error.DtoErrorApiOut,
            "description": "Error."
        },
        fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": src.dto.dto_error.DtoErrorApiOut,
            "description": "Error."
        },
        fastapi.status.HTTP_503_SERVICE_UNAVAILABLE: {
            "model": src.dto.dto_error.DtoErrorApiOut,
            "description": "Error."
        }
    }
)
async def post_account_authenticate(
        request: fastapi.Request,
        state_app: src.state.state_app.StateApp = src.depends.depends_state_app.depends(),
        post_account_authenticate_in: src.dto.dto_account.DtoPostAccountAuthenticateIn = fastapi.Body(
            ...
        )
):
    db_account_model: src.database.account.database_account_model.DatabaseAccountModel

    try:
        # Find account.
        db_account_model = await state_app.database.database_account.find_by_email(
            email=post_account_authenticate_in.username
        )
    except src.database.error.database_error_not_found.DatabaseErrorNotFound:
        raise src.error.error.Error(
            code=fastapi.status.HTTP_401_UNAUTHORIZED,
            type=src.error.error_type.ACCOUNT_AUTHENTICATE_INVALID_CREDENTIALS
        )

    # Verify password.
    if not state_app.service.service_password.password_verify(
            password=post_account_authenticate_in.password,
            password_hash=db_account_model.authentication.password_reg.primary.password
    ):
        raise src.error.error.Error(
            code=fastapi.status.HTTP_401_UNAUTHORIZED,
            type=src.error.error_type.ACCOUNT_AUTHENTICATE_INVALID_CREDENTIALS
        )

    sub: str
    sub = db_account_model.identifier
    data: dict
    data = {}

    # Issue new access_token and refresh token.
    access_token: str
    access_token = state_app.service.service_jwt.issue(
        sub=sub,
        data=data,
        lifetime=state_app.service.service_jwt.lifetime_access,
        scopes=["type:access"]
    )
    refresh_token: str
    refresh_token = state_app.service.service_jwt.issue(
        sub=sub,
        data=data,
        lifetime=state_app.service.service_jwt.lifetime_refresh,
        scopes=["type:refresh"],
        access_token=access_token
    )

    return src.dto.dto_account.DtoPostAccountAuthenticateOut(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post(
    path="/authenticate/refresh",
    summary="Account authenticate refresh.",
    status_code=fastapi.status.HTTP_200_OK,
    responses={
        fastapi.status.HTTP_200_OK: {
            "model": src.dto.dto_account.DtoPostAccountAuthenticateRefreshOut,
            "description": "Operation successful."
        },
        fastapi.status.HTTP_400_BAD_REQUEST: {
            "model": src.dto.dto_error.DtoErrorApiOut,
            "description": "Error."
        },
        fastapi.status.HTTP_401_UNAUTHORIZED: {
            "model": src.dto.dto_error.DtoErrorApiOut,
            "description": "Error."
        },
        fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": src.dto.dto_error.DtoErrorApiOut,
            "description": "Error."
        },
        fastapi.status.HTTP_503_SERVICE_UNAVAILABLE: {
            "model": src.dto.dto_error.DtoErrorApiOut,
            "description": "Error."
        }
    }
)
async def post_account_authenticate_refresh(
        request: fastapi.Request,
        state_app: src.state.state_app.StateApp = src.depends.depends_state_app.depends(),
        post_account_authenticate_refresh_in: src.dto.dto_account.DtoPostAccountAuthenticateRefreshIn = fastapi.Body(
            ...
        )
):
    access_token_payload: dict
    access_token_payload = state_app.service.service_jwt.verify(
        token=post_account_authenticate_refresh_in.access_token,
        required_scopes=["type:access"],
        verify_token_error_type=src.error.error_type.UNAUTHORIZED_ACCESS_TOKEN_INVALID,
        verify_iss_error_type=src.error.error_type.UNAUTHORIZED_ACCESS_TOKEN_ISSUER,
        # Skip expiration verification.
        verify_exp_error_type=None,
        verify_scopes_error_type=src.error.error_type.UNAUTHORIZED_ACCESS_TOKEN_SCOPES,
        options=state_app.service.service_jwt.verify_access_options
    )

    refresh_token_payload: dict
    refresh_token_payload = state_app.service.service_jwt.verify(
        token=post_account_authenticate_refresh_in.refresh_token,
        required_scopes=["type:refresh"],
        verify_token_error_type=src.error.error_type.UNAUTHORIZED_REFRESH_TOKEN_INVALID,
        verify_iss_error_type=src.error.error_type.UNAUTHORIZED_REFRESH_TOKEN_ISSUER,
        verify_exp_error_type=src.error.error_type.UNAUTHORIZED_REFRESH_TOKEN_EXPIRED,
        verify_scopes_error_type=src.error.error_type.UNAUTHORIZED_REFRESH_TOKEN_SCOPES,
        options=state_app.service.service_jwt.verify_refresh_options,
        access_token=post_account_authenticate_refresh_in.access_token
    )

    sub: str
    sub = refresh_token_payload["sub"]
    data: dict
    data = refresh_token_payload["data"]

    # TODO
    #  After token verification update token data based on current db state.

    # Issue new access_token and refresh token.
    access_token: str
    access_token = state_app.service.service_jwt.issue(
        sub=sub,
        data=data,
        lifetime=state_app.service.service_jwt.lifetime_access,
        scopes=access_token_payload["scopes"]
    )
    refresh_token: str
    refresh_token = state_app.service.service_jwt.issue(
        sub=sub,
        data=data,
        lifetime=state_app.service.service_jwt.lifetime_refresh,
        scopes=["type:refresh"],
        access_token=access_token
    )

    return src.dto.dto_account.DtoPostAccountAuthenticateRefreshOut(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post(
    path="/password/forget",
    summary="Account password forget.",
    status_code=fastapi.status.HTTP_200_OK,
    responses={
        fastapi.status.HTTP_200_OK: {
            "model": src.dto.dto_account.DtoPostAccountPasswordForgetOut,
            "description": "Operation successful."
        },
        fastapi.status.HTTP_400_BAD_REQUEST: {
            "model": src.dto.dto_error.DtoErrorApiOut,
            "description": "Error."
        },
        fastapi.status.HTTP_401_UNAUTHORIZED: {
            "model": src.dto.dto_error.DtoErrorApiOut,
            "description": "Error."
        },
        fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": src.dto.dto_error.DtoErrorApiOut,
            "description": "Error."
        },
        fastapi.status.HTTP_503_SERVICE_UNAVAILABLE: {
            "model": src.dto.dto_error.DtoErrorApiOut,
            "description": "Error."
        }
    }
)
async def post_account_password_forget(
        request: fastapi.Request,
        state_app: src.state.state_app.StateApp = src.depends.depends_state_app.depends(),
        post_account_password_forget_in: src.dto.dto_account.DtoPostAccountPasswordForgetIn = fastapi.Body(
            ...
        )
):
    db_account_model: src.database.account.database_account_model.DatabaseAccountModel

    try:
        # Find account.
        db_account_model = await state_app.database.database_account.find_by_email(
            email=post_account_password_forget_in.username
        )
    except src.database.error.database_error_not_found.DatabaseErrorNotFound:
        # Account does not exist.
        await asyncio.sleep(
            delay=1
        )
        return src.dto.dto_account.DtoPostAccountPasswordForgetOut()

    # Build recover context to auto revoke token if password was changed.
    # It's possible to request many recovery links, however as soon password will be changed mac verification will fail.
    nonce_bytes: bytes
    nonce_bytes = os.urandom(16)
    signature_bytes: bytes
    signature_bytes = hmac.digest(
        key=db_account_model.authentication.password_reg.primary.password.encode("utf-8"),
        msg=nonce_bytes,
        digest="sha256"
    )

    sub: str
    sub = db_account_model.identifier
    data: dict
    data = {
        "nonce": nonce_bytes.hex(),
        "signature": signature_bytes.hex()
        # TODO
        #  Consider including client source IP.
        #  This can be verified in stateless manner during recovery.
    }

    # Issue JWT password recover token.
    password_recover_token: str
    password_recover_token = state_app.service.service_jwt.issue(
        sub=sub,
        data=data,
        lifetime=state_app.service.service_jwt.lifetime_password_recover,
        scopes=["type:password_recover"]
    )

    try:
        pass
        # TODO Send email with password recovery link.
    except Exception:
        raise src.error.error.Error(
            code=fastapi.status.HTTP_503_SERVICE_UNAVAILABLE,
            type=src.error.error_type.SERVICE_UNAVAILABLE_EMAIL_ACCOUNT_PASSWORD_FORGET
        )

    return src.dto.dto_account.DtoPostAccountPasswordForgetOut()


@router.post(
    path="/password/recover",
    summary="Account password recover.",
    status_code=fastapi.status.HTTP_200_OK,
    responses={
        fastapi.status.HTTP_200_OK: {
            "model": src.dto.dto_account.DtoPostAccountPasswordRecoverOut,
            "description": "Operation successful."
        },
        fastapi.status.HTTP_400_BAD_REQUEST: {
            "model": src.dto.dto_error.DtoErrorApiOut,
            "description": "Error."
        },
        fastapi.status.HTTP_401_UNAUTHORIZED: {
            "model": src.dto.dto_error.DtoErrorApiOut,
            "description": "Error."
        },
        fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": src.dto.dto_error.DtoErrorApiOut,
            "description": "Error."
        },
        fastapi.status.HTTP_503_SERVICE_UNAVAILABLE: {
            "model": src.dto.dto_error.DtoErrorApiOut,
            "description": "Error."
        }
    }
)
async def post_account_password_recover(
        request: fastapi.Request,
        state_app: src.state.state_app.StateApp = src.depends.depends_state_app.depends(),
        password_recover_token: str = src.depends.depends_bearer_token.depends(),
        post_account_password_recover_in: src.dto.dto_account.DtoPostAccountPasswordRecoverIn = fastapi.Body(
            ...
        )
):
    payload: dict
    payload = state_app.service.service_jwt.verify(
        token=password_recover_token,
        required_scopes=["type:password_recover"],
        verify_token_error_type=src.error.error_type.UNAUTHORIZED_PASSWORD_RECOVER_TOKEN_INVALID,
        verify_iss_error_type=src.error.error_type.UNAUTHORIZED_PASSWORD_RECOVER_TOKEN_ISSUER,
        verify_exp_error_type=src.error.error_type.UNAUTHORIZED_PASSWORD_RECOVER_TOKEN_EXPIRED,
        verify_scopes_error_type=src.error.error_type.UNAUTHORIZED_PASSWORD_RECOVER_TOKEN_SCOPES,
        options=state_app.service.service_jwt.verify_password_recover_options,
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

    identifier: str
    identifier = payload["sub"]

    db_account_model: src.database.account.database_account_model.DatabaseAccountModel

    try:
        # Find account.
        db_account_model = await state_app.database.database_account.find_by_identifier(
            identifier=identifier
        )
    except src.database.error.database_error_not_found.DatabaseErrorNotFound:
        raise src.error.error.Error(
            code=fastapi.status.HTTP_401_UNAUTHORIZED,
            type=src.error.error_type.UNAUTHORIZED_PASSWORD_RECOVER_TOKEN_INVALID
        )

    old_password_hash: str
    old_password_hash = db_account_model.authentication.password_reg.primary.password

    # Verify that symmetric signature is correct.
    if not hmac.compare_digest(
            signature_bytes,
            hmac.digest(
                key=db_account_model.authentication.password_reg.primary.password.encode("utf-8"),
                msg=nonce_bytes,
                digest="sha256"
            )
    ):
        # Password was already changed, token expired.
        raise src.error.error.Error(
            code=fastapi.status.HTTP_401_UNAUTHORIZED,
            type=src.error.error_type.UNAUTHORIZED_PASSWORD_RECOVER_TOKEN_EXPIRED
        )

    new_password_hash: str

    while True:
        new_password_hash = state_app.service.service_password.password_hash(
            post_account_password_recover_in.password
        )

        # The chance it will not break is like 1 / ( 2**128 * (password repetition probability))
        if not hmac.compare_digest(old_password_hash, new_password_hash):
            break

    db_account_model.authentication.password_reg.primary.password = new_password_hash

    try:
        # Update account.
        db_account_model = await state_app.database.database_account.update(
            db_account_model
        )
    except src.database.error.database_error_not_found.DatabaseErrorNotFound:
        raise src.error.error.Error(
            code=fastapi.status.HTTP_503_SERVICE_UNAVAILABLE,
            type=src.error.error_type.SERVICE_UNAVAILABLE
        )

    # Password successfully changed.
    return src.dto.dto_account.DtoPostAccountPasswordRecoverOut()
