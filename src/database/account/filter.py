import typing

import bson.objectid

import src.database.account.model


def emails(
        value: typing.Union[
            src.database.account.model.Account,
            typing.Set[str]
        ]
) -> typing.MutableMapping:
    return {
        "emails.value": {
            "$in": [email.email for email in value.emails] if isinstance(
                value,
                src.database.account.model.Account
            ) else list(value)
        }
    }


def identifier(
        value: typing.Union[
            src.database.account.model.Account,
            str
        ]
) -> typing.MutableMapping:
    return {
        "_id": bson.objectid.ObjectId(
            value.identifier if isinstance(
                value,
                src.database.account.model.Account
            ) else value
        )
    }
