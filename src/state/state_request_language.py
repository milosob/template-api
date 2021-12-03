import src.language.language_impl


class StateRequestLanguage:
    language: src.language.language_impl.Language

    def __init__(
            self,
            language: src.language.language_impl.Language
    ):
        self.language = language
