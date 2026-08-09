from argon2 import Type
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher


from sqlalchemy.ext.asyncio import AsyncSession

from database.models.db_schemas import UserTable
from AgentService.schemas.auth_schemas import RegisterRequest
from AgentService.repository.user_repository import get_user, create_user
from utils.exception import EmailAlreadyExistError

password_hash = PasswordHash(
    (Argon2Hasher(time_cost=3, memory_cost=65536, parallelism=4, type=Type.ID),)
)


# create registeration function
async def signup(db: AsyncSession, payload: RegisterRequest) -> UserTable:
    # check if user is already registered by checking if email already exist
    existing_user = await get_user(db, user_email=payload.email)

    if existing_user:
        raise EmailAlreadyExistError

    # get the user name, password, email and save in db
    hashed_password = password_hash.hash(payload.password)

    return await create_user(
        db,
        user_email=payload.email,
        user_name=payload.username,
        hashed_password=hashed_password,
    )



# create signin function
