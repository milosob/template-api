import datetime

import fastapi
import pydantic


class ErrorApiOutBase(pydantic.BaseModel):
    code: int
    type: str


class ErrorApiOut(ErrorApiOutBase):
    pass
