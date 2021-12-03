import fastapi

import src.state.state_app


def depends(
        request: fastapi.Request
) -> src.state.state_app.StateApp:
    return request.app.state
