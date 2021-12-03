import fastapi
import pydantic


# POST CONFIRM PRIVATE

class DtoPostConfirmInBase(pydantic.BaseModel):
    token: str = fastapi.Body(
        ...
    )

    @pydantic.validator("token")
    def validator_token(
            cls,
            v: str
    ) -> str:
        # TODO

        return v


class DtoPostConfirmOutBase(pydantic.BaseModel):
    pass


# POST CONFIRM PUBLIC

class DtoPostConfirmIn(DtoPostConfirmInBase):
    pass


class DtoPostConfirmOut(DtoPostConfirmOutBase):
    pass
