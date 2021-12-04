import datetime
import typing


class DatabaseAccountEmailRegRecordModel:
    email: str
    primary: bool
    confirmed_at: datetime.datetime


class DatabaseAccountEmailRegModel:
    primary: DatabaseAccountEmailRegRecordModel
    records: typing.List[DatabaseAccountEmailRegRecordModel]


class DatabaseAccountEmailLogRecordModel:
    email: str
    confirmed_at: datetime.datetime

    type: str
    context: object
    occurred_at: datetime.datetime


class DatabaseAccountEmailLogModel:
    records: typing.List[DatabaseAccountEmailLogRecordModel]


class DatabaseAccountEmailModel:
    reg: DatabaseAccountEmailRegModel
    log: DatabaseAccountEmailLogModel


class DatabaseAccountAuthenticationPasswordRegRecordModel:
    password: str


class DatabaseAccountAuthenticationPasswordRegModel:
    primary: DatabaseAccountAuthenticationPasswordRegRecordModel


class DatabaseAccountAuthenticationPasswordLogRecordModel:
    password: str

    type: str
    context: object
    occurred_at: datetime.datetime


class DatabaseAccountAuthenticationPasswordLogModel:
    records: typing.List[DatabaseAccountEmailLogRecordModel]


class DatabaseAccountAuthenticationModel:
    password_reg: DatabaseAccountAuthenticationPasswordRegModel
    password_log: DatabaseAccountAuthenticationPasswordLogModel


class DatabaseAccountModel:
    # BASIC USER INFO
    identifier: str

    # BASIC USER TIME
    created_at: datetime.datetime
    changed_at: datetime.datetime

    # ACCOUNT EMAIL
    email: DatabaseAccountEmailModel

    # ACCOUNT AUTHENTICATION
    authentication: DatabaseAccountAuthenticationModel

    def __init__(
            self
    ) -> None:
        email = DatabaseAccountEmailModel()
        email.reg = DatabaseAccountEmailRegModel()
        email.reg.primary = DatabaseAccountEmailRegRecordModel()
        email.reg.records = []
        email.log = DatabaseAccountEmailLogModel()
        email.log.records = []

        self.email = email

        authentication = DatabaseAccountAuthenticationModel()
        authentication.password_reg = DatabaseAccountAuthenticationPasswordRegModel()
        authentication.password_reg.primary = DatabaseAccountAuthenticationPasswordRegRecordModel()
        authentication.password_log = DatabaseAccountAuthenticationPasswordLogModel()
        authentication.password_log.records = []

        self.authentication = authentication
