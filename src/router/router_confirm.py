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
import src.dto.dto_account
import src.dto.dto_confirm
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
        }
    }
)
async def post_confirm(
        request: fastapi.Request,
        post_confirm_in: src.dto.dto_confirm.DtoPostConfirmIn,
        state_app: src.state.state_app.StateApp = fastapi.Depends(
            src.depends.depends_state_app.depends
        ),
        state_request: src.state.state_request.StateRequest = fastapi.Depends(
            src.depends.depends_state_request.depends
        )
):
    db_confirm_model: src.database.confirm.database_confirm_model.DatabaseConfirmModel

    timestamp_now: int
    timestamp_now = int(time.time())

    try:
        db_confirm_model = await state_app.database.database_confirm.find_by_identifier(
            identifier=post_confirm_in.token
        )
    except src.database.error.database_error_not_found.DatabaseErrorNotFound:
        # TODO Handle case.
        raise Exception()

    if db_confirm_model.expires_at < timestamp_now:
        # TODO Handle case, confirmation time expired.
        raise Exception()

    # Guard to check that confirmation really occurred.
    confirm_guard: bool
    confirm_guard = False

    if db_confirm_model.type == "account-confirm-email":
        # Email confirmation routine.
        db_confirm_model_context: src.database.confirm.database_confirm_model.DatabaseConfirmEmailModel
        db_confirm_model_context = db_confirm_model.context

        db_account_model: src.database.account.database_account_model.DatabaseAccountModel

        try:
            db_account_model = await state_app.database.database_account.find_by_identifier(
                identifier=db_confirm_model_context.identifier
            )
        except src.database.error.database_error_not_found.DatabaseErrorNotFound:
            # TODO Handle case.
            raise Exception()

        for account_email_reg_record in db_account_model.email_reg.records:
            if account_email_reg_record.email == db_confirm_model_context.email:
                confirm_guard = True
                if account_email_reg_record.confirmed_at == 0:
                    account_email_reg_record.confirmed_at = timestamp_now

                    if account_email_reg_record.email == db_account_model.email_reg.primary.email:
                        db_account_model.email_reg.primary.confirmed_at = timestamp_now
                # Already confirmed, ignore.
                break

        if not confirm_guard:
            # TODO Handle case.
            raise Exception()

        db_confirm_model.confirmed_at = timestamp_now

        try:

            await state_app.database.database_confirm.update(
                db_confirm_model
            )

        except src.database.error.database_error_not_found.DatabaseErrorNotFound:
            # TODO Handle case.
            raise Exception()

        try:

            await state_app.database.database_account.update(
                db_account_model
            )

        except src.database.error.database_error_not_found.DatabaseErrorNotFound:
            # TODO Handle case.
            raise Exception()

        # Maybe return confirmation context data?
        return src.dto.dto_confirm.DtoPostConfirmOut()

    else:
        # Programmer error.
        raise Exception()
