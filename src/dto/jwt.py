import base64
import datetime
import hmac
import os
import typing


class JwtUserEmail:
    value: str
    primary: bool
    confirmed: bool

    def __init__(
            self,
            value: typing.Optional[str] = None,
            primary: typing.Optional[bool] = False,
            confirmed: typing.Optional[bool] = False
    ):
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
        i = JwtUserEmail()
        i.value = d["v"]
        i.primary = d["p"] == 1
        i.confirmed = d["c"] == 1
        return i


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
        i = JwtUserVerification()
        i.email = d["e"] == 1
        return i


# TOP
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
            emails=None,
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
            ]
        }

    @staticmethod
    def from_json_dict(
            d: dict
    ):
        i = JwtUser()
        i.revision = d["r"]
        i.identifier = d["i"]
        i.created_at = datetime.datetime.utcfromtimestamp(d["c"])
        i.updated_at = datetime.datetime.utcfromtimestamp(d["u"])
        i.emails = [JwtUserEmail.from_json_dict(email, i.revision) for email in d["em"]]
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
    ):
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
        i = JwtPasswordRecover()
        i.revision = d["r"]
        i.identifier = d["i"]
        i.message = base64.b64decode(d["n"])
        i.signature = base64.b64decode(d["s"])

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


class Jwt:
    user: JwtUser
    password_recover: JwtPasswordRecover
