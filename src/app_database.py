import src.database.account.driver_base
import src.database.account.driver_memory


class AppDatabase:
    config: dict

    account: src.database.account.driver_base.DriverBase

    def __init__(
            self,
            config: dict
    ) -> None:
        self.config = config

        # Account
        account_config = config["account"]
        account_driver = account_config["driver"]

        if account_driver not in [
            "memory"
        ]:
            raise NotImplementedError()

        if account_driver == "memory":
            self.account = src.database.account.driver_memory.DriverMemory()
