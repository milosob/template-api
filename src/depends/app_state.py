import typing

import fastapi

import src.app_state


def depends(
) -> src.app_state.AppState:
    def dependency(
            request: fastapi.Request
    ) -> src.app_state.AppState:
        return request.app.state

    return fastapi.Depends(dependency)
