import datetime
import typing


class DatabaseConfirmEmailModel:
    email: str


class DatabaseConfirmModel:
    identifier: str

    token: str

    issued_at: datetime.datetime
    expires_at: datetime.datetime
    confirmed_at: datetime.datetime

    type: str
    context: typing.Any
