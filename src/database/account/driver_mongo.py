import datetime
import typing

import pymongo
import pymongo.results

import src.database.account.model
import src.database.account.filter
import src.database.account.update


class DriverMongo:
    _impl: pymongo.collection.Collection

    def __init__(
            self,
            impl: pymongo.collection.Collection
    ):
        super().__init__()
        self._impl = impl

    def find_one(
            self,
            filter: typing.MutableMapping
    ) -> typing.Union[src.database.account.model.Account, None]:
        result: typing.Any
        result = self._impl.find_one(
            filter=filter
        )

        if not result:
            return None

        result["_id"] = str(result["_id"])

        return src.database.account.model.Account.from_mongo_dict(d=result)

    def find_one_and_update(
            self,
            filter: typing.MutableMapping,
            update: typing.MutableMapping
    ) -> typing.Union[src.database.account.model.Account, None]:
        try:
            update["$currentDate"]["_uat"] = True
        except KeyError:
            update["$currentDate"] = {
                "_uat": True
            }

        result: pymongo.results.UpdateResult
        result = self._impl.find_one_and_update(
            filter=filter,
            update=update,
            return_document=pymongo.ReturnDocument.AFTER
        )

        if not result.acknowledged:
            return None

        result.raw_result["_id"] = str(result.raw_result["_id"])

        return src.database.account.model.Account.from_mongo_dict(d=result.raw_result)

    def find_one_and_delete(
            self,
            filter: typing.MutableMapping
    ) -> typing.Union[src.database.account.model.Account, None]:
        result: pymongo.results.DeleteResult
        result = self._impl.find_one_and_delete(
            filter=filter
        )

        if not result.acknowledged:
            return None

        result.raw_result["_id"] = str(result.raw_result["_id"])

        return src.database.account.model.Account.from_mongo_dict(d=result.raw_result)

    def insert_one(
            self,
            model: src.database.account.model.Account
    ) -> typing.Union[src.database.account.model.Account, None]:
        date_now: datetime.datetime = datetime.datetime.utcnow()

        model._cat = date_now
        model._uat = date_now

        document: dict
        document = model.to_mongo_dict()

        del document["_id"]

        result: pymongo.results.InsertOneResult
        result = self._impl.insert_one(document=document)

        if not result.acknowledged:
            return None

        model._id = str(result.inserted_id)

        return model

    def update_one(
            self,
            model: src.database.account.model.Account,
            updaters: typing.MutableMapping[
                str,
                typing.Set[
                    typing.Callable[
                        [typing.Union[src.database.account.model.Account, typing.Any]],
                        typing.MutableMapping
                    ]
                ]
            ]
    ) -> typing.Union[src.database.account.model.Account, None]:
        update: typing.MutableMapping
        update = {
            operator: src.database.account.update.aggregate(
                value=model,
                updaters=updaters
            ) for operator, updaters in updaters.items()
        }

        return self.find_one_and_update(
            filter=src.database.account.filter.identifier(
                value=model
            ),
            update=update
        )
