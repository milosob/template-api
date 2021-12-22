import asyncio

import fastapi
import fastapi.security

import src.app_state
import src.database.account.filter
import src.database.account.update
import src.database.account.model
import src.depends.app_state
import src.depends.jwt.access
import src.depends.jwt.recover
import src.depends.jwt.refresh
import src.depends.jwt.register
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
        }
    }
)
async def account_post_register(
        request: fastapi.Request,
        app_state: src.app_state.AppState = src.depends.app_state.depends(),
        dto: src.dto.account.AccountPostRegisterIn = fastapi.Body(...)
):
    account: src.database.account.model.Account
    account = app_state.database.account.find_one(
        src.database.account.filter.emails(
            [dto.username]
        )
    )

    if account:
        raise src.error.error.Error(
            fastapi.status.HTTP_400_BAD_REQUEST,
            src.error.error_type.BAD_REQUEST_USERNAME_UNAVAILABLE
        )

    account = src.database.account.model.Account()

    account_contact_email_primary: src.database.account.model.AccountContactEmail
    account_contact_email_primary = src.database.account.model.AccountContactEmail()
    account_contact_email_primary.email = dto.username
    account_contact_email_primary.primary = True
    account_contact_email_primary.confirmed = False
    account.contact.emails.append(
        account_contact_email_primary
    )

    account.authentication.passwords.primary.value = app_state.service.password.password_hash(
        dto.password
    )

    account_inserted: src.database.account.model.Account
    account_inserted = app_state.database.account.insert_one(
        account
    )

    if not account_inserted:
        raise src.error.error.Error(
            fastapi.status.HTTP_503_SERVICE_UNAVAILABLE,
            src.error.error_type.SERVICE_UNAVAILABLE_DATABASE
        )

    account = account_inserted

    jwt_register: src.dto.jwt.JwtRegister
    jwt_register = src.dto.jwt.JwtRegister()

    register_token: str
    register_token = app_state.service.jwt.issue(
        account.identifier,
        jwt_register.to_json_dict(),
        app_state.service.jwt.lifetime_register,
        app_state.service.jwt.issue_register_scopes
    )

    try:
        await app_state.service.mail.send_template(
            {next(email for email in account.contact.emails if email.primary).email: ""},
            None,
            None,
            app_state.service.locale.by_request(request),
            app_state.service.template.mail_account_register,
            token=register_token
        )
    except Exception:
        raise src.error.error.Error(
            fastapi.status.HTTP_503_SERVICE_UNAVAILABLE,
            src.error.error_type.SERVICE_UNAVAILABLE_MAIL
        )

    return src.dto.account.AccountPostRegisterOut(
        username=dto.username,
        password=None
    )


@router.post(
    path="/register/confirm",
    summary="Account register.",
    status_code=fastapi.status.HTTP_200_OK,
    responses=error_responses | {
        fastapi.status.HTTP_200_OK: {
            "model": src.dto.account.AccountPostRegisterConfirmOut,
            "description": "Resource created."
        }
    }
)
async def account_post_register_confirm(
        jwt: src.dto.jwt.Jwt = src.depends.jwt.register.depends(),
        app_state: src.app_state.AppState = src.depends.app_state.depends(),
        dto: src.dto.account.AccountPostRegisterConfirmIn = fastapi.Body(...)
):
    account: src.database.account.model.Account
    account = app_state.database.account.find_one(
        src.database.account.filter.identifier(
            jwt.sub
        )
    )

    if account.verification.email:
        return src.dto.account.AccountPostRegisterConfirmOut()

    account.verification.email = True

    account_contact_email_primary: src.database.account.model.AccountContactEmail
    account_contact_email_primary = next((email for email in account.contact.emails if email.primary), None)

    if not account_contact_email_primary:
        raise src.error.error.Error(
            fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
            src.error.error_type.INTERNAL_SERVER_ERROR
        )

    account_contact_email_primary.confirmed = True

    if not app_state.database.account.update_one(
            account,
            {
                "$set": {
                    src.database.account.update.verification,
                    src.database.account.update.contact_emails
                }
            }
    ):
        raise src.error.error.Error(
            fastapi.status.HTTP_503_SERVICE_UNAVAILABLE,
            src.error.error_type.SERVICE_UNAVAILABLE_DATABASE
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
        app_state: src.app_state.AppState = src.depends.app_state.depends(),
        dto: src.dto.account.AccountPostAuthenticateIn = fastapi.Body(...)
):
    account: src.database.account.model.Account
    account = app_state.database.account.find_one(
        src.database.account.filter.emails(
            [dto.username]
        )
    )

    if not account:
        raise src.error.error.Error(
            fastapi.status.HTTP_401_UNAUTHORIZED,
            src.error.error_type.UNAUTHORIZED_CREDENTIALS
        )

    if not app_state.service.password.password_verify(
            dto.password,
            account.authentication.passwords.primary.value
    ):
        raise src.error.error.Error(
            fastapi.status.HTTP_401_UNAUTHORIZED,
            src.error.error_type.UNAUTHORIZED_CREDENTIALS
        )

    jwt_access: src.dto.jwt.JwtAccess
    jwt_access = src.dto.jwt.JwtAccess()
    jwt_access.user = src.dto.jwt.JwtUser.from_account(account)

    jwt_refresh: src.dto.jwt.JwtRefresh
    jwt_refresh = src.dto.jwt.JwtRefresh()
    jwt_refresh.counter = 0

    access_token: str
    access_token = app_state.service.jwt.issue(
        account.identifier,
        jwt_access.to_json_dict(),
        app_state.service.jwt.lifetime_access,
        app_state.service.jwt.issue_access_scopes
    )

    refresh_token: str
    refresh_token = app_state.service.jwt.issue(
        account.identifier,
        jwt_refresh.to_json_dict(),
        app_state.service.jwt.lifetime_refresh,
        app_state.service.jwt.issue_refresh_scopes,
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
        app_state: src.app_state.AppState = src.depends.app_state.depends(),
        jwt: src.dto.jwt.Jwt = src.depends.jwt.refresh.depends()
):
    jwt.refresh.counter += 1

    access_token: str
    access_token = app_state.service.jwt.issue(
        jwt.sub,
        jwt.access.to_json_dict(),
        app_state.service.jwt.lifetime_access,
        jwt.access_scopes
    )
    refresh_token: str
    refresh_token = app_state.service.jwt.issue(
        jwt.sub,
        jwt.refresh.to_json_dict(),
        app_state.service.jwt.lifetime_refresh,
        jwt.refresh_scopes,
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
        dto: src.dto.account.AccountPostPasswordForgetIn = fastapi.Body(...)
):
    account: src.database.account.model.Account
    account = app_state.database.account.find_one(
        src.database.account.filter.emails(
            [dto.username]
        )
    )

    if not account:
        await asyncio.sleep(2)
        return src.dto.account.AccountPostPasswordForgetOut()

    old_password: str
    old_password = account.authentication.passwords.primary.value

    jwt_recover: src.dto.jwt.JwtRecover
    jwt_recover = src.dto.jwt.JwtRecover()
    jwt_recover.sign(
        old_password
    )

    recover_token: str
    recover_token = app_state.service.jwt.issue(
        account.identifier,
        jwt_recover.to_json_dict(),
        app_state.service.jwt.lifetime_recover,
        app_state.service.jwt.issue_recover_scopes + ["recover:password"]
    )

    try:
        await app_state.service.mail.send_template(
            {next(email for email in account.contact.emails if email.primary).email: ""},
            None,
            None,
            app_state.service.locale.by_request(request),
            app_state.service.template.mail_account_password_recover,
            token=recover_token
        )
    except Exception:
        raise src.error.error.Error(
            fastapi.status.HTTP_503_SERVICE_UNAVAILABLE,
            src.error.error_type.SERVICE_UNAVAILABLE_MAIL
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
        jwt: src.dto.jwt.Jwt = src.depends.jwt.recover.depends(["recover:password"]),
        app_state: src.app_state.AppState = src.depends.app_state.depends(),
        dto: src.dto.account.AccountPostPasswordRecoverIn = fastapi.Body(...)
):
    account: src.database.account.model.Account
    account = app_state.database.account.find_one(
        src.database.account.filter.identifier(
            jwt.sub
        )
    )

    if not account:
        raise src.error.error.Error(
            fastapi.status.HTTP_401_UNAUTHORIZED,
            src.error.error_type.UNAUTHORIZED_RECOVER_TOKEN_INVALID
        )

    old_password: str
    old_password = account.authentication.passwords.primary.value

    if not jwt.recover.verify(
            old_password
    ):
        raise src.error.error.Error(
            fastapi.status.HTTP_401_UNAUTHORIZED,
            src.error.error_type.UNAUTHORIZED_RECOVER_TOKEN_EXPIRED
        )

    new_password: str
    new_password = app_state.service.password.password_hash(
        dto.password
    )

    account.authentication.passwords.primary.value = new_password

    if not app_state.database.account.update_one(
            account,
            {
                "$set": {
                    src.database.account.update.authentication_passwords_primary
                }
            }
    ):
        raise src.error.error.Error(
            fastapi.status.HTTP_503_SERVICE_UNAVAILABLE,
            src.error.error_type.SERVICE_UNAVAILABLE_DATABASE
        )

    return src.dto.account.AccountPostPasswordRecoverOut(
        password=None
    )


@router.get(
    path="/info",
    summary="Fetch resource.",
    status_code=fastapi.status.HTTP_200_OK,
    responses=error_responses | {
        fastapi.status.HTTP_200_OK: {
            "model": src.dto.account.AccountGetInfoOut,
            "description": "Resource fetched."
        },
    }
)
async def account_get_info(
        jwt: src.dto.jwt.Jwt = src.depends.jwt.access.depends(),
        app_state: src.app_state.AppState = src.depends.app_state.depends(),
        dto: src.dto.account.AccountGetInfoIn = fastapi.Depends()
):
    account: src.database.account.model.Account
    account = app_state.database.account.find_one(
        src.database.account.filter.identifier(
            jwt.sub
        )
    )

    if not account:
        raise src.error.error.Error(
            fastapi.status.HTTP_404_NOT_FOUND,
            src.error.error_type.NOT_FOUND_ACCOUNT
        )

    if not account.info:
        raise src.error.error.Error(
            fastapi.status.HTTP_404_NOT_FOUND,
            src.error.error_type.NOT_FOUND_ACCOUNT_INFO
        )

    return src.dto.account.AccountGetInfoOut(
        alias=account.info.alias,
        gender=account.info.gender,
        birthdate=account.info.birthdate
    )


@router.put(
    path="/info",
    summary="Modify resource.",
    status_code=fastapi.status.HTTP_201_CREATED,
    responses=error_responses | {
        fastapi.status.HTTP_201_CREATED: {
            "model": src.dto.account.AccountPutInfoOut,
            "description": "Resource modified."
        },
    }
)
async def account_put_info(
        jwt: src.dto.jwt.Jwt = src.depends.jwt.access.depends(),
        app_state: src.app_state.AppState = src.depends.app_state.depends(),
        dto: src.dto.account.AccountPutInfoIn = fastapi.Body(...)
):
    account: src.database.account.model.Account
    account = app_state.database.account.find_one(
        src.database.account.filter.identifier(
            jwt.sub
        )
    )

    if not account:
        raise src.error.error.Error(
            fastapi.status.HTTP_404_NOT_FOUND,
            src.error.error_type.NOT_FOUND_ACCOUNT
        )

    if not account.info:
        raise src.error.error.Error(
            fastapi.status.HTTP_404_NOT_FOUND,
            src.error.error_type.NOT_FOUND_ACCOUNT_INFO
        )

    # todo
    #   Implement generic attribute to update transform.

    raise src.error.error.Error(
        fastapi.status.HTTP_501_NOT_IMPLEMENTED,
        src.error.error_type.NOT_IMPLEMENTED
    )


@router.post(
    path="/info",
    summary="Create resource.",
    status_code=fastapi.status.HTTP_201_CREATED,
    responses=error_responses | {
        fastapi.status.HTTP_201_CREATED: {
            "model": src.dto.account.AccountPostInfoOut,
            "description": "Resource created."
        },
    }
)
async def account_post_info(
        jwt: src.dto.jwt.Jwt = src.depends.jwt.access.depends(),
        app_state: src.app_state.AppState = src.depends.app_state.depends(),
        dto: src.dto.account.AccountPostInfoIn = fastapi.Body(...)
):
    account: src.database.account.model.Account
    account = app_state.database.account.find_one(
        src.database.account.filter.identifier(
            jwt.sub
        )
    )

    if not account:
        raise src.error.error.Error(
            fastapi.status.HTTP_404_NOT_FOUND,
            src.error.error_type.NOT_FOUND_ACCOUNT
        )

    if account.info:
        raise src.error.error.Error(
            fastapi.status.HTTP_409_CONFLICT,
            src.error.error_type.CONFLICT_ACCOUNT_INFO
        )

    account.info = src.database.account.model.AccountInfo()
    account.info.alias = dto.alias
    account.info.gender = dto.gender
    account.info.birthdate = dto.birthdate

    if not app_state.database.account.update_one(
            account,
            {
                "$set": {
                    src.database.account.update.info
                }
            }
    ):
        raise src.error.error.Error(
            fastapi.status.HTTP_503_SERVICE_UNAVAILABLE,
            src.error.error_type.SERVICE_UNAVAILABLE_DATABASE
        )

    return src.dto.account.AccountPostInfoOut(
        alias=dto.alias,
        gender=dto.gender,
        birthdate=dto.birthdate
    )
