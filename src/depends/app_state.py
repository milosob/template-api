import typing

import fastapi

import src.app_state


class AppState:

    def __init__(
            self
    ) -> None:
        pass

    def __call__(
            self,
            request: fastapi.Request
    ) -> src.app_state.AppState:
        return request.app.state


def depends(
) -> typing.Any:
    return fastapi.Depends(
        AppState()
    )
