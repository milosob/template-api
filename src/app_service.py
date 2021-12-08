import src.service.mail
import src.service.jwt
import src.service.locale
import src.service.password


class AppService:
    config: dict

    mail: src.service.mail.ServiceMail
    jwt: src.service.jwt.ServiceJwt
    locale: src.service.locale.ServiceLocale
    password: src.service.password.ServicePassword

    def __init__(
            self,
            config: dict
    ) -> None:
        self.config = config
        self.mail = src.service.mail.ServiceMail(
            config=config["mail"]
        )
        self.jwt = src.service.jwt.ServiceJwt(
            config=config["jwt"]
        )
        self.locale = src.service.locale.ServiceLocale(
            config=config["locale"]
        )
        self.password = src.service.password.ServicePassword(
            config=config["password"]
        )
