import typing

import bson.objectid


def email(
        value: str
) -> dict:
    return {
        "emails.value": {
            "$eq": value
        }
    }


def emails(
        value: typing.List[str]
) -> dict:
    return {
        "emails.value": {
            "$in": value
        }
    }


def identifier(
        value: str
) -> dict:
    return {
        "_id": bson.objectid.ObjectId(value)
    }
