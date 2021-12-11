import datetime
import typing

import bson.objectid
import pymongo
import pymongo.results

import src.database.account.driver_base
import src.database.account.model


class DriverMongo(src.database.account.driver_base.DriverBase):
    impl: pymongo.collection.Collection

    def __init__(
            self,
            impl: pymongo.collection.Collection
    ):
        super().__init__()
        self.impl = impl

    async def find_one_by_identifier(
            self,
            identifier: str
    ) -> typing.Union[src.database.account.model.Account, None]:
        result: typing.Any
        result = self.impl.find_one(
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
        result = self.impl.find_one(
            filter={
                "email.records.value": {
                    "$eq": email
                }
            }
        )

        if result:
            return src.database.account.model.Account(result)

        return None

    async def insert_one(
            self,
            model: src.database.account.model.Account
    ) -> bool:
        model.notify_create()

        result: pymongo.results.InsertOneResult
        result = self.impl.insert_one(
            document=model
        )

        if not result.acknowledged:
            return False

        model.identifier = str(result.inserted_id)

        return True

    async def remove_by_identifier(
            self,
            identifier: str,
            model: src.database.account.model.Account
    ) -> bool:
        model.notify_remove()

        result: pymongo.results.DeleteResult
        result = self.impl.delete_one(
            filter={
                "_id": bson.objectid.ObjectId(identifier)
            }
        )

        return result.acknowledged

    async def remove_one(
            self,
            model: src.database.account.model.Account
    ) -> bool:

        return await self.remove_by_identifier(
            identifier=model.identifier,
            model=model
        )

    async def update_one_by_identifier(
            self,
            identifier: str,
            model: src.database.account.model.Account
    ) -> bool:
        model.notify_update()

        result: pymongo.results.UpdateResult
        result = self.impl.update_one(
            filter={
                "_id": bson.objectid.ObjectId(identifier)
            },
            update={
                "$set": model
            }
        )

        return result.acknowledged

    async def update_one(
            self,
            model: src.database.account.model.Account
    ) -> bool:
        return await self.update_one_by_identifier(
            identifier=model.identifier,
            model=model
        )
