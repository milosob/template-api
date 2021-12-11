import datetime
import typing


class Base(dict):
    pass


# ACCOUNT EMAIL
class AccountEmail(Base):
    value: str = None
    primary: bool = False
    confirmed: bool = False


# ACCOUNT AUTHENTICATION PASSWORD
class AccountAuthenticationPassword(Base):
    value: str = None


class AccountAuthenticationPasswords(Base):
    primary: AccountAuthenticationPassword = AccountAuthenticationPassword()


# ACCOUNT AUTHENTICATION
class AccountAuthentication(Base):
    passwords: AccountAuthenticationPasswords = AccountAuthenticationPasswords()


class AccountVerification(Base):
    basic: bool = False


class Account(Base):
    _id: typing.Any = None
    _rev: int = 1

    emails: typing.List[AccountEmail] = []

    verification: AccountVerification = AccountVerification()

    authentication: AccountAuthentication = AccountAuthentication()

    created_at: typing.Union[datetime.datetime, None] = None
    updated_at: typing.Union[datetime.datetime, None] = None

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
        self.created_at = date
        self.updated_at = date

    def notify_update(
            self,
            date: datetime.datetime = datetime.datetime.utcnow()
    ) -> None:
        self.updated_at = date
