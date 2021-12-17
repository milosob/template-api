import asyncio

import fastapi
import fastapi.security

import src.app_state
import src.database.me.filter
import src.database.me.update
import src.database.me.model
import src.depends.bearer_token
import src.depends.app_state
import src.dto.error
import src.dto.me
import src.error.error
import src.error.error_type

router = fastapi.APIRouter(
    prefix="/me",
    tags=["me"]
)

error_responses: dict = {
    fastapi.status.HTTP_400_BAD_REQUEST: {
        "model": src.dto.error.ErrorApiOut,
        "description": "Error."
    },
    fastapi.status.HTTP_401_UNAUTHORIZED: {
        "model": src.dto.error.ErrorApiOut,
        "description": "Error."
    },
    fastapi.status.HTTP_404_NOT_FOUND: {
        "model": src.dto.error.ErrorApiOut,
        "description": "Error."
    },
    fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": src.dto.error.ErrorApiOut,
        "description": "Error."
    },
    fastapi.status.HTTP_503_SERVICE_UNAVAILABLE: {
        "model": src.dto.error.ErrorApiOut,
        "description": "Error."
    }
}


@router.get(
    path="",
    summary="Fetch resource.",
    status_code=fastapi.status.HTTP_200_OK,
    responses=error_responses | {
        fastapi.status.HTTP_200_OK: {
            "model": src.dto.me.MeGetOut,
            "description": "Resource fetched."
        },
    }
)
async def me_get(
        request: fastapi.Request,
        app_state: src.app_state.AppState = src.depends.app_state.depends(),
        me_get_in: src.dto.me.MeGetIn = fastapi.Depends()
):
    pass


@router.put(
    path="",
    summary="Modify resource.",
    status_code=fastapi.status.HTTP_201_CREATED,
    responses=error_responses | {
        fastapi.status.HTTP_201_CREATED: {
            "model": src.dto.me.MePutIn,
            "description": "Resource modified."
        },
    }
)
async def me_put(
        request: fastapi.Request,
        app_state: src.app_state.AppState = src.depends.app_state.depends(),
        me_put_in: src.dto.me.MePutIn = fastapi.Depends()
):
    pass


@router.post(
    path="",
    summary="Create resource.",
    status_code=fastapi.status.HTTP_201_CREATED,
    responses=error_responses | {
        fastapi.status.HTTP_201_CREATED: {
            "model": src.dto.me.MePostIn,
            "description": "Resource created."
        },
    }
)
async def me_post(
        request: fastapi.Request,
        app_state: src.app_state.AppState = src.depends.app_state.depends(),
        me_post_in: src.dto.me.MePostIn = fastapi.Depends()
):
    pass
