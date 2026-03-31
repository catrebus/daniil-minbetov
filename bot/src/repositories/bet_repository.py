import datetime
from abc import ABC, abstractmethod
from zoneinfo import ZoneInfo

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_models import Users, Bets


class BetRepositoryProtocol(ABC):

    @abstractmethod
    async def create_new_bet(self): ...

    @abstractmethod
    async def set_last_bet_result(self, result: bool): ...

class BetRepository(BetRepositoryProtocol):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_new_bet(self):
        obj = Bets(date=datetime.datetime.now(ZoneInfo("Europe/Moscow")) + datetime.timedelta(days=1))
        self.session.add(obj)

    async def set_last_bet_result(self, result: bool):
        id_result = await self.session.execute(
            select(Bets.id).order_by(Bets.id.desc()).limit(1)
        )
        last_bet_id = id_result.scalar()

        await self.session.execute(update(Bets).where(Bets.id == last_bet_id).values(result=result))