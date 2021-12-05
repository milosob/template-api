import datetime

import fastapi

import src.database.error.database_error_conflict
import src.database.error.database_error_not_found
import src.database.account.database_account_driver_base
import src.database.account.database_account_model
import src.database.confirm.database_confirm_driver_base
import src.database.confirm.database_confirm_model
import src.depends.depends_state_app
import src.depends.depends_state_request
import src.dto.dto_account
import src.dto.dto_confirm
import src.error.error
import src.error.error_type
import src.state.state_app
import src.state.state_request

router = fastapi.APIRouter(
    prefix="/confirm",
    tags=["confirm"]
)


@router.post(
    path="",
    summary="Performs confirmation of specific operation identified by supplied token.",
    status_code=fastapi.status.HTTP_200_OK,
    responses={
        fastapi.status.HTTP_200_OK: {
            "model": src.dto.dto_confirm.DtoPostConfirmOut,
            "description": "Confirmation succeeded."
        },
        fastapi.status.HTTP_400_BAD_REQUEST: {
            "model": src.dto.dto_error.DtoErrorApiOut,
            "description": "Error."
        },
        fastapi.status.HTTP_404_NOT_FOUND: {
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
async def post_confirm(
        request: fastapi.Request,
        post_confirm_in: src.dto.dto_confirm.DtoPostConfirmIn = fastapi.Body(
            ...
        ),
        state_app: src.state.state_app.StateApp = fastapi.Depends(
            src.depends.depends_state_app.depends
        ),
        state_request: src.state.state_request.StateRequest = fastapi.Depends(
            src.depends.depends_state_request.depends
        )
):
    db_confirm_model: src.database.confirm.database_confirm_model.DatabaseConfirmModel

    date_now: datetime.datetime
    date_now = datetime.datetime.utcnow()

    try:
        # Retrieve confirm.
        db_confirm_model = await state_app.database.database_confirm.find_by_token(
            token=post_confirm_in.token
        )
    except src.database.error.database_error_not_found.DatabaseErrorNotFound:
        raise src.error.error.Error(
            code=fastapi.status.HTTP_404_NOT_FOUND,
            type=src.error.error_type.CONFIRM_TOKEN_NOT_FOUND
        )

    # Check if token expired.
    if db_confirm_model.expires_at < date_now:
        raise src.error.error.Error(
            code=fastapi.status.HTTP_400_BAD_REQUEST,
            type=src.error.error_type.CONFIRM_TOKEN_EXPIRED
        )

    # Check if token was consumed.
    if db_confirm_model.confirmed_at is not None:
        raise src.error.error.Error(
            code=fastapi.status.HTTP_400_BAD_REQUEST,
            type=src.error.error_type.CONFIRM_TOKEN_CONSUMED
        )

    # Guard to check that confirmation really occurred.
    confirm_guard: bool
    confirm_guard = False

    if db_confirm_model.type == "account-confirm-email":
        # Email confirmation routine.
        db_confirm_model_context: src.database.confirm.database_confirm_model.DatabaseConfirmEmailModel
        db_confirm_model_context = db_confirm_model.context

        db_account_model: src.database.account.database_account_model.DatabaseAccountModel

        try:
            # Find account.
            db_account_model = await state_app.database.database_account.find_by_email(
                email=db_confirm_model_context.email
            )
        except src.database.error.database_error_not_found.DatabaseErrorNotFound:
            raise src.error.error.Error(
                code=fastapi.status.HTTP_404_NOT_FOUND,
                type=src.error.error_type.CONFIRM_TOKEN_EMAIL_NOT_FOUND
            )

        for email_reg_record in db_account_model.email.reg.records:
            # Confirm on matching email.
            if email_reg_record.email == db_confirm_model_context.email:
                confirm_guard = True
                if email_reg_record.confirmed_at is None:
                    email_reg_record.confirmed_at = date_now
                    if email_reg_record.email == db_account_model.email.reg.primary.email:
                        db_account_model.email.reg.primary.confirmed_at = date_now

        if not confirm_guard:
            raise src.error.error.Error(
                code=fastapi.status.HTTP_400_BAD_REQUEST,
                type=src.error.error_type.CONFIRM_TOKEN_FAILURE
            )

        db_confirm_model.confirmed_at = date_now

        # Update confirm.
        await state_app.database.database_confirm.update(
            model=db_confirm_model
        )

        # Update account.
        await state_app.database.database_account.update(
            model=db_account_model
        )

        # Maybe return confirmation context data?
        return src.dto.dto_confirm.DtoPostConfirmOut()

    else:
        # Programmer error.
        raise src.error.error.Error(
            code=fastapi.status.HTTP_400_BAD_REQUEST,
            type=src.error.error_type.CONFIRM_TOKEN_FAILURE
        )
