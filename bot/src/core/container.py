from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from core import Config
from repositories.bet_repository import BetRepository
from repositories.user_bets_repository import UserBetsRepository
from repositories.user_repository import UserRepository
from services.bet_service import BetService
from services.user_bets_service import UserBetsService

from services.user_service import UserService


class Container:
    def __init__(self):
        # ------ Config ------
        self.config = Config()

        # ------ Database ------
        self.engine = create_async_engine(self.config.DATABASE_URL, echo=True)
        self.SessionLocal = async_sessionmaker(bind=self.engine, expire_on_commit=False)

        # ------ Services that are singletons ------

    # ------ Dependencies -----
    def user_repository(self, session: AsyncSession) -> UserRepository:
        return UserRepository(session)

    def bet_repository(self, session: AsyncSession) -> BetRepository:
        return BetRepository(session)

    def user_bets_repository(self, session: AsyncSession) -> UserBetsRepository:
        return UserBetsRepository(session)

    def user_service(self) -> UserService:
        return UserService(self.SessionLocal, self.user_repository)

    def bet_service(self) -> BetService:
        return BetService(self.SessionLocal, self.bet_repository)

    def user_bets_service(self) -> UserBetsService:
        return UserBetsService(self.SessionLocal, self.user_bets_repository)


container = Container()