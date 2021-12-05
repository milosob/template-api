import email.message
import email.headerregistry
import email.utils


class TemplateEmail:
    template_subject: str
    template_text: str
    template_html: str

    def __init__(
            self,
            template_subject: str,
            template_text: str,
            template_html: str
    ) -> None:
        self.template_subject = template_subject
        self.template_text = template_text
        self.template_html = template_html

    @staticmethod
    def _template_substitute(
            template: str,
            parameters: dict
    ) -> str:
        for arg, value in parameters.items():
            template = template.replace(f"%%{arg}%%", value)

        return template

    def build(
            self,
            parameters: dict
    ) -> email.message.EmailMessage:
        email_message: email.message.EmailMessage
        email_message = email.message.EmailMessage()

        subject: str
        subject = TemplateEmail._template_substitute(
            template=self.template_subject,
            parameters=parameters["subject"]
        )

        text: str
        text = TemplateEmail._template_substitute(
            template=self.template_text,
            parameters=parameters["body"]
        )

        html: str
        html = TemplateEmail._template_substitute(
            template=self.template_html,
            parameters=parameters["body"]
        )

        if "from" in parameters:
            email_message["From"] = ", ".join(
                [
                    email.utils.formataddr(
                        (
                            name,
                            address
                        )
                    ) for address, name in parameters["from"].items()
                ]
            )

        if "to" in parameters:
            email_message["To"] = ", ".join(
                [
                    email.utils.formataddr(
                        (
                            name,
                            address
                        )
                    ) for address, name in parameters["to"].items()
                ]
            )

        if "bcc" in parameters:
            email_message["Bcc"] = ", ".join(
                [
                    email.utils.formataddr(
                        (
                            name,
                            address
                        )
                    ) for address, name in parameters["bcc"].items()
                ]
            )

        email_message["Subject"] = subject

        email_message.add_alternative(
            text,
            subtype="text"
        )
        email_message.add_alternative(
            html,
            subtype="html"
        )

        return email_message
