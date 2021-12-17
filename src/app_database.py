import pymongo

import src.database.account.driver


class AppDatabase:
    config: dict

    account_config: dict
    account_client: pymongo.MongoClient
    account: src.database.account.driver.Driver

    def __init__(
            self,
            config: dict
    ) -> None:
        self.config = config

        self.account_config = config["account"]
        self.account_client = pymongo.MongoClient(
            self.account_config["uri"]
        )
        self.account = src.database.account.driver.Driver(
            self.account_client.get_database(
                self.account_config["name"]
            ).get_collection(
                self.account_config["collection"]
            )
        )
