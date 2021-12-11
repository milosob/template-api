import typing

import src.database.account.model
import src.database.error.error_not_implemented


class DriverBase:

    def __init__(
            self
    ) -> None:
        pass

    async def find_one_by_identifier(
            self,
            identifier: str
    ) -> typing.Union[src.database.account.model.Account, None]:
        pass

    async def find_one_by_email(
            self,
            email: str
    ) -> typing.Union[src.database.account.model.Account, None]:
        pass

    async def insert_one(
            self,
            model: src.database.account.model.Account
    ) -> bool:
        pass

    async def remove_by_identifier(
            self,
            identifier: str,
            model: src.database.account.model.Account
    ) -> bool:
        pass

    async def remove_one(
            self,
            model: src.database.account.model.Account
    ) -> bool:
        pass

    async def update_one_by_identifier(
            self,
            identifier: str,
            model: src.database.account.model.Account
    ) -> bool:
        pass

    async def update_one(
            self,
            model: src.database.account.model.Account
    ) -> bool:
        pass
