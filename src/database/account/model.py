import datetime
import typing


class Base(dict):
    pass


# ACCOUNT EMAIL

class AccountEmailRecord(Base):
    value: str
    confirmed: bool


class AccountEmail(Base):
    primary: AccountEmailRecord = AccountEmailRecord()
    records: typing.List[AccountEmailRecord] = []


# ACCOUNT AUTHENTICATION PASSWORD

class AccountAuthenticationPasswordRecord(Base):
    value: str


class AccountAuthenticationPassword(Base):
    primary: AccountAuthenticationPasswordRecord = AccountAuthenticationPasswordRecord()


# ACCOUNT AUTHENTICATION

class AccountAuthentication(Base):
    password: AccountAuthenticationPassword = AccountAuthenticationPassword()


class Account(Base):
    _id: typing.Any = None

    version: int = 1

    cat: typing.Union[datetime.datetime, None] = None
    uat: typing.Union[datetime.datetime, None] = None
    rat: typing.Union[datetime.datetime, None] = None

    email: AccountEmail = AccountEmail()

    authentication: AccountAuthentication = AccountAuthentication()

    @property
    def identifier(
            self
    ) -> typing.Union[str, None]:
        if self._id:
            return str(self._id)
        return None

    @identifier.setter
    def identifier(
            self,
            value: str
    ) -> None:
        self._id = value

    def notify_create(
            self,
            date: datetime.datetime = datetime.datetime.utcnow()
    ) -> None:
        self.cat = date
        self.uat = date

    def notify_update(
            self,
            date: datetime.datetime = datetime.datetime.utcnow()
    ) -> None:
        self.uat = date

    def notify_remove(
            self,
            date: datetime.datetime = datetime.datetime.utcnow()
    ) -> None:
        self.uat = date
        self.rat = date
