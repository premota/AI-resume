from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from utils.exception import EmailAlreadyExistError

from database.models.db_schemas import UserTable


async def get_user(db: AsyncSession, user_email: str) -> UserTable | None:
    db_statement = select(UserTable).where(UserTable.email == user_email)
    user_info = (await db.scalars(db_statement)).first()
    return user_info


async def create_user(
    db: AsyncSession, user_email: str, user_name: str, hashed_password: str
) -> UserTable:
    user = UserTable(email=user_email, username=user_name, password=hashed_password)

    db.add(user)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise EmailAlreadyExistError()
    await db.refresh(user)
    return user
