import typing

import fastapi
import pydantic


# POST ACCOUNT REGISTER PRIVATE

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


class AccountPostRegisterOutBase(pydantic.BaseModel):
    username: str
    password: typing.Optional[str]


# POST ACCOUNT REGISTER PUBLIC

class AccountPostRegisterIn(AccountPostRegisterInBase):
    pass


class AccountPostRegisterOut(AccountPostRegisterOutBase):
    pass


# POST ACCOUNT REGISTER CONFIRM PRIVATE

class AccountPostRegisterConfirmInBase(pydantic.BaseModel):
    pass


class AccountPostRegisterConfirmOutBase(pydantic.BaseModel):
    pass


# POST ACCOUNT REGISTER CONFIRM PUBLIC

class AccountPostRegisterConfirmIn(AccountPostRegisterConfirmInBase):
    pass


class AccountPostRegisterConfirmOut(AccountPostRegisterConfirmOutBase):
    pass


# POST ACCOUNT AUTHENTICATE PRIVATE

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


class AccountPostAuthenticateOutBase(pydantic.BaseModel):
    access_token: str
    refresh_token: str


# POST ACCOUNT AUTHENTICATE PUBLIC

class AccountPostAuthenticateIn(AccountPostAuthenticateInBase):
    pass


class AccountPostAuthenticateOut(AccountPostAuthenticateOutBase):
    pass


# POST ACCOUNT AUTHENTICATE REFRESH PRIVATE

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


class AccountPostAuthenticateRefreshOutBase(pydantic.BaseModel):
    access_token: str
    refresh_token: str


# POST ACCOUNT AUTHENTICATE REFRESH PUBLIC

class AccountPostAuthenticateRefreshIn(AccountPostAuthenticateRefreshInBase):
    pass


class AccountPostAuthenticateRefreshOut(AccountPostAuthenticateRefreshOutBase):
    pass


# POST ACCOUNT PASSWORD FORGET PRIVATE

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


class AccountPostPasswordForgetOutBase(pydantic.BaseModel):
    pass


# POST ACCOUNT PASSWORD FORGET PUBLIC

class AccountPostPasswordForgetIn(AccountPostPasswordForgetInBase):
    pass


class AccountPostPasswordForgetOut(AccountPostPasswordForgetOutBase):
    pass


# POST ACCOUNT PASSWORD RECOVER PRIVATE

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


class AccountPostPasswordRecoverOutBase(pydantic.BaseModel):
    password: typing.Optional[str]


# POST ACCOUNT PASSWORD RECOVER PUBLIC

class AccountPostPasswordRecoverIn(AccountPostPasswordRecoverInBase):
    pass


class AccountPostPasswordRecoverOut(AccountPostPasswordRecoverOutBase):
    pass
