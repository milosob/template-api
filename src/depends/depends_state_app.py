import typing

import fastapi

import src.state.state_app


class DependsStateApp:

    def __init__(
            self
    ) -> None:
        pass

    def __call__(
            self,
            request: fastapi.Request
    ) -> src.state.state_app.StateApp:
        return request.app.state


def depends(
) -> typing.Any:
    return fastapi.Depends(
        DependsStateApp()
    )
