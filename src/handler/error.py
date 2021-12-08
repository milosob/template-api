import datetime

import fastapi
import fastapi.responses

import src.dto.error
import src.error.error

error_type = src.error.error.Error


async def handler(
        request: fastapi.Request,
        exc: error_type,
):
    return fastapi.responses.Response(
        status_code=exc.code,
        media_type="application/json",
        content=src.dto.error.ErrorApiOut(
            code=exc.code,
            type=exc.type,
            occurred_at=datetime.datetime.utcnow()
        ).json()
    )
