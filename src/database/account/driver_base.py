import typing

import src.database.account.model


class DriverBase:

    def __init__(
            self
    ) -> None:
        pass

    async def insert_one(
            self,
            model: src.database.account.model.Account
    ) -> bool:
        raise NotImplementedError()

    async def update_one(
            self,
            model: src.database.account.model.Account
    ) -> bool:
        raise NotImplementedError()

    async def update_one_authentication_password_primary(
            self,
            model: src.database.account.model.Account
    ) -> bool:
        raise NotImplementedError()

    async def update_one_emails(
            self,
            model: src.database.account.model.Account
    ) -> bool:
        raise NotImplementedError()

    async def remove_one(
            self,
            model: src.database.account.model.Account
    ) -> bool:
        raise NotImplementedError()

    async def find_one_by_identifier(
            self,
            identifier: str
    ) -> typing.Union[src.database.account.model.Account, None]:
        raise NotImplementedError()

    async def find_one_by_email(
            self,
            email: str
    ) -> typing.Union[src.database.account.model.Account, None]:
        raise NotImplementedError()
