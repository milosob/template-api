import src.service.service_email
import src.service.service_jwt
import src.service.service_language
import src.service.service_password


class StateAppService:
    config: dict

    service_email: src.service.service_email.ServiceEmail
    service_jwt: src.service.service_jwt.ServiceJwt
    service_language: src.service.service_language.ServiceLanguage
    service_password: src.service.service_password.ServicePassword

    def __init__(
            self,
            config: dict
    ) -> None:
        self.config = config
        self.service_email = src.service.service_email.ServiceEmail(
            config=config["service_email"]
        )
        self.service_jwt = src.service.service_jwt.ServiceJwt(
            config=config["service_jwt"]
        )
        self.service_password = src.service.service_password.ServicePassword(
            config=config["service_password"]
        )
        self.service_language = src.service.service_language.ServiceLanguage(
            config=config["service_language"]
        )
