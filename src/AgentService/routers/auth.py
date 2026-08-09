from AgentService.schemas.auth_schemas import RegisterRequest, RegisterResponse
from AgentService.services.auth_service import signup
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from AgentService.dependencies import get_db


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post(
    "/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED
)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)):
    return await signup(db, payload)
    