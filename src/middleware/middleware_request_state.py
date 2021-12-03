

import fastapi

import src.state.state_request


async def middleware(
        request: fastapi.Request,
        call_next
) -> fastapi.Response:
    response: fastapi.Response

    # Set default request state.
    request.state.current = src.state.state_request.StateRequest()

    # Middleware forward pass.
    response = await call_next(
        request
    )

    # Middleware downhill pass.
    return response
