import typing

import passlib.hash


class ServicePassword:
    config: typing.Dict

    def __init__(
            self,
            config: typing.Dict
    ) -> None:
        self.config = config

    @staticmethod
    def password_hash(
            password: str
    ) -> str:
        return passlib.hash.argon2.using(
            salt_size=16,
            digest_size=32
        ).hash(
            password
        )

    @staticmethod
    def password_verify(
            password: str,
            password_hash: str
    ) -> bool:
        return passlib.hash.argon2.verify(
            password,
            password_hash
        )
