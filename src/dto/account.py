import typing

import fastapi
import pydantic


# POST ACCOUNT REGISTER PRIVATE

class PostAccountRegisterInBase(pydantic.BaseModel):
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


class PostAccountRegisterOutBase(pydantic.BaseModel):
    username: str
    password: typing.Optional[str]


# POST ACCOUNT REGISTER PUBLIC

class PostAccountRegisterIn(PostAccountRegisterInBase):
    pass


class PostAccountRegisterOut(PostAccountRegisterOutBase):
    pass


# POST ACCOUNT AUTHENTICATE PRIVATE

class PostAccountAuthenticateInBase(pydantic.BaseModel):
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


class PostAccountAuthenticateOutBase(pydantic.BaseModel):
    access_token: str
    refresh_token: str


# POST ACCOUNT AUTHENTICATE PUBLIC

class PostAccountAuthenticateIn(PostAccountAuthenticateInBase):
    pass


class PostAccountAuthenticateOut(PostAccountAuthenticateOutBase):
    pass


# POST ACCOUNT AUTHENTICATE REFRESH PRIVATE

class PostAccountAuthenticateRefreshInBase(pydantic.BaseModel):
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


class PostAccountAuthenticateRefreshOutBase(pydantic.BaseModel):
    access_token: str
    refresh_token: str


# POST ACCOUNT AUTHENTICATE REFRESH PUBLIC

class PostAccountAuthenticateRefreshIn(PostAccountAuthenticateRefreshInBase):
    pass


class PostAccountAuthenticateRefreshOut(PostAccountAuthenticateRefreshOutBase):
    pass


# POST ACCOUNT PASSWORD FORGET PRIVATE

class PostAccountPasswordForgetInBase(pydantic.BaseModel):
    username: str

    @pydantic.validator("username")
    def validator_username(
            cls,
            v: str
    ) -> str:
        # TODO

        return v


class PostAccountPasswordForgetOutBase(pydantic.BaseModel):
    pass


# POST ACCOUNT PASSWORD FORGET PUBLIC

class PostAccountPasswordForgetIn(PostAccountPasswordForgetInBase):
    pass


class PostAccountPasswordForgetOut(PostAccountPasswordForgetOutBase):
    pass


# POST ACCOUNT PASSWORD RECOVER PRIVATE

class PostAccountPasswordRecoverInBase(pydantic.BaseModel):
    password: str

    @pydantic.validator("password")
    def validator_password(
            cls,
            v: str
    ) -> str:
        # TODO

        return v


class PostAccountPasswordRecoverOutBase(pydantic.BaseModel):
    password: str


# POST ACCOUNT PASSWORD RECOVER PUBLIC

class PostAccountPasswordRecoverIn(PostAccountPasswordRecoverInBase):
    pass


class PostAccountPasswordRecoverOut(PostAccountPasswordRecoverOutBase):
    pass
