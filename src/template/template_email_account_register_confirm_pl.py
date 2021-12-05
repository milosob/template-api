import src.template.template_email

__TEMPLATE_SUBJECT = \
    """\
Potwierdź rejestrację\
"""

__TEMPLATE_TEXT = \
    """\
http:localhost:3000/confirm?token=%%token%%
"""

__TEMPLATE_HTML = \
    """\
    http:localhost:3000/confirm?token=%%token%%
"""

template: src.template.template_email.TemplateEmail = src.template.template_email.TemplateEmail(
    template_subject=__TEMPLATE_SUBJECT,
    template_text=__TEMPLATE_TEXT,
    template_html=__TEMPLATE_HTML
)
