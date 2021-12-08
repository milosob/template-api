import typing

import fastapi


class ServiceLocale:
    config: dict

    default: str
    supported: typing.List[str]

    def __init__(
            self,
            config: dict
    ) -> None:
        self.config = config
        self.default = config["default"]
        self.supported = config["supported"]

    def by_accept_language_header(
            self,
            value: str
    ) -> str:
        locales_preference: typing.List[tuple]
        locales_preference = []

        try:

            for entry in value.split(","):
                locale: str
                quality: str

                locale, _, quality = entry.partition(";")

                if locale == entry:
                    locales_preference.append((locale, 1.0))
                else:
                    _, _, preference = quality.partition("=")

                    value = float(preference)
                    value = min(value, 1.0)

                    locales_preference.append((locale, value))

        except ValueError:
            return self.default
        except IndexError:
            return self.default

        locales_preference.sort(
            key=lambda x: x[1],
            reverse=True
        )

        locales: typing.List[str]
        locales = [locale_preference[0] for locale_preference in locales_preference]

        for locale in locales:
            if locale in self.supported:
                return locale

        # No perfect match.
        for locale in locales:
            language, _, location = locale.partition("-")

            if language in self.supported:
                return language

        return self.default

    def by_request(
            self,
            request: fastapi.Request
    ) -> str:
        if "accept-language" in request.headers:
            return self.by_accept_language_header(
                value=request.headers["accept-language"]
            )
        else:
            return self.default
