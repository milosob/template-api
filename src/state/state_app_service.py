import src.service.service_email
import src.service.service_jwt
import src.service.service_locale
import src.service.service_password


class StateAppService:
    config: dict

    service_email: src.service.service_email.ServiceEmail
    service_jwt: src.service.service_jwt.ServiceJwt
    service_locale: src.service.service_locale.ServiceLocale
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
        self.service_locale = src.service.service_locale.ServiceLocale(
            config=config["service_locale"]
        )
        self.service_password = src.service.service_password.ServicePassword(
            config=config["service_password"]
        )
