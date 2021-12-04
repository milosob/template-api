import src.lang.lang


class StateRequestLang:
    lang: src.lang.lang.Lang

    def __init__(
            self,
            lang: src.lang.lang.Lang
    ):
        self.lang = lang
