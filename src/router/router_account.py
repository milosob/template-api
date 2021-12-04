import datetime
import os
import time

import fastapi

import src.database.error.database_error_conflict
import src.database.error.database_error_not_found
import src.database.account.database_account_driver_base
import src.database.account.database_account_model
import src.database.confirm.database_confirm_driver_base
import src.database.confirm.database_confirm_model
import src.depends.depends_state_app
import src.depends.depends_state_request
import src.error.error
import src.error.error_type
import src.dto.dto_account
import src.state.state_app
import src.state.state_request

router = fastapi.APIRouter(
    prefix="/account",
    tags=["account"]
)


@router.post(
    path="/register",
    summary="Register account.",
    status_code=fastapi.status.HTTP_201_CREATED,
    responses={
        fastapi.status.HTTP_201_CREATED: {
            "model": src.dto.dto_account.DtoPostAccountRegisterOut,
            "description": "Resource created."
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
        ),
        state_request: src.state.state_request.StateRequest = fastapi.Depends(
            src.depends.depends_state_request.depends
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

    # Assign email and verification token.
    db_account_model.email.reg.primary.email = account_register_in.username
    # Mark email as primary.
    db_account_model.email.reg.primary.primary = True
    # Mark account to require authentication.
    db_account_model.email.reg.primary.confirmed_at = 0
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
        # Send activation email to the email.
        await state_app.service.service_email.send_confirm_email_message(
            email=db_account_model.email.reg.primary.email,
            token=db_confirm_model.token
        )
    except Exception:
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
    summary="Authenticate account.",
    status_code=fastapi.status.HTTP_200_OK,
    responses={
        fastapi.status.HTTP_200_OK: {
            "model": src.dto.dto_account.DtoPostAccountAuthenticateOut,
            "description": "Operation successful."
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
        ),
        state_request: src.state.state_request.StateRequest = fastapi.Depends(
            src.depends.depends_state_request.depends
        )
):
    db_account_model: src.database.account.database_account_model.DatabaseAccountModel

    try:
        # Retrieve account from database.
        db_account_model = await state_app.database.database_account.find_by_email(
            email=post_account_authenticate_in.username
        )
    except src.database.error.database_error_not_found.DatabaseErrorNotFound:
        # TODO Bad request, invalid username or password.
        raise Exception()

    # Authenticate against provided credentials.
    if not state_app.service.service_password.password_verify(
            password=post_account_authenticate_in.password,
            password_hash=db_account_model.authentication.password_reg.primary.password
    ):
        # TODO Bad request, invalid username or password.
        raise Exception()

    # Successfully authenticated.
    # TODO Verify scopes from body.

    return src.dto.dto_account.DtoPostAccountAuthenticateOut(
        token=state_app.service.service_jwt.issue(
            sub=post_account_authenticate_in.username,
            data={
                "id": db_account_model.identifier
            },
            scopes=post_account_authenticate_in.scopes + [
                # TODO Set scopes based on request scopes, account state (verified or not) and desired permissions.
            ]
        ),
        token_type="Bearer"
    )
