import calendar
import datetime
import typing

import fastapi

import jose
import jose.jwt

import src.error.error
import src.error.error_type


class ServiceJwt:
    config: dict

    issue_id: str
    issue_key: str
    issue_alg: str

    verify_ids: typing.List[str]
    verify_keys: typing.List[str]
    verify_algs: typing.List[str]

    access_lifetime: int
    refresh_lifetime: int

    verify_options: dict

    scopes_god: typing.List[str]

    def __init__(
            self,
            config: dict
    ):
        self.config = config

        self.issue_id = config["issue_id"]
        self.issue_key = config["issue_key"]
        self.issue_alg = config["issue_alg"]

        self.verify_ids = config["verify_ids"]
        self.verify_keys = config["verify_keys"]
        self.verify_algs = config["verify_algs"]

        self.access_lifetime = config["access_lifetime"]
        self.refresh_lifetime = config["refresh_lifetime"]

        self.scopes_god = config["scopes_god"]

    def issue(
            self,
            sub: str,
            data: dict,
            lifetime: int,
            scopes: typing.List[str]
    ) -> str:
        date_now: datetime.datetime
        date_now = datetime.datetime.utcnow()

        payload: dict
        payload = {
            "iss": self.issue_id,
            "sub": sub,
            "iat": date_now,
            "exp": date_now + datetime.timedelta(
                seconds=lifetime
            ),
            "data": data,
            "scopes": scopes
        }

        token: str
        token = jose.jwt.encode(
            claims=payload,
            key=self.issue_key,
            algorithm=self.issue_alg
        )

        return token

    def issue_access(
            self,
            sub: str,
            data: dict,
            scopes: typing.List[str]
    ) -> str:
        date_now: datetime.datetime
        date_now = datetime.datetime.utcnow()

        payload: dict
        payload = {
            "iss": self.issue_id,
            "sub": sub,
            "iat": date_now,
            "exp": date_now + datetime.timedelta(
                seconds=self.access_lifetime
            ),
            "data": data,
            "scopes": scopes + [
                "access"
            ]
        }

        token: str
        token = jose.jwt.encode(
            claims=payload,
            key=self.issue_key,
            algorithm=self.issue_alg,
            headers=None,
            access_token=None
        )

        return token

    def issue_refresh(
            self,
            sub: str,
            data: dict,
            scopes: typing.List[str],
            access_token: str
    ) -> str:
        date_now: datetime.datetime
        date_now = datetime.datetime.utcnow()

        payload: dict
        payload = {
            "iss": self.issue_id,
            "sub": sub,
            "iat": date_now,
            "exp": date_now + datetime.timedelta(
                seconds=self.refresh_lifetime
            ),
            "data": data,
            "scopes": scopes + [
                "refresh"
            ]
        }

        token: str
        token = jose.jwt.encode(
            claims=payload,
            key=self.issue_key,
            algorithm=self.issue_alg,
            headers=None,
            access_token=access_token
        )

        return token

    def verify_access(
            self,
            access_token: str,
            access_token_required_scopes: typing.List[str]
    ) -> dict:
        access_token_payload: dict

        try:
            access_token_payload = jose.jwt.decode(
                token=access_token,
                key=self.verify_keys,
                algorithms=self.verify_algs,
                options={
                    "verify_signature": True,
                    "verify_aud": False,
                    "verify_iat": False,
                    "verify_exp": False,
                    "verify_nbf": False,
                    "verify_iss": False,
                    "verify_sub": False,
                    "verify_jti": False,
                    "verify_at_hash": False,
                    "require_aud": False,
                    "require_iat": True,
                    "require_exp": True,
                    "require_nbf": False,
                    "require_iss": True,
                    "require_sub": True,
                    "require_jti": False,
                    "require_at_hash": False
                }
            )
        except jose.JWTError:
            raise src.error.error.Error(
                code=fastapi.status.HTTP_401_UNAUTHORIZED,
                type=src.error.error_type.AUTHORIZATION_ACCESS_TOKEN_INVALID
            )

        if access_token_payload["iss"] not in self.verify_ids:
            raise src.error.error.Error(
                code=fastapi.status.HTTP_401_UNAUTHORIZED,
                type=src.error.error_type.AUTHORIZATION_ACCESS_TOKEN_INVALID
            )

        date_now: datetime.datetime
        date_now = datetime.datetime.utcnow()

        if calendar.timegm(date_now.utctimetuple()) > access_token_payload["exp"]:
            raise src.error.error.Error(
                code=fastapi.status.HTTP_401_UNAUTHORIZED,
                type=src.error.error_type.AUTHORIZATION_ACCESS_TOKEN_EXPIRED
            )

        scopes: typing.List[str]
        scopes = access_token_payload.get("scopes", [])

        # Check for god mode.
        for scope in self.scopes_god:
            if scope in scopes:
                return access_token_payload

        # Check for required scopes.
        for scope in access_token_required_scopes:
            if scope not in scopes:
                raise src.error.error.Error(
                    code=fastapi.status.HTTP_401_UNAUTHORIZED,
                    type=src.error.error_type.AUTHORIZATION_ACCESS_TOKEN_INVALID
                )

        return access_token_payload

    def verify_refresh(
            self,
            access_token: str,
            refresh_token: str,
            refresh_token_required_scopes: typing.List[str]
    ) -> dict:
        access_token_payload: dict
        refresh_token_payload: dict

        try:
            access_token_payload = jose.jwt.decode(
                token=access_token,
                key=self.verify_keys,
                algorithms=self.verify_algs,
                options={
                    "verify_signature": True,
                    "verify_aud": False,
                    "verify_iat": False,
                    "verify_exp": False,
                    "verify_nbf": False,
                    "verify_iss": False,
                    "verify_sub": False,
                    "verify_jti": False,
                    "verify_at_hash": False,
                    "require_aud": False,
                    "require_iat": True,
                    "require_exp": True,
                    "require_nbf": False,
                    "require_iss": True,
                    "require_sub": True,
                    "require_jti": False,
                    "require_at_hash": False
                }
            )
        except jose.JWTError:
            raise src.error.error.Error(
                code=fastapi.status.HTTP_401_UNAUTHORIZED,
                type=src.error.error_type.AUTHORIZATION_ACCESS_TOKEN_INVALID
            )

        if access_token_payload["iss"] not in self.verify_ids:
            raise src.error.error.Error(
                code=fastapi.status.HTTP_401_UNAUTHORIZED,
                type=src.error.error_type.AUTHORIZATION_ACCESS_TOKEN_INVALID
            )

        try:
            refresh_token_payload = jose.jwt.decode(
                token=refresh_token,
                key=self.verify_keys,
                algorithms=self.verify_algs,
                options={
                    "verify_signature": True,
                    "verify_aud": False,
                    "verify_iat": False,
                    "verify_exp": False,
                    "verify_nbf": False,
                    "verify_iss": False,
                    "verify_sub": False,
                    "verify_jti": False,
                    "verify_at_hash": True,
                    "require_aud": False,
                    "require_iat": True,
                    "require_exp": True,
                    "require_nbf": False,
                    "require_iss": True,
                    "require_sub": True,
                    "require_jti": False,
                    "require_at_hash": True
                },
                access_token=access_token
            )
        except jose.JWTError:
            raise src.error.error.Error(
                code=fastapi.status.HTTP_401_UNAUTHORIZED,
                type=src.error.error_type.AUTHORIZATION_REFRESH_TOKEN_INVALID
            )

        if refresh_token_payload["iss"] not in self.verify_ids:
            raise src.error.error.Error(
                code=fastapi.status.HTTP_401_UNAUTHORIZED,
                type=src.error.error_type.AUTHORIZATION_REFRESH_TOKEN_INVALID
            )

        date_now: datetime.datetime
        date_now = datetime.datetime.utcnow()

        if calendar.timegm(date_now.utctimetuple()) > refresh_token_payload["exp"]:
            raise src.error.error.Error(
                code=fastapi.status.HTTP_401_UNAUTHORIZED,
                type=src.error.error_type.AUTHORIZATION_REFRESH_TOKEN_EXPIRED
            )

        scopes: typing.List[str]
        scopes = refresh_token_payload.get("scopes", [])

        # Check for god mode.
        for scope in self.scopes_god:
            if scope in scopes:
                return refresh_token_payload

        # Check for required scopes.
        for scope in refresh_token_required_scopes:
            if scope not in scopes:
                raise src.error.error.Error(
                    code=fastapi.status.HTTP_401_UNAUTHORIZED,
                    type=src.error.error_type.AUTHORIZATION_REFRESH_TOKEN_INVALID
                )

        return refresh_token_payload
