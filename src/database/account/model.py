import datetime
import typing


class Base(dict):
    pass


class AccountEmail:
    value: str = None
    primary: bool = False
    confirmed: bool = False

    def to_mongo_dict(
            self
    ) -> dict:
        return {
            "value": self.value,
            "primary": self.primary,
            "confirmed": self.confirmed
        }

    @staticmethod
    def from_mongo_dict(
            d: dict
    ):
        instance = AccountEmail()
        instance.value = d["value"]
        instance.primary = d["primary"]
        instance.confirmed = d["confirmed"]
        return instance


class AccountAuthenticationPassword:
    value: str = None

    def to_mongo_dict(
            self
    ) -> dict:
        return {
            "value": self.value,
        }

    @staticmethod
    def from_mongo_dict(
            d: dict
    ):
        instance = AccountAuthenticationPassword()
        instance.value = d["value"]
        return instance


class AccountAuthenticationPasswords:
    primary: AccountAuthenticationPassword = AccountAuthenticationPassword()

    def to_mongo_dict(
            self
    ) -> dict:
        return {
            "primary": self.primary.to_mongo_dict(),
        }

    @staticmethod
    def from_mongo_dict(
            d: dict
    ):
        instance = AccountAuthenticationPasswords()
        instance.primary = AccountAuthenticationPassword.from_mongo_dict(d["primary"])
        return instance


class AccountAuthentication:
    passwords: AccountAuthenticationPasswords = AccountAuthenticationPasswords()

    def to_mongo_dict(
            self
    ) -> dict:
        return {
            "passwords": self.passwords.to_mongo_dict(),
        }

    @staticmethod
    def from_mongo_dict(
            d: dict
    ):
        instance = AccountAuthentication()
        instance.passwords = AccountAuthenticationPasswords.from_mongo_dict(d["passwords"])
        return instance


class AccountVerification:
    email: bool = False

    def to_mongo_dict(
            self
    ) -> dict:
        return {
            "email": self.email
        }

    @staticmethod
    def from_mongo_dict(
            d: dict
    ):
        instance = AccountVerification()
        instance.email = d["email"]
        return instance


class Account:
    _id: str = None
    _ver: int = 1
    _cat: typing.Union[datetime.datetime, None] = None
    _uat: typing.Union[datetime.datetime, None] = None

    emails: typing.List[AccountEmail] = []

    verification: AccountVerification = AccountVerification()

    authentication: AccountAuthentication = AccountAuthentication()

    @property
    def identifier(
            self
    ) -> typing.Union[str, None]:
        return self._id

    @property
    def created_at(
            self
    ) -> typing.Union[datetime.datetime, None]:
        return self._cat

    @property
    def updated_at(
            self
    ) -> typing.Union[datetime.datetime, None]:
        return self._uat

    def notify_create(
            self,
            date: datetime.datetime = datetime.datetime.utcnow()
    ) -> None:
        self._cat = date
        self._uat = date

    def notify_update(
            self,
            date: datetime.datetime = datetime.datetime.utcnow()
    ) -> None:
        self._uat = date

    def to_mongo_dict(
            self
    ) -> dict:
        return {
            "_id": self._id,
            "_ver": self._ver,
            "_cat": self._cat,
            "_uat": self._uat,
            "emails": [x.to_mongo_dict() for x in self.emails],
            "verification": self.verification.to_mongo_dict(),
            "authentication": self.authentication.to_mongo_dict(),
        }

    @staticmethod
    def from_mongo_dict(
            d: dict
    ):
        instance = Account()
        instance._id = d["_id"]
        instance._ver = d["_ver"]
        instance._cat = d["_cat"]
        instance._uat = d["_uat"]
        instance.emails = [AccountEmail.from_mongo_dict(x) for x in d["emails"]]
        instance.verification = AccountVerification.from_mongo_dict(d["verification"])
        instance.authentication = AccountAuthentication.from_mongo_dict(d["authentication"])
        return instance
