import base64
import datetime
import typing


class JwtUserEmail:
    value: str
    primary: bool
    confirmed: bool

    def to_json_dict(
            self
    ) -> dict:
        return {
            "v": self.value,
            "p": self.primary,
            "c": self.confirmed
        }

    @staticmethod
    def from_json_dict(
            d: dict,
            version: int
    ):
        i = JwtUserEmail()
        i.value = d["v"]
        i.primary = d["p"]
        i.confirmed = d["c"]
        return i


# TOP
class JwtUser:
    revision: int = 1

    identifier: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    emails: typing.List[JwtUserEmail]

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

    nonce: bytes
    signature: bytes

    def to_json_dict(
            self
    ) -> dict:
        return {
            "r": self.revision,
            "n": base64.b64encode(self.nonce),
            "s": base64.b64encode(self.signature),
        }

    @staticmethod
    def from_json_dict(
            d: dict
    ):
        i = JwtPasswordRecover()
        i.revision = d["r"]
        i.nonce = base64.b64decode(d["n"])
        i.signature = base64.b64decode(d["s"])
