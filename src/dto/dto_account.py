import typing

import fastapi
import pydantic


# POST ACCOUNT REGISTER PRIVATE

class DtoPostAccountRegisterInBase(pydantic.BaseModel):
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


class DtoPostAccountRegisterOutBase(pydantic.BaseModel):
    username: str
    password: typing.Optional[str]


# POST ACCOUNT REGISTER PUBLIC

class DtoPostAccountRegisterIn(DtoPostAccountRegisterInBase):
    pass


class DtoPostAccountRegisterOut(DtoPostAccountRegisterOutBase):
    pass


# POST ACCOUNT AUTHENTICATE PRIVATE

class DtoPostAccountAuthenticateInBase(pydantic.BaseModel):
    username: str = fastapi.Body(
        ...
    )
    password: str = fastapi.Body(
        ...
    )
    scopes: typing.Optional[typing.List[str]] = fastapi.Body(
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

    @pydantic.validator("scopes")
    def validator_scopes(
            cls,
            v: str
    ) -> str:
        # TODO

        return v


class DtoPostAccountAuthenticateOutBase(pydantic.BaseModel):
    access_token: str
    refresh_token: str


# POST ACCOUNT AUTHENTICATE PUBLIC

class DtoPostAccountAuthenticateIn(DtoPostAccountAuthenticateInBase):
    pass


class DtoPostAccountAuthenticateOut(DtoPostAccountAuthenticateOutBase):
    pass


# POST ACCOUNT AUTHENTICATE REFRESH PRIVATE

class DtoPostAccountAuthenticateRefreshInBase(pydantic.BaseModel):
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


class DtoPostAccountAuthenticateRefreshOutBase(pydantic.BaseModel):
    access_token: str
    refresh_token: str


# POST ACCOUNT AUTHENTICATE REFRESH PUBLIC

class DtoPostAccountAuthenticateRefreshIn(DtoPostAccountAuthenticateRefreshInBase):
    pass


class DtoPostAccountAuthenticateRefreshOut(DtoPostAccountAuthenticateRefreshOutBase):
    pass


# POST ACCOUNT PASSWORD FORGET PRIVATE

class DtoPostAccountPasswordForgetInBase(pydantic.BaseModel):
    username: str

    @pydantic.validator("username")
    def validator_username(
            cls,
            v: str
    ) -> str:
        # TODO

        return v


class DtoPostAccountPasswordForgetOutBase(pydantic.BaseModel):
    pass


# POST ACCOUNT PASSWORD FORGET PUBLIC

class DtoPostAccountPasswordForgetIn(DtoPostAccountPasswordForgetInBase):
    pass


class DtoPostAccountPasswordForgetOut(DtoPostAccountPasswordForgetOutBase):
    pass


# POST ACCOUNT PASSWORD RECOVER PRIVATE

class DtoPostAccountPasswordRecoverInBase(pydantic.BaseModel):
    password: str

    @pydantic.validator("password")
    def validator_password(
            cls,
            v: str
    ) -> str:
        # TODO

        return v


class DtoPostAccountPasswordRecoverOutBase(pydantic.BaseModel):
    password: str


# POST ACCOUNT PASSWORD RECOVER PUBLIC

class DtoPostAccountPasswordRecoverIn(DtoPostAccountPasswordRecoverInBase):
    pass


class DtoPostAccountPasswordRecoverOut(DtoPostAccountPasswordRecoverOutBase):
    pass
