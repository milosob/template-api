import base64
import datetime
import hmac
import os
import typing
import fastapi

import src.database.account.model
import src.error.error_type
import src.error


class JwtUserEmail:
    value: str
    primary: bool
    confirmed: bool

    def __init__(
            self,
            value: typing.Optional[str] = None,
            primary: typing.Optional[bool] = False,
            confirmed: typing.Optional[bool] = False
    ) -> None:
        self.value = value
        self.primary = primary
        self.confirmed = confirmed

    def to_json_dict(
            self
    ) -> dict:
        return {
            "v": self.value,
            "p": 1 if self.primary else 0,
            "c": 1 if self.confirmed else 0
        }

    @staticmethod
    def from_json_dict(
            d: dict,
            revision: int
    ):
        return JwtUserEmail(
            d["v"],
            d["p"] == 1,
            d["c"] == 1
        )

    @staticmethod
    def from_account(
            model: src.database.account.model.AccountEmail
    ):
        return JwtUserEmail(
            model.value,
            model.primary,
            model.confirmed
        )


class JwtUserVerification:
    email: bool

    def __init__(
            self,
            email: typing.Optional[bool] = False
    ) -> None:
        self.email = email

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
        return JwtUserVerification(
            d["e"] == 1
        )

    @staticmethod
    def from_account(
            model: src.database.account.model.AccountVerification
    ):
        return JwtUserVerification(
            model.email
        )


class JwtUser:
    revision: int = 1

    identifier: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    emails: typing.List[JwtUserEmail]
    verification: JwtUserVerification

    def __init__(
            self,
            identifier: typing.Optional[str] = None,
            created_at: typing.Optional[datetime.datetime] = None,
            updated_at: typing.Optional[datetime.datetime] = None,
            emails: typing.Optional[typing.List[JwtUserEmail]] = None,
            verification: typing.Optional[JwtUserVerification] = None
    ) -> None:
        if emails is None:
            emails = []

        if verification is None:
            verification = JwtUserVerification()

        self.identifier = identifier
        self.created_at = created_at
        self.updated_at = updated_at
        self.emails = emails
        self.verification = verification

    def to_json_dict(
            self
    ) -> dict:
        return {
            "r": self.revision,
            "i": self.identifier,
            "c": int(self.created_at.timestamp()),
            "u": int(self.updated_at.timestamp()),
            "em": [
                email.to_json_dict()
                for email in self.emails
            ],
            "vr": self.verification.to_json_dict()
        }

    @staticmethod
    def from_json_dict(
            d: dict
    ):
        revision = d["r"]
        i = JwtUser(
            d["i"],
            datetime.datetime.utcfromtimestamp(d["c"]),
            datetime.datetime.utcfromtimestamp(d["u"]),
            [JwtUserEmail.from_json_dict(email, revision) for email in d["em"]],
            JwtUserVerification.from_json_dict(d["vr"], revision)
        )
        i.revision = revision
        return i

    @staticmethod
    def from_account(
            model: src.database.account.model.Account
    ):
        return JwtUser(
            model.identifier,
            model.created_at,
            model.updated_at,
            [JwtUserEmail.from_account(email) for email in model.emails],
            JwtUserVerification.from_account(model.verification)
        )


# TOP
class JwtRegister:
    revision: int = 1

    def __init__(
            self
    ) -> None:
        pass

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


# TOP
class JwtPasswordRecover:
    revision: int = 1

    identifier: str
    message: bytes
    signature: bytes

    def __init__(
            self,
            identifier: typing.Optional[str] = None,
            message: typing.Optional[bytes] = None,
            signature: typing.Optional[bytes] = None
    ) -> None:
        if not message:
            message = os.urandom(16)

        self.identifier = identifier
        self.message = message
        self.signature = signature

    def to_json_dict(
            self
    ) -> dict:
        return {
            "r": self.revision,
            "i": self.identifier,
            "m": base64.b64encode(self.message),
            "s": base64.b64encode(self.signature),
        }

    @staticmethod
    def from_json_dict(
            d: dict
    ):
        revision = d["r"]
        i = JwtPasswordRecover(
            d["i"],
            base64.b64decode(d["m"]),
            base64.b64decode(d["s"])
        )
        i.revision = revision
        return i

    def sign(
            self,
            password: str
    ) -> None:
        self.signature = hmac.digest(
            password.encode("utf-8") + self.identifier.encode("utf-8"),
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
                    password.encode("utf-8") + self.identifier.encode("utf-8"),
                    self.message,
                    "sha256"
                )
            )
        return False


# TOP
class JwtAccess:
    revision: int = 1

    user: JwtUser

    def __init__(
            self,
            user: typing.Optional[JwtUser] = None
    ):
        self.user = user

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
        i = JwtAccess(
            JwtUser.from_json_dict(d["u"])
        )
        i.revision = revision
        return i


# TOP
class JwtRefresh:
    revision: int = 1

    counter: int

    def __init__(
            self,
            counter: typing.Optional[int] = 0
    ) -> None:
        self.counter = counter

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
        i = JwtRefresh(
            d["c"]
        )
        i.revision = revision
        return i


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

    def load_register(
            self,
            payload: dict
    ) -> None:
        self.load_sub(payload)
        self.register = JwtRegister.from_json_dict(payload["data"])
        self.register_scopes = payload["scopes"]

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

    def load_password_recover(
            self,
            payload: dict
    ) -> None:
        self.load_sub(payload)
        self.password_recover = JwtPasswordRecover.from_json_dict(payload["data"])
        self.password_recover_scopes = payload["scopes"]
