import datetime
import typing


class AccountContactEmail:
    email: str = None
    primary: bool = False
    confirmed: bool = False

    def to_mongo_dict(
            self
    ) -> dict:
        return {
            "email": self.email,
            "primary": self.primary,
            "confirmed": self.confirmed
        }

    @staticmethod
    def from_mongo_dict(
            d: dict
    ):
        i = AccountContactEmail()
        i.email = d["email"]
        i.primary = d["primary"]
        i.confirmed = d["confirmed"]
        return i


class AccountContact:
    emails: typing.List[AccountContactEmail] = []

    def to_mongo_dict(
            self
    ) -> dict:
        return {
            "emails": [x.to_mongo_dict() for x in self.emails]
        }

    @staticmethod
    def from_mongo_dict(
            d: dict,
            r: int
    ):
        i = AccountContact()
        i.emails = [AccountContactEmail.from_mongo_dict(x) for x in d["emails"]]
        return i


class AccountInfo:
    alias: str = None
    gender: str = None
    birthdate: datetime.datetime = None

    def to_mongo_dict(
            self
    ) -> dict:
        return {
            "alias": self.alias,
            "gender": self.gender,
            "birthdate": self.birthdate
        }

    @staticmethod
    def from_mongo_dict(
            d: dict,
            r: int
    ):
        if not d:
            return None

        i = AccountInfo()
        i.alias = d["alias"]
        i.gender = d["gender"]
        i.birthdate = d["birthdate"]
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


class Account:
    revision: int = 1
    identifier: str = None
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None

    contact: AccountContact = AccountContact()

    info: AccountInfo = None

    verification: AccountVerification = AccountVerification()

    authentication: AccountAuthentication = AccountAuthentication()

    def to_mongo_dict(
            self
    ) -> dict:
        return {
            "_rev": self.revision,
            "_id": self.identifier,
            "_cat": self.created_at,
            "_uat": self.updated_at,
            "contact": self.contact.to_mongo_dict(),
            "info": self.info.to_mongo_dict() if self.info else None,
            "verification": self.verification.to_mongo_dict(),
            "authentication": self.authentication.to_mongo_dict(),
        }

    @staticmethod
    def from_mongo_dict(
            d: dict
    ):
        revision: int = d["_rev"]

        i = Account()
        i.revision = revision
        i.identifier = d["_id"]
        i.created_at = d["_cat"]
        i.updated_at = d["_uat"]

        i.contact = AccountContact.from_mongo_dict(d["contact"], revision)
        i.info = AccountInfo.from_mongo_dict(d["info"], revision)
        i.verification = AccountVerification.from_mongo_dict(d["verification"])
        i.authentication = AccountAuthentication.from_mongo_dict(d["authentication"])

        return i
