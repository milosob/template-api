import datetime
import typing


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
        i = AccountEmail()
        i.value = d["value"]
        i.primary = d["primary"]
        i.confirmed = d["confirmed"]
        return i


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
        i = AccountAuthenticationPassword()
        i.value = d["value"]
        return i


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
        i = AccountAuthenticationPasswords()
        i.primary = AccountAuthenticationPassword.from_mongo_dict(d["primary"])
        return i


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
        i = AccountAuthentication()
        i.passwords = AccountAuthenticationPasswords.from_mongo_dict(d["passwords"])
        return i


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
        i = AccountVerification()
        i.email = d["email"]
        return i


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
        i = Account()
        i._id = d["_id"]
        i._ver = d["_ver"]
        i._cat = d["_cat"]
        i._uat = d["_uat"]
        i.emails = [AccountEmail.from_mongo_dict(x) for x in d["emails"]]
        i.verification = AccountVerification.from_mongo_dict(d["verification"])
        i.authentication = AccountAuthentication.from_mongo_dict(d["authentication"])
        return i
