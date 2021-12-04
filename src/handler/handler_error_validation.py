import typing

import fastapi
import fastapi.responses
import pydantic

import src.depends.depends_state_request
import src.state.state_request

error_type = pydantic.ValidationError


async def handler(
        request: fastapi.Request,
        exc: pydantic.ValidationError,
):
    state_request: src.state.state_request.StateRequest
    state_request = src.depends.depends_state_request.depends(
        request=request
    )

    # 1. TODO Perform errors translation into message based on desired lang.

    return fastapi.responses.JSONResponse(
        status_code=fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=exc.errors(),
    )
