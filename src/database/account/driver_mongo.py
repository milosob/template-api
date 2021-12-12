import datetime
import typing

import pymongo
import pymongo.results

import src.database.account.model


class DriverMongo:
    _impl: pymongo.collection.Collection

    def __init__(
            self,
            impl: pymongo.collection.Collection
    ):
        super().__init__()
        self._impl = impl

    def insert_one(
            self,
            model: src.database.account.model.Account
    ) -> typing.Union[src.database.account.model.Account, None]:

        document: dict
        document = model.to_dict()

        del document["_id"]

        result: pymongo.results.InsertOneResult
        result = self._impl.insert_one(
            document=document
        )

        if not result.acknowledged:
            return None

        model._id = str(result.inserted_id)

        return model

    def find_one(
            self,
            filter: dict
    ) -> typing.Union[src.database.account.model.Account, None]:
        result: typing.Any
        result = self._impl.find_one(
            filter=filter
        )

        print(result)

        if not result:
            return None

        result["_id"] = str(result["_id"])

        return src.database.account.model.Account.from_dict(d=result)

    def update_one(
            self,
            filter: dict,
            update: dict
    ) -> bool:
        result: pymongo.results.UpdateResult
        result = self._impl.update_one(
            filter=filter,
            update=update
        )

        return result.acknowledged

    def delete_one(
            self,
            filter: dict
    ) -> bool:
        result: pymongo.results.DeleteResult
        result = self._impl.delete_one(
            filter=filter
        )

        return result.acknowledged
