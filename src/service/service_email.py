class ServiceEmail:
    config: dict

    def __init__(
            self,
            config: dict
    ) -> None:
        self.config = config
        # TODO Read config and configure service.

    async def send_confirm_email_message(
            self,
            email: str,
            token: str
    ) -> None:
        # TODO Send confirm email message.
        pass
