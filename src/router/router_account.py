import datetime
import os

import fastapi

import src.database.error.database_error_conflict
import src.database.error.database_error_not_found
import src.database.account.database_account_driver_base
import src.database.account.database_account_model
import src.database.confirm.database_confirm_driver_base
import src.database.confirm.database_confirm_model
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
        account_register_in: src.dto.dto_account.DtoPostAccountRegisterIn = fastapi.Body(
            ...
        ),
        state_app: src.state.state_app.StateApp = fastapi.Depends(
            src.depends.depends_state_app.depends
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
            language=state_app.service.service_lang.by_request(
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
            type=src.error.error_type.SERVICE_UNAVAILABLE
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
        post_account_authenticate_in: src.dto.dto_account.DtoPostAccountAuthenticateIn = fastapi.Body(
            ...
        ),
        state_app: src.state.state_app.StateApp = fastapi.Depends(
            src.depends.depends_state_app.depends
        )
):
    db_account_model: src.database.account.database_account_model.DatabaseAccountModel

    try:
        # Retrieve account from database.
        db_account_model = await state_app.database.database_account.find_by_email(
            email=post_account_authenticate_in.username
        )
    except src.database.error.database_error_not_found.DatabaseErrorNotFound:
        raise src.error.error.Error(
            code=fastapi.status.HTTP_401_UNAUTHORIZED,
            type=src.error.error_type.ACCOUNT_AUTHENTICATE_INVALID_CREDENTIALS
        )

    # Authenticate against provided credentials.
    if not state_app.service.service_password.password_verify(
            password=post_account_authenticate_in.password,
            password_hash=db_account_model.authentication.password_reg.primary.password
    ):
        raise src.error.error.Error(
            code=fastapi.status.HTTP_401_UNAUTHORIZED,
            type=src.error.error_type.ACCOUNT_AUTHENTICATE_INVALID_CREDENTIALS
        )

    # Successfully authenticated.

    sub: str
    sub = post_account_authenticate_in.username
    data: dict
    data = {
        "id": db_account_model.identifier
    }

    access_token: str
    access_token = state_app.service.service_jwt.issue_access(
        sub=post_account_authenticate_in.username,
        data=data,
        scopes=[]
    )
    refresh_token: str
    refresh_token = state_app.service.service_jwt.issue_refresh(
        sub=sub,
        data=data,
        scopes=[],
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
        post_account_authenticate_refresh_in: src.dto.dto_account.DtoPostAccountAuthenticateRefreshIn = fastapi.Body(
            ...
        ),
        state_app: src.state.state_app.StateApp = fastapi.Depends(
            src.depends.depends_state_app.depends
        )
):
    payload: dict
    payload = state_app.service.service_jwt.verify_refresh(
        access_token=post_account_authenticate_refresh_in.access_token,
        refresh_token=post_account_authenticate_refresh_in.refresh_token,
        refresh_token_required_scopes=[]
    )

    sub: str
    sub = payload["sub"]
    data: dict
    data = payload["data"]

    access_token: str
    access_token = state_app.service.service_jwt.issue_access(
        sub=sub,
        data=data,
        scopes=[]
    )
    refresh_token: str
    refresh_token = state_app.service.service_jwt.issue_refresh(
        sub=sub,
        data=data,
        scopes=[],
        access_token=access_token
    )

    return src.dto.dto_account.DtoPostAccountAuthenticateRefreshOut(
        access_token=access_token,
        refresh_token=refresh_token
    )
