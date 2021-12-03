import src.database.account.database_account_model
import src.database.error.database_error_not_implemented


class DatabaseAccountDriverBase:

    def __init__(
            self
    ) -> None:
        pass

    async def find_by_identifier(
            self,
            identifier: str
    ) -> src.database.account.database_account_model.DatabaseAccountModel:
        raise src.database.error.database_error_not_implemented.DatabaseErrorNotImplemented()

    async def find_by_email(
            self,
            email: str
    ) -> src.database.account.database_account_model.DatabaseAccountModel:
        raise src.database.error.database_error_not_implemented.DatabaseErrorNotImplemented()

    async def insert(
            self,
            model: src.database.account.database_account_model.DatabaseAccountModel
    ) -> src.database.account.database_account_model.DatabaseAccountModel:
        raise src.database.error.database_error_not_implemented.DatabaseErrorNotImplemented()

    async def update(
            self,
            model: src.database.account.database_account_model.DatabaseAccountModel
    ) -> src.database.account.database_account_model.DatabaseAccountModel:
        raise src.database.error.database_error_not_implemented.DatabaseErrorNotImplemented()

    async def remove(
            self,
            model: src.database.account.database_account_model.DatabaseAccountModel
    ) -> src.database.account.database_account_model.DatabaseAccountModel:
        raise src.database.error.database_error_not_implemented.DatabaseErrorNotImplemented()
