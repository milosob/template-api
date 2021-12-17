import collections
import datetime
import typing

import src.database.account.model


def aggregate(
        value: src.database.account.model.Account,
        updaters: typing.Set[
            typing.Callable[
                [typing.Union[src.database.account.model.Account, typing.Any]],
                typing.MutableMapping
            ]
        ]
) -> typing.MutableMapping:
    return collections.ChainMap(*[updater(value) for updater in updaters])


def updated_at(
        value: typing.Union[
            src.database.account.model.Account,
            datetime.datetime
        ]
) -> typing.MutableMapping:
    return {
        "_uat": value.updated_at if isinstance(
            value,
            src.database.account.model.Account
        ) else value
    }


def emails(
        value: typing.Union[
            src.database.account.model.Account,
            typing.List[src.database.account.model.AccountEmail]
        ]
) -> typing.MutableMapping:
    return {
        "emails": [x.to_mongo_dict() for x in (value.emails if isinstance(
            value,
            src.database.account.model.Account
        ) else value)]
    }


def verification(
        value: typing.Union[
            src.database.account.model.Account,
            src.database.account.model.AccountVerification
        ]
) -> typing.MutableMapping:
    return {
        "verification": (value.verification if isinstance(
            value,
            src.database.account.model.Account
        ) else value).to_mongo_dict()
    }


def verification_email(
        value: typing.Union[
            src.database.account.model.Account,
            bool
        ]
) -> typing.MutableMapping:
    return {
        "verification.email": value.verification.email if isinstance(
            value,
            src.database.account.model.Account
        ) else value
    }


def authentication_passwords_primary(
        value: typing.Union[
            src.database.account.model.Account,
            src.database.account.model.AccountAuthenticationPassword
        ]
) -> typing.MutableMapping:
    return {
        "authentication.password.primary": (value.authentication.passwords.primary if isinstance(
            value,
            src.database.account.model.Account
        ) else value).to_mongo_dict()
    }
