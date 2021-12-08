import app_database
import app_service


class AppState:
    config: dict

    database: app_database.AppDatabase
    service: app_service.AppService

    def __init__(
            self,
            config: dict
    ):
        self.config = config
        self.database = app_database.AppDatabase(
            config=config["database"]
        )
        self.service = app_service.AppService(
            config=config["service"]
        )
