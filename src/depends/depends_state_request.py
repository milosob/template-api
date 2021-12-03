import fastapi

import src.state.state_request


def depends(
        request: fastapi.Request
) -> src.state.state_request.StateRequest:
    return request.state.current
