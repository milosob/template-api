import datetime
import re


def username(
        v: str
) -> str:
    if not re.fullmatch(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$', v):
        raise ValueError("Invalid email address.")

    return v


def password(
        v: str
) -> str:
    # todo
    #   Verify password strength.

    # Increasing restriction can result in failed logins.

    return v


def alias(
        v: str
) -> str:
    if not re.fullmatch(r'^[A-Za-z0-9._ -]{4,}$', v):
        raise ValueError("Invalid alias characters.")

    return v


def gender(
        v: str
) -> str:
    if not re.fullmatch(r'^(unspecified|male|female|other:[A-Za-z ]+)$', v):
        raise ValueError("Invalid gender.")

    return v


def birthdate(
        v: datetime.datetime
) -> datetime.datetime:
    date_now: datetime.datetime
    date_now = datetime.datetime.now()

    if date_now < v:
        raise ValueError("Invalid birthdate. Age requirements not met.")

    if date_now.year - v.year + (date_now.month > v.month or date_now.month == v.month and date_now.day >= v.day) >= 18:
        raise ValueError("Invalid birthdate. Age requirements not met.")

    return v
