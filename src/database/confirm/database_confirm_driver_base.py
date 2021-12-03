import src.database.confirm.database_confirm_model
import src.database.error.database_error_not_implemented


class DatabaseConfirmDriverBase:

    def __init__(
            self
    ) -> None:
        pass

    async def find_by_identifier(
            self,
            identifier: str
    ) -> src.database.account.database_account_model.DatabaseAccountModel:
        raise src.database.error.database_error_not_implemented.DatabaseErrorNotImplemented()

    async def insert(
            self,
            model: src.database.confirm.database_confirm_model.DatabaseConfirmModel
    ) -> src.database.confirm.database_confirm_model.DatabaseConfirmModel:
        pass

    async def update(
            self,
            model: src.database.confirm.database_confirm_model.DatabaseConfirmModel
    ) -> src.database.confirm.database_confirm_model.DatabaseConfirmModel:
        pass
