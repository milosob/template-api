import datetime
import typing

import pymongo
import pymongo.results

import src.database.account.model
import src.database.account.filter
import src.database.account.update


class Driver:
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
        result: dict
        result = self._impl.find_one(
            filter
        )

        if not result:
            return None

        result["_id"] = str(result["_id"])

        return src.database.account.model.Account.from_mongo_dict(result)

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

        result: dict
        result = self._impl.find_one_and_update(
            filter,
            update,
            None,
            None,
            False,
            pymongo.ReturnDocument.AFTER
        )

        if not result:
            return None

        result["_id"] = str(result["_id"])

        return src.database.account.model.Account.from_mongo_dict(result)

    def find_one_and_delete(
            self,
            filter: typing.MutableMapping
    ) -> typing.Union[src.database.account.model.Account, None]:
        result: dict
        result = self._impl.find_one_and_delete(
            filter
        )

        if not result:
            return None

        result["_id"] = str(result["_id"])

        return src.database.account.model.Account.from_mongo_dict(result)

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
        result = self._impl.insert_one(document)

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
                model,
                updaters
            ) for operator, updaters in updaters.items()
        }

        return self.find_one_and_update(
            src.database.account.filter.identifier(
                model
            ),
            update
        )
