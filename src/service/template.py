import pathlib
import typing

import jinja2
import jinja2.environment


class ServiceTemplate:
    config: dict

    mail: jinja2.Environment

    def __init__(
            self,
            config: dict
    ) -> None:
        self.config = config

        self.mail = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                pathlib.Path(__file__).parent.parent.joinpath(
                    "template"
                ).joinpath(
                    "mail"
                )
            )
        )

    @property
    def mail_account_register(
            self
    ) -> typing.Tuple[jinja2.Template, jinja2.Template]:
        return (
            self.mail.get_template("account_register.subject.text"),
            self.mail.get_template("account_register.body.html")
        )
