import aiosmtplib
import email.message
import email.utils
import ssl
import typing

import jinja2


class ServiceMail:
    config: dict

    send_cb: typing.Callable[[email.message.EmailMessage], typing.Coroutine[typing.Any, typing.Any, None]]

    smtp_host: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    smtp_tls: bool
    smtp_tls_context: typing.Union[ssl.SSLContext, None]

    smtp_options: dict

    def __init__(
            self,
            config: dict
    ) -> None:
        self.config = config

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
                self.smtp_options |= {
                    "username": self.smtp_username,
                    "password": self.smtp_password
                }

            if self.smtp_port in [
                587,
                2525,
                465
            ]:
                self.smtp_tls = True
                self.smtp_tls_context = ssl.create_default_context()

                self.smtp_options |= {
                    "use_tls": self.smtp_tls,
                    "tls_context": self.smtp_tls_context
                }

            else:
                self.smtp_tls = False
                self.smtp_tls_context = None

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
            to: dict = None,
            bcc: dict = None,
            locale: str = None,
            template: typing.Tuple[jinja2.Template, jinja2.Template] = None,
            **template_parameters
    ) -> None:
        email_message: email.message.EmailMessage
        email_message = email.message.EmailMessage()

        email_message["Subject"] = template[0].render(
            LANGUAGE=locale,
            **template_parameters
        )
        email_message.add_alternative(
            template[1].render(
                LANGUAGE=locale,
                **template_parameters
            ),
            subtype="html"
        )

        email_message["From"] = ", ".join(
            [
                email.utils.formataddr(
                    (
                        name,
                        address
                    )
                ) for address, name in self.config["from"].items()
            ]
        )

        if to:
            email_message["To"] = ", ".join(
                [
                    email.utils.formataddr(
                        (
                            name,
                            address
                        )
                    ) for address, name in to.items()
                ]
            )

        if bcc:
            email_message["Bcc"] = ", ".join(
                [
                    email.utils.formataddr(
                        (
                            name,
                            address
                        )
                    ) for address, name in bcc.items()
                ]
            )

        await self.send(
            message=email_message
        )
