import fastapi

import src.lang.lang
import src.lang.lang_en
import src.lang.lang_pl


class ServiceLang:
    config: dict

    lang_dict: dict
    lang_default: src.lang.lang.Lang

    def __init__(
            self,
            config: dict
    ) -> None:
        self.config = config

        default: str
        default = config["default"]

        self._lang_locale = {
            "en": src.lang.lang_en.lang,
            "pl": src.lang.lang_pl.lang
        }

        assert default in self._lang_locale.keys(), "Default lang not found in lang."

        self._lang_locale_default = self._lang_locale[default]

    def default(
            self
    ) -> src.lang.lang.Lang:
        return self._lang_locale_default

    def specific(
            self,
            locale: str
    ) -> src.lang.lang.Lang:
        if locale not in self._lang_locale:
            return self.default()

        return self._lang_locale[locale]

    def by_accept_lang(
            self,
            accept_lang: str
    ) -> src.lang.lang.Lang:
        # TODO Add proper handling of accept lang header.
        return self.default()

    def by_request(
            self,
            request: fastapi.Request
    ) -> src.lang.lang.Lang:

        if "accept-lang" in request.headers:
            return self.by_accept_lang(
                request.headers["accept-lang"]
            )
        else:
            return self.default()
