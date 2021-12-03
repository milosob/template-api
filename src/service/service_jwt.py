import time
import typing

import jose
import jose.jwt


class ServiceJwt:
    config: dict

    issuer: str
    sign_key: str
    sign_alg: str
    validation_options: dict

    lifetime: int
    lifetime_bump: int
    lifetime_bump_threshold: int

    scopes_god: typing.List[str]
    scopes_refresh: typing.List[str]

    def __init__(
            self,
            config: dict
    ):
        self.config = config

        self.issuer = config["issuer"]
        self.sign_key = config["sign_key"]
        self.sign_alg = config["sign_alg"]
        self.validation_options = config["validation_options"]

        self.lifetime = config["lifetime"]
        self.lifetime_bump = config["lifetime_bump"]
        self.lifetime_bump_threshold = config["lifetime_bump_threshold"]

        self.scopes_god = config["scopes_god"]
        self.scopes_refresh = config["scopes_refresh"]

    def _issue(
            self,
            payload: dict
    ) -> str:
        token: str
        token = jose.jwt.encode(
            claims=payload,
            key=self.sign_key,
            algorithm=self.sign_alg
        )
        return token

    def _verify(
            self,
            token: str
    ) -> dict:
        payload: dict
        payload = jose.jwt.decode(
            token=token,
            key=self.sign_key,
            algorithms=[self.sign_alg],
            issuer=self.issuer,
            options=self.validation_options
        )
        return payload

    def issue(
            self,
            sub: str,
            data: dict,
            scopes: typing.List[str]
    ) -> str:
        timestamp_now: int
        timestamp_now = int(time.time())

        payload: dict
        payload = {
            "iss": self.issuer,
            "iat": timestamp_now,
            "exp": timestamp_now + self.lifetime,
            "sub": sub,
            "data": data,
            "scopes": scopes
        }

        token: str
        token = self._issue(
            payload=payload
        )

        return token

    def verify(
            self,
            token: str,
            required_scopes: typing.List[str]
    ) -> dict:
        payload: dict

        try:
            payload = self._verify(
                token=token
            )
        except jose.JWTError:
            # TODO Unauthorized.
            raise Exception()

        scopes: typing.List[str]
        scopes = payload.get("scopes", [])

        # Check for god mode.
        for scope in self.scopes_god:
            if scope in scopes:
                return payload

        # Check for required scopes.
        for scope in required_scopes:
            if scope not in scopes:
                # TODO Unauthorized.
                raise Exception()

        return payload

    def refresh(
            self,
            token: str,
    ) -> str:
        payload = self.verify(
            token=token,
            required_scopes=self.scopes_refresh
        )

        iat: int
        iat = payload.get("iat")

        exp: int
        exp = payload.get("exp")

        # If expires at is greater than bump time border, raise.
        if exp >= iat + self.lifetime_bump_threshold:
            # TODO Unauthorized.
            raise Exception()

        payload["exp"] = exp + self.lifetime_bump

        token: str
        token = self._issue(
            payload=payload
        )

        return token
