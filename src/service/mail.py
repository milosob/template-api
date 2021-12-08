import aiosmtplib
import email.message
import ssl
import typing

import src.template.template_email
import src.template.template_email_account_register_confirm_pl


class ServiceMail:
    config: dict
    from_: dict

    templates: dict
    send_cb: typing.Callable[[email.message.EmailMessage], typing.Coroutine[typing.Any, typing.Any, None]]

    smtp_host: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    smtp_tls: bool
    smtp_tls_context: ssl.SSLContext

    smtp_options: dict

    def __init__(
            self,
            config: dict
    ) -> None:
        self.config = config
        self.from_ = config["from"]

        service_email_driver: str
        service_email_driver = config["driver"]

        if service_email_driver not in [
            "smtp"
        ]:
            raise NotImplementedError()

        if config["driver"] == "smtp":
            self.send_cb = self._send_smtp

            self.smtp_host = config["smtp"]["host"]
            self.smtp_port = config["smtp"]["port"]
            self.smtp_username = config["smtp"]["username"]
            self.smtp_password = config["smtp"]["password"]

            self.smtp_options = {
                "hostname": self.smtp_host,
                "port": self.smtp_port
            }

            if self.smtp_port != 25252:
                self.smtp_options.update(
                    {
                        "username": self.smtp_username,
                        "password": self.smtp_password
                    }
                )

            if self.smtp_port in [
                587,
                2525,
                465
            ]:
                self.smtp_tls = True
                self.smtp_tls_context = ssl.create_default_context()

                self.smtp_options.update(
                    {
                        "use_tls": self.smtp_tls,
                        "tls_context": self.smtp_tls_context
                    }
                )

            else:
                self.smtp_tls = False
                self.smtp_tls_context = None

        templates_pl: dict
        templates_pl = {
            "account-register-confirm": src.template.template_email_account_register_confirm_pl.template
        }

        self.templates = {
            "pl": templates_pl,
            "en": templates_pl,
            "default": templates_pl
        }

    async def _send_smtp(
            self,
            message: email.message.EmailMessage
    ):

        await aiosmtplib.send(
            message,
            **self.smtp_options
        )

    async def send(
            self,
            message: email.message.EmailMessage
    ) -> None:
        await self.send_cb(
            message=message
        )

    async def send_template(
            self,
            language: str,
            parameters: dict,
            identifier: str
    ) -> None:

        template: src.template.template_email.TemplateEmail

        if language not in self.templates:
            template = self.templates["default"][identifier]
        else:
            template = self.templates[language][identifier]

        if "from" in parameters:
            parameters["from"].update(
                self.from_
            )
        else:
            parameters["from"] = self.from_.copy()

        await self.send(
            message=template.build(
                parameters
            )
        )

    async def send_template_account_register_confirm(
            self,
            language: str,
            parameters: dict,
    ) -> None:
        await self.send_template(
            language=language,
            parameters=parameters,
            identifier="account-register-confirm"
        )
