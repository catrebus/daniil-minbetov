import datetime
from abc import ABC, abstractmethod
from typing import List
from zoneinfo import ZoneInfo

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_models import Users


class UserRepositoryProtocol(ABC):

    @abstractmethod
    async def add_user(self, tg_id: int): ...

    @abstractmethod
    async def user_exists(self, tg_id: int) -> bool: ...

    @abstractmethod
    async def is_admin(self, tg_id: int) -> bool: ...

    @abstractmethod
    async def get_users(self) -> List[Users]: ...

class UserRepository(UserRepositoryProtocol):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user(self, tg_id: int) -> None:
        obj = Users(telegram_id=tg_id, created_at=datetime.datetime.now(ZoneInfo("Europe/Moscow")), is_admin=0)
        self.session.add(obj)

    async def user_exists(self, tg_id: int) -> bool:
        result = await self.session.execute(
            select(Users).where(Users.telegram_id == tg_id)
        )
        return result.scalar() is not None

    async def is_admin(self, tg_id: int) -> bool:
        result = await self.session.execute(
            select(Users.is_admin).where(Users.telegram_id == tg_id)
        )
        value = result.scalar()
        return bool(value) if value is not None else False

    async def get_users(self) -> List[Users]:
        result = await self.session.execute(select(Users))
        return result.scalars().all()