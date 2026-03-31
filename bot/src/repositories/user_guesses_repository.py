from abc import ABC, abstractmethod

from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_models import Bets, UserGuesses


class UserGuessesRepositoryProtocol(ABC):

    @abstractmethod
    async def get_last_bet_result(self): ...

    @abstractmethod
    async def do_bet(self, telegram_id: int, bet_value: int): ...

    @abstractmethod
    async def get_bets_by_last_bet(self) -> list[list]: ...

    @abstractmethod
    async def get_user_statistic(self, telegram_id: int): ...


class UserGuessesRepository(UserGuessesRepositoryProtocol):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_last_bet_result(self):
        result = await self.session.execute(
            select(
                UserGuesses.id,
                UserGuesses.bet_id,
                Bets.result,
                UserGuesses.telegram_id,
                UserGuesses.guess
            )
            .join(Bets, UserGuesses.bet_id == Bets.id)
            .where(UserGuesses.bet_id == select(func.max(UserGuesses.bet_id)).scalar_subquery())
        )
        return result.all()

    async def do_bet(self, telegram_id: int, guess: int):
        """Пользователь делает ставку"""
        last_bet_id = await self.session.execute(
            select(func.max(Bets.id))
        )
        last_bet_id = last_bet_id.scalar()

        existing = await self.session.execute(
            select(UserGuesses).where(
                UserGuesses.bet_id == last_bet_id,
                UserGuesses.telegram_id == telegram_id
            )
        )
        existing = existing.scalar()

        if existing:
            await self.session.execute(
                update(UserGuesses)
                .where(UserGuesses.id == existing.id)
                .values(guess=guess)
            )
        else:
            obj = UserGuesses(
                bet_id=last_bet_id,
                telegram_id=telegram_id,
                guess=guess
            )
            self.session.add(obj)

    async def get_bets_by_last_bet(self) -> list[list]:
        result = await self.session.execute(
            select(UserGuesses.telegram_id, UserGuesses.guess)
            .where(UserGuesses.bet_id == select(func.max(Bets.id)).scalar_subquery())
        )
        return [list(row) for row in result.all()]

    async def get_user_statistic(self, telegram_id: int):
        """Получение статистики пользователя (Количество правильных ставок, ...)"""
        stmt = select(
            UserGuesses.telegram_id,
            func.count(UserGuesses.id)
        ).join(
            Bets, UserGuesses.bet_id == Bets.id
        ).where(
            UserGuesses.guess == Bets.result,
            UserGuesses.telegram_id == telegram_id
        ).group_by(
            UserGuesses.telegram_id
        )

        result = await self.session.execute(stmt)
        return result.mappings().one_or_none()
