import datetime

import fastapi
import fastapi.responses

import src.dto.dto_error
import src.error.error

error_type = src.error.error.Error


async def handler(
        request: fastapi.Request,
        exc: error_type,
):
    return fastapi.responses.JSONResponse(
        status_code=exc.code,
        content=src.dto.dto_error.DtoErrorApiOut(
            code=exc.code,
            type=exc.type,
            occurred_at=datetime.datetime.utcnow()
        )
    )
