import src.database.account.database_account_driver_base
import src.database.account.database_account_driver_memory
import src.database.confirm.database_confirm_driver_base
import src.database.confirm.database_confirm_driver_memory


class StateAppDatabase:
    config: dict

    database_account: src.database.account.database_account_driver_base.DatabaseAccountDriverBase
    database_confirm: src.database.confirm.database_confirm_driver_base.DatabaseConfirmDriverBase

    def __init__(
            self,
            config: dict
    ) -> None:
        self.config = config

        # DatabaseAccount
        database_account_config = config["database_account"]
        database_account_driver = database_account_config["driver"]

        if database_account_driver not in [
            "memory"
        ]:
            raise NotImplementedError()

        if database_account_driver == "memory":
            self.database_account = src.database.account.database_account_driver_memory.DatabaseAccountDriverMemory()

        # DatabaseConfirm
        database_confirm_config = config["database_confirm"]
        database_confirm_driver = database_confirm_config["driver"]

        if database_confirm_driver not in [
            "memory"
        ]:
            raise NotImplementedError()

        if database_confirm_driver == "memory":
            self.database_confirm = src.database.confirm.database_confirm_driver_memory.DatabaseConfirmDriverMemory()
