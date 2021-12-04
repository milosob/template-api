import fastapi

import src.depends.depends_state_app
import src.depends.depends_state_request
import src.state.state_app
import src.state.state_request
import src.state.state_request_lang


async def middleware(
        request: fastapi.Request,
        call_next
) -> fastapi.Response:
    response: fastapi.Response

    state_app: src.state.state_app.StateApp
    state_app = src.depends.depends_state_app.depends(
        request=request
    )

    # Get request state.
    state_request: src.state.state_request.StateRequest
    state_request = src.depends.depends_state_request.depends(
        request=request
    )

    # Set request lang state.
    state_request.lang = src.state.state_request_lang.StateRequestLang(
        lang=state_app.service.service_lang.by_request(
            request=request
        )
    )

    # Middleware forward pass.
    response = await call_next(
        request
    )

    # Middleware downhill pass.
    return response
