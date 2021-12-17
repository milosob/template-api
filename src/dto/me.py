import pydantic


# ME GET
class MeGetInBase(pydantic.BaseModel):
    pass


class MeGetIn(MeGetInBase):
    pass


class MeGetOutBase(pydantic.BaseModel):
    pass


class MeGetOut(MeGetOutBase):
    pass


# ME POST
class MePostInBase(pydantic.BaseModel):
    pass


class MePostIn(MePostInBase):
    pass


class MePostOutBase(pydantic.BaseModel):
    pass


class MePostOut(MePostOutBase):
    pass


# ME PUT
class MePutInBase(pydantic.BaseModel):
    pass


class MePutIn(MePutInBase):
    pass


class MePutOutBase(pydantic.BaseModel):
    pass


class MePutOut(MePutOutBase):
    pass
