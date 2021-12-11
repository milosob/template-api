import datetime
import typing

import bson.objectid
import pymongo
import pymongo.results

import src.database.account.driver_base
import src.database.account.model


class DriverMongo(src.database.account.driver_base.DriverBase):
    _impl: pymongo.collection.Collection

    def __init__(
            self,
            impl: pymongo.collection.Collection
    ):
        super().__init__()
        self._impl = impl

    async def insert_one(
            self,
            model: src.database.account.model.Account
    ) -> bool:
        model.notify_create()

        result: pymongo.results.InsertOneResult
        result = self._impl.insert_one(
            document=model
        )

        if not result.acknowledged:
            return False

        model.identifier = str(result.inserted_id)

        return True

    async def update_one(
            self,
            model: src.database.account.model.Account
    ) -> bool:
        model.notify_update()

        result: pymongo.results.UpdateResult
        result = self._impl.update_one(
            filter={
                "_id": bson.objectid.ObjectId(model.identifier)
            },
            update={
                "$set": model
            }
        )

        return result.acknowledged

    async def update_one_authentication_password_primary(
            self,
            model: src.database.account.model.Account
    ) -> bool:
        model.notify_update()

        result: pymongo.results.UpdateResult
        result = self._impl.update_one(
            filter={
                "_id": bson.objectid.ObjectId(model.identifier)
            },
            update={
                "$set": {
                    "authentication.password.primary": model.authentication.passwords.primary,
                    "updated_at": model.updated_at
                }
            }
        )

        return result.acknowledged

    async def update_one_emails(
            self,
            model: src.database.account.model.Account
    ) -> bool:
        model.notify_update()

        result: pymongo.results.UpdateResult
        result = self._impl.update_one(
            filter={
                "_id": bson.objectid.ObjectId(model.identifier)
            },
            update={
                "$set": {
                    "emails": model.emails,
                    "updated_at": model.updated_at
                }
            }
        )

        return result.acknowledged

    async def remove_one(
            self,
            model: src.database.account.model.Account
    ) -> bool:
        model.notify_update()

        result: pymongo.results.DeleteResult
        result = self._impl.delete_one(
            filter={
                "_id": bson.objectid.ObjectId(model.identifier)
            }
        )

        return result.acknowledged

    async def find_one_by_identifier(
            self,
            identifier: str
    ) -> typing.Union[src.database.account.model.Account, None]:
        result: typing.Any
        result = self._impl.find_one(
            filter={
                "_id": bson.objectid.ObjectId(identifier)
            }
        )

        if result:
            return src.database.account.model.Account(result)

        return None

    async def find_one_by_email(
            self,
            email: str
    ) -> typing.Union[src.database.account.model.Account, None]:
        result: typing.Any
        result = self._impl.find_one(
            filter={
                "email.records.value": {
                    "$eq": email
                }
            }
        )

        if result:
            return src.database.account.model.Account(result)

        return None
