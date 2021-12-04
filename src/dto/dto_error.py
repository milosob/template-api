import datetime

import fastapi
import pydantic


class DtoErrorApiOutBase(pydantic.BaseModel):
    code: int
    type: str
    occurred_at: datetime.datetime


class DtoErrorApiOut(DtoErrorApiOutBase):
    pass
