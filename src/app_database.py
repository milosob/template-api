import src.database.account.driver_base
import src.database.account.driver_memory


class AppDatabase:
    config: dict

    database_account: src.database.account.driver_base.DriverBase

    def __init__(
            self,
            config: dict
    ) -> None:
        self.config = config

        # Account
        database_account_config = config["account"]
        database_account_driver = database_account_config["driver"]

        if database_account_driver not in [
            "memory"
        ]:
            raise NotImplementedError()

        if database_account_driver == "memory":
            self.database_account = src.database.account.driver_memory.DriverMemory()
