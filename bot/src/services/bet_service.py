from abc import ABC, abstractmethod


class BetServiceProtocol(ABC):

    @abstractmethod
    async def set_last_bet_result(self, result: bool): ...

class BetService(BetServiceProtocol):

    def __init__(self, SessionLocal, bet_repo_factory):
        self.SessionLocal = SessionLocal
        self.bet_repo_factory = bet_repo_factory

    async def set_last_bet_result(self, result: bool):
        async with self.SessionLocal() as session:
            repo = self.bet_repo_factory(session)
            await repo.set_last_bet_result(result)
            await session.commit()