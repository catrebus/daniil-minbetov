from abc import ABC, abstractmethod

from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_models import Bets, UserBets


class UserBetsRepositoryProtocol(ABC):

    @abstractmethod
    async def get_last_bet_result(self): ...

    @abstractmethod
    async def do_bet(self, telegram_id: int, bet_value: int): ...

    async def get_bets_by_last_bet(self) -> list[list]: ...

class UserBetsRepository(UserBetsRepositoryProtocol):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_last_bet_result(self):
        result = await self.session.execute(
            select(
                UserBets.id,
                UserBets.bet_id,
                Bets.result,
                UserBets.telegram_id,
                UserBets.bet_value
            )
            .join(Bets, UserBets.bet_id == Bets.id)
            .where(UserBets.bet_id == select(func.max(UserBets.bet_id)).scalar_subquery())
        )
        return result.all()

    async def do_bet(self, telegram_id: int, bet_value: int):
        last_bet_id = await self.session.execute(
            select(func.max(Bets.id))
        )
        last_bet_id = last_bet_id.scalar()

        existing = await self.session.execute(
            select(UserBets).where(
                UserBets.bet_id == last_bet_id,
                UserBets.telegram_id == telegram_id
            )
        )
        existing = existing.scalar()

        if existing:
            await self.session.execute(
                update(UserBets)
                .where(UserBets.id == existing.id)
                .values(bet_value=bet_value)
            )
        else:
            obj = UserBets(
                bet_id=last_bet_id,
                telegram_id=telegram_id,
                bet_value=bet_value
            )
            self.session.add(obj)

    async def get_bets_by_last_bet(self) -> list[list]:
        result = await self.session.execute(
            select(UserBets.telegram_id, UserBets.bet_value)
            .where(UserBets.bet_id == select(func.max(Bets.id)).scalar_subquery())
        )
        return [list(row) for row in result.all()]

