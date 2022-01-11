import datetime
import typing

import fastapi
import pydantic

import src.validator.account


# ACCOUNT POST  REGISTER

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
        v = src.validator.account.username(v)
        return v

    @pydantic.validator("password")
    def validator_password(
            cls,
            v: str
    ) -> str:
        v = src.validator.account.password(v)
        return v


class AccountPostRegisterIn(AccountPostRegisterInBase):
    pass


class AccountPostRegisterOutBase(pydantic.BaseModel):
    username: str
    password: typing.Optional[str]


class AccountPostRegisterOut(AccountPostRegisterOutBase):
    pass


# ACCOUNT POST  REGISTER CONFIRM

class AccountPostRegisterConfirmInBase(pydantic.BaseModel):
    pass


class AccountPostRegisterConfirmIn(AccountPostRegisterConfirmInBase):
    pass


class AccountPostRegisterConfirmOutBase(pydantic.BaseModel):
    pass


class AccountPostRegisterConfirmOut(AccountPostRegisterConfirmOutBase):
    pass


# ACCOUNT POST  AUTHENTICATE

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
        v = src.validator.account.username(v)
        return v

    @pydantic.validator("password")
    def validator_password(
            cls,
            v: str
    ) -> str:
        v = src.validator.account.password(v)
        return v


class AccountPostAuthenticateIn(AccountPostAuthenticateInBase):
    pass


class AccountPostAuthenticateOutBase(pydantic.BaseModel):
    access_token: str
    refresh_token: str


class AccountPostAuthenticateOut(AccountPostAuthenticateOutBase):
    pass


# ACCOUNT POST  AUTHENTICATE REFRESH

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


# ACCOUNT POST  PASSWORD FORGET

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


# ACCOUNT POST PASSWORD RECOVER

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


# ACCOUNT GET INFO
class AccountGetInfoInBase(pydantic.BaseModel):
    pass


class AccountGetInfoIn(AccountGetInfoInBase):
    pass


class AccountGetInfoOutBase(pydantic.BaseModel):
    alias: str
    gender: str
    birthdate: datetime.datetime


class AccountGetInfoOut(AccountGetInfoOutBase):
    pass


# ACCOUNT PUT INFO
class AccountPutInfoInBase(pydantic.BaseModel):
    alias: typing.Optional[str] = fastapi.Body(
        None
    )
    gender: typing.Optional[str] = fastapi.Body(
        None
    )
    birthdate: typing.Optional[datetime.datetime] = fastapi.Body(
        None
    )

    @pydantic.root_validator(pre=True)
    def validator_root(
            cls,
            v: dict
    ) -> dict:
        all_null_guard: bool
        all_null_guard = True

        for key, value in v.items():
            if value:
                all_null_guard = False

        if all_null_guard:
            raise ValueError("At least one field is required to perform resource update.")

        return v

    @pydantic.validator("alias")
    def validator_alias(
            self,
            v: str
    ) -> str:
        if v:
            v = src.validator.account.alias(v)
        return v

    @pydantic.validator("gender")
    def validator_gender(
            self,
            v: str
    ) -> str:
        if v:
            v = src.validator.account.gender(v)
        return v

    @pydantic.validator("birthdate")
    def validator_birthdate(
            self,
            v: datetime.datetime
    ) -> datetime.datetime:
        if v:
            v = src.validator.account.birthdate(v)
        return v


class AccountPutInfoIn(AccountPutInfoInBase):
    pass


class AccountPutInfoOutBase(pydantic.BaseModel):
    alias: typing.Optional[str]
    gender: typing.Optional[str]
    birthdate: typing.Optional[datetime.datetime]


class AccountPutInfoOut(AccountPutInfoOutBase):
    pass


# ACCOUNT POST INFO

# noinspection PyMethodParameters
class AccountPostInfoInBase(pydantic.BaseModel):
    alias: str = fastapi.Body(
        ...
    )
    gender: str = fastapi.Body(
        ...
    )
    birthdate: datetime.datetime = fastapi.Body(
        ...
    )

    @pydantic.validator("alias")
    def validator_alias(
            cls,
            v: str
    ) -> str:
        v = src.validator.account.alias(v)
        return v

    @pydantic.validator("gender")
    def validator_gender(
            cls,
            v: str
    ) -> str:
        v = src.validator.account.gender(v)
        return v

    @pydantic.validator("birthdate")
    def validator_birthdate(
            cls,
            v: datetime.datetime
    ) -> datetime.datetime:
        v = src.validator.account.birthdate(v)
        return v


class AccountPostInfoIn(AccountPostInfoInBase):
    pass


class AccountPostInfoOutBase(pydantic.BaseModel):
    alias: str
    gender: typing.Optional[str]
    birthdate: typing.Optional[datetime.datetime]


class AccountPostInfoOut(AccountPostInfoOutBase):
    pass
