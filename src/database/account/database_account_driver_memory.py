import datetime
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
            for email_record in entry.email.reg.records:
                if email_record.email == email:
                    return entry

        raise src.database.error.database_error_not_found.DatabaseErrorNotFound()

    async def insert(
            self,
            model: src.database.account.database_account_model.DatabaseAccountModel
    ) -> src.database.account.database_account_model.DatabaseAccountModel:
        try:
            _ = await self.find_by_email(
                email=model.email.reg.primary.email
            )
            raise src.database.error.database_error_conflict.DatabaseErrorConflict()
        except src.database.error.database_error_not_found.DatabaseErrorNotFound:
            pass

        date_now: datetime.datetime
        date_now = datetime.datetime.utcnow()

        model.identifier = str(uuid.uuid4())
        model.created_at = date_now
        model.changed_at = date_now

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
                date_now: datetime.datetime
                date_now = datetime.datetime.utcnow()

                self.impl.remove(entry)

                model.changed_at = date_now

                self.impl.append(model)
                return model

        raise src.database.error.database_error_not_found.DatabaseErrorNotFound()

    async def remove(
            self,
            model: src.database.account.database_account_model.DatabaseAccountModel
    ) -> src.database.account.database_account_model.DatabaseAccountModel:
        for entry in self.impl:
            if entry.identifier == model.identifier:
                self.impl.remove(entry)
                return entry

        raise src.database.error.database_error_not_found.DatabaseErrorNotFound()
