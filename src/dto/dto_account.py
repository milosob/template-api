import typing

import fastapi
import pydantic

import fastapi.security


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
    token: str
    token_type: str


# POST ACCOUNT AUTHENTICATE PUBLIC

class DtoPostAccountAuthenticateIn(DtoPostAccountAuthenticateInBase):
    pass


class DtoPostAccountAuthenticateOut(DtoPostAccountAuthenticateOutBase):
    pass
