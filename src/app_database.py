import typing

import src.database.account.driver_base
import src.database.account.driver_mongo


class AppDatabase:
    config: dict

    account: src.database.account.driver_base.DriverBase

    def __init__(
            self,
            config: dict
    ) -> None:
        self.config = config

        # Account
        account_config: dict
        account_config = config["account"]
        account_driver: str
        account_driver = account_config["driver"]

        if account_driver not in [
            "mongo"
        ]:
            raise NotImplementedError()

        account_driver_config: dict
        account_driver_config = account_config[account_driver]

        if account_driver == "mongo":
            import pymongo

            account_mongo_client: typing.Union[pymongo.mongo_client.MongoClient, None]
            account_mongo_client = None

            auth: str
            auth = account_driver_config["auth"]

            if auth == "uri":
                account_mongo_client = pymongo.mongo_client.MongoClient(
                    account_driver_config[auth]["uri"]
                )

            assert account_mongo_client is not None

            self.account = src.database.account.driver_mongo.DriverMongo(
                account_mongo_client[account_driver_config["name"]][account_driver_config["collection"]]
            )

        assert self.account is not None
