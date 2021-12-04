import asyncio
import logging

import fastapi
import fastapi.middleware.cors
import hypercorn.config
import hypercorn.asyncio
import starlette.middleware.base

import src.handler.handler_error_validation
import src.middleware.middleware_request_state
import src.middleware.middleware_request_state_lang
import src.router.router_account
import src.router.router_confirm
import src.state.state_app


def run(
        config: dict
) -> None:
    # log configuration
    logging.basicConfig(
        level=config["log"]["level"]
    )

    # app build
    app = fastapi.FastAPI()

    # app error handlers
    app.add_exception_handler(
        src.handler.handler_error_validation.error_type,
        src.handler.handler_error_validation.handler
    )

    # app middleware
    app_middlewares = [
        src.middleware.middleware_request_state.middleware,
        src.middleware.middleware_request_state_lang.middleware
    ]

    # app middleware register in reverse order
    for app_middleware in app_middlewares[::-1]:
        app.add_middleware(
            starlette.middleware.base.BaseHTTPMiddleware,
            dispatch=app_middleware
        )

    app.add_middleware(
        fastapi.middleware.cors.CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # app routers
    app.include_router(
        router=src.router.router_account.router
    )

    app.include_router(
        router=src.router.router_confirm.router
    )

    # app state
    app.state = src.state.state_app.StateApp(
        config=config["app"]
    )

    # app networking
    use_ipv4: bool = config["net"]["ipv4"]
    use_ipv4_ssl: bool = config["net"]["ipv4_ssl"]
    use_ipv6: bool = config["net"]["ipv6"]
    use_ipv6_ssl: bool = config["net"]["ipv6_ssl"]
    use_ssl: bool = config["net"]["ssl"]

    app_serve_config: hypercorn.Config = hypercorn.Config()

    app_serve_config.bind.clear()

    if use_ipv4:
        host: str = config["net"]["ipv4_host"]
        port: int = config["net"]["ipv4_port"]

        app_serve_config.bind.append(
            f"{host}:{port}"
        )

    if use_ipv6:
        host: str = config["net"]["ipv6_host"]
        port: int = config["net"]["ipv6_port"]

        app_serve_config.bind.append(
            f"{host}:{port}"
        )

    asyncio.run(
        hypercorn.asyncio.serve(
            app=app,
            config=app_serve_config
        )
    )
