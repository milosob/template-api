import typing


class DatabaseAccountEmailRegRecordModel:
    email: str
    primary: bool
    confirmed_at: int


class DatabaseAccountEmailRegModel:
    primary: DatabaseAccountEmailRegRecordModel
    records: typing.List[DatabaseAccountEmailRegRecordModel]


class DatabaseAccountEmailLogRecordModel:
    email: str
    confirmed_at: int

    type: str
    context: object
    occurred_at: int


class DatabaseAccountEmailLogModel:
    records: typing.List[DatabaseAccountEmailLogRecordModel]


class DatabaseAccountAuthenticationPasswordRegRecordModel:
    password: str


class DatabaseAccountAuthenticationPasswordRegModel:
    primary: DatabaseAccountAuthenticationPasswordRegRecordModel


class DatabaseAccountAuthenticationPasswordLogRecordModel:
    password: str

    type: str
    context: object
    occurred_at: int


class DatabaseAccountAuthenticationPasswordLogModel:
    records: typing.List[DatabaseAccountEmailLogRecordModel]


class DatabaseAccountAuthenticationModel:
    password_reg: DatabaseAccountAuthenticationPasswordRegModel
    password_log: DatabaseAccountAuthenticationPasswordLogModel


class DatabaseAccountModel:
    # BASIC USER INFO
    identifier: str

    # BASIC USER TIME
    created_at: int
    changed_at: int

    # ACCOUNT EMAIL
    email_reg: DatabaseAccountEmailRegModel
    email_log: DatabaseAccountEmailLogModel

    # ACCOUNT AUTHENTICATION
    authentication: DatabaseAccountAuthenticationModel

    def __init__(
            self
    ) -> None:
        self.email_reg = DatabaseAccountEmailRegModel()
        self.email_reg.primary = DatabaseAccountEmailRegRecordModel()
        self.email_reg.records = []
        self.email_log = DatabaseAccountEmailLogModel()
        self.email_log.records = []

        self.authentication = DatabaseAccountAuthenticationModel()
        self.authentication.password_reg = DatabaseAccountAuthenticationPasswordRegModel()
        self.authentication.password_reg.primary = DatabaseAccountAuthenticationPasswordRegRecordModel()
        self.authentication.password_log = DatabaseAccountAuthenticationPasswordLogModel()
        self.authentication.password_log.records = []
