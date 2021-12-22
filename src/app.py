import asyncio
import logging
import typing

import fastapi
import fastapi.middleware.cors
import hypercorn.config
import hypercorn.asyncio

import src.app_state
import src.handler.error
import src.router.account


def run(
        config: dict
) -> None:
    # log configuration
    logging.basicConfig(
        level=config["log"]["level"]
    )

    # app middleware
    app_middleware: typing.List[fastapi.middleware.Middleware]
    app_middleware = []

    # app middleware internal pre
    app_middleware.extend(
        [

        ]
    )

    # app middleware cors
    if "cors" in config["middleware"] and config["middleware"]["cors"]["enabled"]:
        app_middleware.append(
            fastapi.middleware.Middleware(
                cls=fastapi.middleware.cors.CORSMiddleware,
                **{
                    **config["middleware"]["cors"]["options"]
                }
            )
        )

    # app middleware internal after
    app_middleware.extend(
        [

        ]
    )

    # app exception handlers
    app_exception_handlers: dict
    app_exception_handlers = {
        src.handler.error.error_type: src.handler.error.handler
    }

    # app build
    app = fastapi.FastAPI(
        middleware=app_middleware,
        exception_handlers=app_exception_handlers
    )

    # app routers
    app.include_router(
        router=src.router.account.router
    )

    # app state
    app.state = src.app_state.AppState(
        config=config["state"]
    )

    # app net
    app_serve_config: hypercorn.Config
    app_serve_config = hypercorn.Config()

    app_serve_config.bind.clear()

    for host, port in config["bind"].items():
        app_serve_config.bind.append(
            f"{host}:{port}"
        )

    asyncio.run(
        hypercorn.asyncio.serve(
            app=app,
            config=app_serve_config
        )
    )
