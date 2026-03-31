from abc import ABC, abstractmethod
from typing import List

from db.db_models import Users


class UserServiceProtocol(ABC):

    @abstractmethod
    async def add_user(self, tg_id: int) -> None: ...

    @abstractmethod
    async def user_exists(self, tg_id: int) -> bool: ...

    @abstractmethod
    async def is_admin(self, tg_id: int) -> bool: ...

    @abstractmethod
    async def get_users(self) -> List[Users]: ...

class UserService(UserServiceProtocol):

    def __init__(self, SessionLocal, user_repo_factory):
        self.SessionLocal = SessionLocal
        self.user_repo_factory = user_repo_factory

    async def add_user(self, tg_id: int) -> None:
        async with self.SessionLocal() as session:
            user_repo = self.user_repo_factory(session)
            if not await user_repo.user_exists(tg_id):
                await user_repo.add_user(tg_id)
                await session.commit()

    async def user_exists(self, tg_id: int) -> bool:
        async with self.SessionLocal() as session:
            repo = self.user_repo_factory(session)
            return await repo.user_exists(tg_id)

    async def is_admin(self, tg_id: int) -> bool:
        async with self.SessionLocal() as session:
            repo = self.user_repo_factory(session)
            return await repo.is_admin(tg_id)

    async def get_users(self) -> List[Users]:
        async with self.SessionLocal() as session:
            repo = self.user_repo_factory(session)
            return repo.get_users()