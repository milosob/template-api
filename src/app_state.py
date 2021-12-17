import src.app_database
import src.app_service


class AppState:
    config: dict

    database: src.app_database.AppDatabase
    service: src.app_service.AppService

    def __init__(
            self,
            config: dict
    ):
        self.config = config
        self.database = src.app_database.AppDatabase(
            config["database"]
        )
        self.service = src.app_service.AppService(
            config["service"]
        )
