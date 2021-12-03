import src.state.state_app_database
import src.state.state_app_service


class StateApp:
    config: dict

    database: src.state.state_app_database.StateAppDatabase
    service: src.state.state_app_service.StateAppService

    def __init__(
            self,
            config: dict
    ):
        self.config = config
        self.database = src.state.state_app_database.StateAppDatabase(
            config=config["database"]
        )
        self.service = src.state.state_app_service.StateAppService(
            config=config["service"]
        )
