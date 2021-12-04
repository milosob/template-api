import uuid
import typing

import src.database.confirm.database_confirm_driver_base
import src.database.confirm.database_confirm_model
import src.database.error.database_error_conflict
import src.database.error.database_error_not_found


class DatabaseConfirmDriverMemory(
    src.database.confirm.database_confirm_driver_base.DatabaseConfirmDriverBase
):
    impl: typing.List[src.database.confirm.database_confirm_model.DatabaseConfirmModel]

    def __init__(
            self
    ) -> None:
        super().__init__()
        self.impl = []

    async def find_by_identifier(
            self,
            identifier: str
    ) -> src.database.confirm.database_confirm_model.DatabaseConfirmModel:
        for entry in self.impl:
            if entry.identifier == identifier:
                return entry

        raise src.database.error.database_error_not_found.DatabaseErrorNotFound()

    async def find_by_token(
            self,
            token: str
    ) -> src.database.confirm.database_confirm_model.DatabaseConfirmModel:
        for entry in self.impl:
            if entry.token == token:
                return entry

        raise src.database.error.database_error_not_found.DatabaseErrorNotFound()

    async def insert(
            self,
            model: src.database.confirm.database_confirm_model.DatabaseConfirmModel
    ) -> src.database.confirm.database_confirm_model.DatabaseConfirmModel:
        model.identifier = str(uuid.uuid4())

        self.impl.append(
            model
        )

        return model

    async def update(
            self,
            model: src.database.confirm.database_confirm_model.DatabaseConfirmModel
    ) -> src.database.confirm.database_confirm_model.DatabaseConfirmModel:
        for entry in self.impl:
            if entry.identifier == model.identifier:
                self.impl.remove(entry)
                self.impl.append(model)

                return model

        raise src.database.error.database_error_not_found.DatabaseErrorNotFound()
