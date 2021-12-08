import datetime
import typing


class AccountEmailRegRecord:
    email: str
    primary: bool
    confirmed_at: datetime.datetime


class AccountEmailReg:
    primary: AccountEmailRegRecord
    records: typing.List[AccountEmailRegRecord]


class AccountEmailLogRecord:
    email: str
    confirmed_at: datetime.datetime

    type: str
    context: object
    occurred_at: datetime.datetime


class AccountEmailLog:
    records: typing.List[AccountEmailLogRecord]


class AccountEmail:
    reg: AccountEmailReg
    log: AccountEmailLog


class AccountAuthenticationPasswordRegRecord:
    password: str


class AccountAuthenticationPasswordReg:
    primary: AccountAuthenticationPasswordRegRecord


class AccountAuthenticationPasswordLogRecord:
    password: str

    type: str
    context: object
    occurred_at: datetime.datetime


class AccountAuthenticationPasswordLog:
    records: typing.List[AccountEmailLogRecord]


class AccountAuthentication:
    password_reg: AccountAuthenticationPasswordReg
    password_log: AccountAuthenticationPasswordLog


class Account:
    # BASIC USER INFO
    identifier: str

    # BASIC USER TIME
    created_at: datetime.datetime
    changed_at: datetime.datetime

    # ACCOUNT EMAIL
    email: AccountEmail

    # ACCOUNT AUTHENTICATION
    authentication: AccountAuthentication

    def __init__(
            self
    ) -> None:
        email = AccountEmail()
        email.reg = AccountEmailReg()
        email.reg.primary = AccountEmailRegRecord()
        email.reg.records = []
        email.log = AccountEmailLog()
        email.log.records = []

        self.email = email

        authentication = AccountAuthentication()
        authentication.password_reg = AccountAuthenticationPasswordReg()
        authentication.password_reg.primary = AccountAuthenticationPasswordRegRecord()
        authentication.password_log = AccountAuthenticationPasswordLog()
        authentication.password_log.records = []

        self.authentication = authentication
