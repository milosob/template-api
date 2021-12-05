import fastapi


class ServiceLang:
    config: dict
    default: str

    def __init__(
            self,
            config: dict
    ) -> None:
        self.config = config
        self.default = config["default"]

    def by_accept_language(
            self,
            accept_language: str
    ) -> str:
        # TODO Add proper handling of accept lang header.
        return self.default

    def by_request(
            self,
            request: fastapi.Request
    ) -> str:
        if "accept-language" in request.headers:
            return self.by_accept_language(
                accept_language=request.headers["accept-language"]
            )
        else:
            return self.default
