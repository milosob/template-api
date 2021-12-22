import base64
import datetime
import hmac
import os
import typing

import fastapi

import src.database.account.model
import src.error.error_type
import src.error


class JwtUserContactEmail:
    email: str
    primary: bool
    confirmed: bool

    def to_json_dict(
            self
    ) -> dict:
        return {
            "e": self.email,
            "p": 1 if self.primary else 0,
            "c": 1 if self.confirmed else 0
        }

    @staticmethod
    def from_json_dict(
            d: dict,
            revision: int
    ):
        i = JwtUserContactEmail()
        i.email = d["e"]
        i.primary = d["p"] == 1
        i.confirmed = d["c"] == 1
        return i

    @staticmethod
    def from_account(
            model: src.database.account.model.AccountContactEmail
    ):
        i = JwtUserContactEmail()
        i.email = model.email
        i.primary = model.primary
        i.confirmed = model.confirmed
        return i


class JwtUserContact:
    emails: typing.List[JwtUserContactEmail]

    def to_json_dict(
            self
    ) -> dict:
        return {
            "e": [email.to_json_dict() for email in self.emails]
        }

    @staticmethod
    def from_json_dict(
            d: dict,
            revision: int
    ):
        i = JwtUserContact()
        i.emails = [JwtUserContactEmail.from_json_dict(email, revision) for email in d["e"]]
        return i

    @staticmethod
    def from_account(
            model: src.database.account.model.AccountContact
    ):
        i = JwtUserContact()
        i.emails = [JwtUserContactEmail.from_account(email) for email in model.emails]
        return i


class JwtUserVerification:
    email: bool

    def to_json_dict(
            self
    ) -> dict:
        return {
            "e": 1 if self.email else 0
        }

    @staticmethod
    def from_json_dict(
            d: dict,
            revision: int
    ):
        i = JwtUserVerification()
        i.email = d["e"] == 1
        return i

    @staticmethod
    def from_account(
            model: src.database.account.model.AccountVerification
    ):
        i = JwtUserVerification()
        i.email = model.email
        return i


class JwtUser:
    revision: int = 1

    created_at: datetime.datetime
    updated_at: datetime.datetime
    contact: JwtUserContact
    verification: JwtUserVerification

    def to_json_dict(
            self
    ) -> dict:
        return {
            "r": self.revision,
            "c": int(self.created_at.timestamp()),
            "u": int(self.updated_at.timestamp()),
            "ct": self.contact.to_json_dict(),
            "vr": self.verification.to_json_dict()
        }

    @staticmethod
    def from_json_dict(
            d: dict
    ):
        revision = d["r"]

        i = JwtUser()
        i.revision = revision
        i.created_at = datetime.datetime.utcfromtimestamp(d["c"])
        i.updated_at = datetime.datetime.utcfromtimestamp(d["u"])
        i.contact = JwtUserContact.from_json_dict(d["ct"], revision)
        i.verification = JwtUserVerification.from_json_dict(d["vr"], revision)
        return i

    @staticmethod
    def from_account(
            model: src.database.account.model.Account
    ):
        i = JwtUser()
        i.created_at = model.created_at
        i.updated_at = model.updated_at
        i.contact = JwtUserContact.from_account(model.contact)
        i.verification = JwtUserVerification.from_account(model.verification)
        return i


# TOP
class JwtAccess:
    revision: int = 1

    user: JwtUser

    def to_json_dict(
            self
    ) -> dict:
        return {
            "r": self.revision,
            "u": self.user.to_json_dict(),
        }

    @staticmethod
    def from_json_dict(
            d: dict
    ):
        revision = d["r"]

        i = JwtAccess()
        i.revision = revision
        i.user = JwtUser.from_json_dict(d["u"])
        return i


# TOP
class JwtRefresh:
    revision: int = 1

    counter: int

    def to_json_dict(
            self
    ) -> dict:
        return {
            "r": self.revision,
            "c": self.counter
        }

    @staticmethod
    def from_json_dict(
            d: dict
    ):
        revision = d["r"]
        i = JwtRefresh()
        i.revision = revision
        i.counter = d["c"]
        return i


# TOP
class JwtRegister:
    revision: int = 1

    def to_json_dict(
            self
    ) -> dict:
        return {
            "r": self.revision
        }

    @staticmethod
    def from_json_dict(
            d: dict
    ):
        revision = d["r"]
        i = JwtRegister()
        i.revision = revision
        return i


class JwtPasswordRecover:
    revision: int = 1

    message: bytes
    signature: bytes

    def to_json_dict(
            self
    ) -> dict:
        return {
            "r": self.revision,
            "m": base64.b64encode(self.message).decode("utf-8"),
            "s": base64.b64encode(self.signature).decode("utf-8"),
        }

    @staticmethod
    def from_json_dict(
            d: dict
    ):
        revision = d["r"]
        i = JwtPasswordRecover()
        i.revision = revision
        i.message = base64.b64decode(d["m"])
        i.signature = base64.b64decode(d["s"])
        return i

    def sign(
            self,
            password: str
    ) -> None:
        if not self.message:
            self.message = os.urandom(16)

        self.signature = hmac.digest(
            password.encode("utf-8"),
            self.message,
            "sha256"
        )

    def verify(
            self,
            password: str
    ) -> bool:
        if self.revision == 1:
            return hmac.compare_digest(
                self.signature,
                hmac.digest(
                    password.encode("utf-8"),
                    self.message,
                    "sha256"
                )
            )
        return False


# TOP


class Jwt:
    sub: str

    register: JwtRegister
    register_scopes: typing.List[str]

    access: JwtAccess
    access_scopes: typing.List[str]

    refresh: JwtRefresh
    refresh_scopes: typing.List[str]

    password_recover: JwtPasswordRecover
    password_recover_scopes: typing.List[str]

    def __init__(
            self
    ) -> None:
        pass

    def load_sub(
            self,
            payload: dict
    ) -> None:
        try:
            if self.sub != payload["sub"]:
                raise src.error.error.Error(
                    fastapi.status.HTTP_401_UNAUTHORIZED,
                    src.error.error_type.UNAUTHORIZED_HEADER_SUB_CONFLICT
                )
        except AttributeError:
            self.sub = payload["sub"]

    def load_access(
            self,
            payload: dict
    ) -> None:
        self.load_sub(payload)
        self.access = JwtAccess.from_json_dict(payload["data"])
        self.access_scopes = payload["scopes"]

    def load_refresh(
            self,
            payload: dict
    ) -> None:
        self.load_sub(payload)
        self.refresh = JwtRefresh.from_json_dict(payload["data"])
        self.refresh_scopes = payload["scopes"]

    def load_register(
            self,
            payload: dict
    ) -> None:
        self.load_sub(payload)
        self.register = JwtRegister.from_json_dict(payload["data"])
        self.register_scopes = payload["scopes"]

    def load_password_recover(
            self,
            payload: dict
    ) -> None:
        self.load_sub(payload)
        self.password_recover = JwtPasswordRecover.from_json_dict(payload["data"])
        self.password_recover_scopes = payload["scopes"]
