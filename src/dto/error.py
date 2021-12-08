import datetime

import fastapi
import pydantic


class ErrorApiOutBase(pydantic.BaseModel):
    code: int
    type: str
    occurred_at: datetime.datetime


class ErrorApiOut(ErrorApiOutBase):
    pass
