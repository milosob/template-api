import typing


class DatabaseConfirmEmailModel:
    identifier: str
    email: str


class DatabaseConfirmModel:
    identifier: str

    created_at: int
    expires_at: int
    confirmed_at: int

    type: str
    context: typing.Any
