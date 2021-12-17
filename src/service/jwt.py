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

    lifetime_access: int
    lifetime_refresh: int
    lifetime_password_recover: int
    lifetime_account_register: int

    verify_default_options: dict
    verify_refresh_options: dict

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

        self.lifetime_access = config["lifetime"]["access"]
        self.lifetime_refresh = config["lifetime"]["refresh"]
        self.lifetime_password_recover = config["lifetime"]["password_recover"]
        self.lifetime_account_register = config["lifetime"]["account_register"]

        self.verify_default_options = {
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
        self.verify_refresh_options = {
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
        }

    def issue(
            self,
            sub: str,
            data: dict,
            lifetime: int,
            scopes: typing.List[str],
            access_token: str = None
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
            payload,
            self.issue_key,
            self.issue_alg,
            None,
            access_token
        )

        return token

    def verify_token(
            self,
            token: str,
            error_type: str,
            options: dict,
            access_token: str
    ):
        try:
            # noinspection PyTypeChecker
            return jose.jwt.decode(
                token,
                self.verify_keys,
                self.verify_algs,
                options,
                None,
                None,
                None,
                access_token
            )
        except jose.JWTError:
            raise src.error.error.Error(
                fastapi.status.HTTP_401_UNAUTHORIZED,
                error_type
            )

    def verify_iss(
            self,
            payload: dict,
            error_type: str
    ) -> None:
        if payload["iss"] not in self.verify_ids:
            raise src.error.error.Error(
                fastapi.status.HTTP_401_UNAUTHORIZED,
                error_type
            )

    def verify_exp(
            self,
            payload: dict,
            error_type: str,
            date_now: datetime.datetime = datetime.datetime.utcnow()
    ) -> None:
        if calendar.timegm(date_now.utctimetuple()) > payload["exp"]:
            raise src.error.error.Error(
                fastapi.status.HTTP_401_UNAUTHORIZED,
                error_type
            )

    def verify_required_scopes(
            self,
            payload: dict,
            error_type: str,
            required_scopes: typing.List[str]
    ) -> None:
        scopes: typing.List[str]
        scopes = payload.get("scopes", [])

        # Check for required scopes.
        for scope in required_scopes:
            if scope not in scopes:
                raise src.error.error.Error(
                    fastapi.status.HTTP_401_UNAUTHORIZED,
                    error_type
                )

    def verify(
            self,
            token: str,
            required_scopes: typing.List[str],
            verify_token_error_type: typing.Optional[str] = None,
            verify_iss_error_type: typing.Optional[str] = None,
            verify_exp_error_type: typing.Optional[str] = None,
            verify_scopes_error_type: typing.Optional[str] = None,
            options: typing.Optional[dict] = None,
            access_token: typing.Optional[str] = None
    ) -> dict:
        payload: dict
        payload = self.verify_token(
            token,
            verify_token_error_type,
            options,
            access_token
        )

        if verify_iss_error_type:
            self.verify_iss(
                payload,
                verify_iss_error_type
            )

        if verify_exp_error_type:
            self.verify_exp(
                payload,
                verify_exp_error_type
            )

        if verify_scopes_error_type:
            self.verify_required_scopes(
                payload,
                verify_scopes_error_type,
                required_scopes
            )

        return payload
