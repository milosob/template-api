import fastapi

import src.language.language_impl
import src.language.language_en
import src.language.language_pl


class ServiceLanguage:
    config: dict

    language_dict: dict
    language_default: src.language.language_impl.Language

    def __init__(
            self,
            config: dict
    ) -> None:
        self.config = config

        default: str
        default = config["default"]

        self._language_locale = {
            "en": src.language.language_en.language,
            "pl": src.language.language_pl.language
        }

        assert default in self._language_locale.keys(), "Default language not found in language."

        self._language_locale_default = self._language_locale[default]

    def default(
            self
    ) -> src.language.language_impl.Language:
        return self._language_locale_default

    def specific(
            self,
            locale: str
    ) -> src.language.language_impl.Language:
        if locale not in self._language_locale:
            return self.default()

        return self._language_locale[locale]

    def by_accept_language(
            self,
            accept_language: str
    ) -> src.language.language_impl.Language:
        # TODO Add proper handling of accept language header.
        return self.default()

    def by_request(
            self,
            request: fastapi.Request
    ) -> src.language.language.Language:

        if "accept-language" in request.headers:
            return self.by_accept_language(
                request.headers["accept-language"]
            )
        else:
            return self.default()
