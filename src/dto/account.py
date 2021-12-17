import typing

import fastapi
import pydantic


# POST ACCOUNT REGISTER

# noinspection PyMethodParameters
class AccountPostRegisterInBase(pydantic.BaseModel):
    username: str = fastapi.Body(
        ...
    )
    password: str = fastapi.Body(
        ...
    )

    @pydantic.validator("username")
    def validator_username(
            cls,
            v: str
    ) -> str:
        # TODO

        return v

    @pydantic.validator("password")
    def validator_password(
            cls,
            v: str
    ) -> str:
        # TODO

        return v


class AccountPostRegisterIn(AccountPostRegisterInBase):
    pass


class AccountPostRegisterOutBase(pydantic.BaseModel):
    username: str
    password: typing.Optional[str]


class AccountPostRegisterOut(AccountPostRegisterOutBase):
    pass


# POST ACCOUNT REGISTER CONFIRM

class AccountPostRegisterConfirmInBase(pydantic.BaseModel):
    pass


class AccountPostRegisterConfirmIn(AccountPostRegisterConfirmInBase):
    pass


class AccountPostRegisterConfirmOutBase(pydantic.BaseModel):
    pass


class AccountPostRegisterConfirmOut(AccountPostRegisterConfirmOutBase):
    pass


# POST ACCOUNT AUTHENTICATE

# noinspection PyMethodParameters
class AccountPostAuthenticateInBase(pydantic.BaseModel):
    username: str = fastapi.Body(
        ...
    )
    password: str = fastapi.Body(
        ...
    )

    @pydantic.validator("username")
    def validator_username(
            cls,
            v: str
    ) -> str:
        # TODO

        return v

    @pydantic.validator("password")
    def validator_password(
            cls,
            v: str
    ) -> str:
        # TODO

        return v


class AccountPostAuthenticateIn(AccountPostAuthenticateInBase):
    pass


class AccountPostAuthenticateOutBase(pydantic.BaseModel):
    access_token: str
    refresh_token: str


class AccountPostAuthenticateOut(AccountPostAuthenticateOutBase):
    pass


# POST ACCOUNT AUTHENTICATE REFRESH

# noinspection PyMethodParameters
class AccountPostAuthenticateRefreshInBase(pydantic.BaseModel):
    access_token: str
    refresh_token: str

    @pydantic.validator("access_token")
    def validator_access_token(
            cls,
            v: str
    ) -> str:
        # TODO

        return v

    @pydantic.validator("refresh_token")
    def validator_refresh_token(
            cls,
            v: str
    ) -> str:
        # TODO

        return v


class AccountPostAuthenticateRefreshIn(AccountPostAuthenticateRefreshInBase):
    pass


class AccountPostAuthenticateRefreshOutBase(pydantic.BaseModel):
    access_token: str
    refresh_token: str


class AccountPostAuthenticateRefreshOut(AccountPostAuthenticateRefreshOutBase):
    pass


# POST ACCOUNT PASSWORD FORGET

# noinspection PyMethodParameters
class AccountPostPasswordForgetInBase(pydantic.BaseModel):
    username: str

    @pydantic.validator("username")
    def validator_username(
            cls,
            v: str
    ) -> str:
        # TODO

        return v


class AccountPostPasswordForgetIn(AccountPostPasswordForgetInBase):
    pass


class AccountPostPasswordForgetOutBase(pydantic.BaseModel):
    pass


class AccountPostPasswordForgetOut(AccountPostPasswordForgetOutBase):
    pass


# POST ACCOUNT PASSWORD RECOVER

# noinspection PyMethodParameters
class AccountPostPasswordRecoverInBase(pydantic.BaseModel):
    password: str

    @pydantic.validator("password")
    def validator_password(
            cls,
            v: str
    ) -> str:
        # TODO

        return v


class AccountPostPasswordRecoverIn(AccountPostPasswordRecoverInBase):
    pass


class AccountPostPasswordRecoverOutBase(pydantic.BaseModel):
    password: typing.Optional[str]


class AccountPostPasswordRecoverOut(AccountPostPasswordRecoverOutBase):
    pass
