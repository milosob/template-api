import uuid
import time
import typing

import src.database.account.database_account_driver_base
import src.database.account.database_account_model
import src.database.error.database_error_conflict
import src.database.error.database_error_not_found


class DatabaseAccountDriverMemory(src.database.account.database_account_driver_base.DatabaseAccountDriverBase):
    impl: typing.List[src.database.account.database_account_model.DatabaseAccountModel]

    def __init__(
            self
    ) -> None:
        super().__init__()
        self.impl = []

    async def find_by_identifier(
            self,
            identifier: str
    ) -> src.database.account.database_account_model.DatabaseAccountModel:

        for entry in self.impl:
            if entry.identifier == identifier:
                return entry

        raise src.database.error.database_error_not_found.DatabaseErrorNotFound()

    async def find_by_email(
            self,
            email: str
    ) -> src.database.account.database_account_model.DatabaseAccountModel:

        for entry in self.impl:
            for email_record in entry.email_reg.records:
                if email_record.email == email:
                    return entry

        raise src.database.error.database_error_not_found.DatabaseErrorNotFound()

    async def insert(
            self,
            model: src.database.account.database_account_model.DatabaseAccountModel
    ) -> src.database.account.database_account_model.DatabaseAccountModel:

        try:

            _ = await self.find_by_email(
                email=model.email_reg.primary.email
            )

            raise src.database.error.database_error_conflict.DatabaseErrorConflict()

        except src.database.error.database_error_not_found.DatabaseErrorNotFound:
            pass

        timestamp = time.time()

        model.identifier = str(uuid.uuid4())
        model.created_at = timestamp
        model.changed_at = timestamp

        self.impl.append(
            model
        )

        return model

    async def update(
            self,
            model: src.database.account.database_account_model.DatabaseAccountModel
    ) -> src.database.account.database_account_model.DatabaseAccountModel:

        for entry in self.impl:
            if entry.identifier == model.identifier:
                timestamp = time.time()

                self.impl.remove(entry)

                model.created_at = entry.created_at
                model.changed_at = timestamp

                self.impl.append(model)
                return model

        raise src.database.error.database_error_not_found.DatabaseErrorNotFound()

    async def remove(
            self,
            model: src.database.account.database_account_model.DatabaseAccountModel
    ) -> src.database.account.database_account_model.DatabaseAccountModel:

        for account in self.impl:
            if account.identifier == model.identifier:
                self.impl.remove(account)
                return account

        raise src.database.error.database_error_not_found.DatabaseErrorNotFound()
