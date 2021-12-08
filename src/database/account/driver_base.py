import src.database.account.model
import src.database.error.error_not_implemented


class DriverBase:

    def __init__(
            self
    ) -> None:
        pass

    async def find_by_identifier(
            self,
            identifier: str
    ) -> src.database.account.model.Account:
        raise src.database.error.error_not_implemented.ErrorNotImplemented()

    async def find_by_email(
            self,
            email: str
    ) -> src.database.account.model.Account:
        raise src.database.error.error_not_implemented.ErrorNotImplemented()

    async def insert(
            self,
            model: src.database.account.model.Account
    ) -> src.database.account.model.Account:
        raise src.database.error.error_not_implemented.ErrorNotImplemented()

    async def update(
            self,
            model: src.database.account.model.Account
    ) -> src.database.account.model.Account:
        raise src.database.error.error_not_implemented.ErrorNotImplemented()

    async def remove(
            self,
            model: src.database.account.model.Account
    ) -> src.database.account.model.Account:
        raise src.database.error.error_not_implemented.ErrorNotImplemented()
