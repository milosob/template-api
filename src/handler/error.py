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
        src.dto.error.ErrorApiOut.construct(
            code=exc.code,
            type=exc.type
        ).json(),
        exc.code,
        None,
        "application/json"
    )
