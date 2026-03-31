from abc import ABC, abstractmethod

class UserGuessesServiceProtocol(ABC):

    @abstractmethod
    async def get_last_bet_result(self): ...

    @abstractmethod
    async def do_bet(self, telegram_id: int, bet_value: int): ...

    @abstractmethod
    async def get_bets_by_last_bet(self) -> list[list]: ...

    @abstractmethod
    async def get_user_statistic(self, telegram_id: int): ...


class UserGuessesService(UserGuessesServiceProtocol):

    def __init__(self, SessionLocal, user_guesses_repo_factory):
        self.SessionLocal = SessionLocal
        self.user_guesses_repo_factory = user_guesses_repo_factory

    async def get_last_bet_result(self):
        async with self.SessionLocal() as session:
            repo = self.user_guesses_repo_factory(session)
            result = await repo.get_last_bet_result()

            winners = []
            losers = []

            for row in result:
                if row[2] == row[4]:
                    winners.append(row[3])
                else:
                    losers.append(row[3])

            return winners, losers

    async def do_bet(self, telegram_id: int, bet_value: int):
        async with self.SessionLocal() as session:
            repo = self.user_guesses_repo_factory(session)
            await repo.do_bet(telegram_id, bet_value)
            await session.commit()

    async def get_bets_by_last_bet(self) -> list[list]:
        async with self.SessionLocal() as session:
            repo = self.user_guesses_repo_factory(session)
            return await repo.get_bets_by_last_bet()

    async def get_user_statistic(self, telegram_id: int):
        """Получение статистики пользователя"""
        async with self.SessionLocal() as session:
            repo = self.user_guesses_repo_factory(session)