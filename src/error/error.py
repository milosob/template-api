class Error(Exception):
    code: int
    type: str

    def __init__(
            self,
            code: int,
            type: str
    ) -> None:
        self.code = code
        self.type = type
