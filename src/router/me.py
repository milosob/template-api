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
