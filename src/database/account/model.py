import datetime
import typing


# ACCOUNT EMAIL
class AccountEmailRecord:
    value: str
    confirmed: bool


class AccountEmail:
    primary: AccountEmailRecord
    alternative: typing.List[AccountEmailRecord]


# ACCOUNT AUTHENTICATION PASSWORD
class AccountAuthenticationPasswordRecord:
    value: str


class AccountAuthenticationPassword:
    primary: AccountAuthenticationPasswordRecord


# ACCOUNT AUTHENTICATION
class AccountAuthentication:
    password: AccountAuthenticationPassword


class Account:
    # BASIC USER INFO
    identifier: str

    # BASIC USER TIME
    created_at: typing.Union[datetime.datetime, None]
    changed_at: typing.Union[datetime.datetime, None]
    removed_at: typing.Union[datetime.datetime, None]

    # ACCOUNT EMAIL
    email: AccountEmail

    # ACCOUNT AUTHENTICATION
    authentication: AccountAuthentication

    def __init__(
            self
    ) -> None:
        self.identifier = None
        self.created_at = None
        self.changed_at = None
        self.removed_at = None

        self.email = AccountEmail()
        self.email.primary = AccountEmailRecord()
        self.email.alternative = []

        self.authentication = AccountAuthentication()
        self.authentication.password = AccountAuthenticationPassword()
        self.authentication.password.primary = AccountAuthenticationPasswordRecord()
