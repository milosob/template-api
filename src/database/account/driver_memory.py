import datetime
import uuid
import typing

import src.database.account.driver_base
import src.database.account.model
import src.database.error.error_conflict
import src.database.error.error_not_found


class DriverMemory(src.database.account.driver_base.DriverBase):
    impl: typing.List[src.database.account.model.Account]

    def __init__(
            self
    ) -> None:
        super().__init__()
        self.impl = []

    async def find_by_identifier(
            self,
            identifier: str
    ) -> src.database.account.model.Account:
        for entry in self.impl:
            if entry.identifier == identifier:
                return entry

        raise src.database.error.error_not_found.ErrorNotFound()

    async def find_by_email(
            self,
            email: str
    ) -> src.database.account.model.Account:
        for entry in self.impl:
            if email == entry.email.primary.value:
                return entry

            for email_record in entry.email.alternative:
                if email_record.value == email:
                    return entry

        raise src.database.error.error_not_found.ErrorNotFound()

    async def insert(
            self,
            model: src.database.account.model.Account
    ) -> src.database.account.model.Account:
        try:
            _ = await self.find_by_email(
                email=model.email.primary.value
            )
            raise src.database.error.error_conflict.ErrorConflict()
        except src.database.error.error_not_found.ErrorNotFound:
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
            model: src.database.account.model.Account
    ) -> src.database.account.model.Account:
        for entry in self.impl:
            if entry.identifier == model.identifier:
                date_now: datetime.datetime
                date_now = datetime.datetime.utcnow()

                self.impl.remove(entry)

                model.changed_at = date_now

                self.impl.append(model)
                return model

        raise src.database.error.error_not_found.ErrorNotFound()

    async def remove(
            self,
            model: src.database.account.model.Account
    ) -> src.database.account.model.Account:
        for entry in self.impl:
            if entry.identifier == model.identifier:
                self.impl.remove(entry)
                return entry

        raise src.database.error.error_not_found.ErrorNotFound()
