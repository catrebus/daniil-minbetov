from typing import Optional
import datetime

from sqlalchemy import BigInteger, Date, DateTime, ForeignKeyConstraint, Index, Integer
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(AsyncAttrs, DeclarativeBase):
    pass


class Bets(Base):
    __tablename__ = 'bets'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    result: Mapped[Optional[int]] = mapped_column(TINYINT)

    user_bets: Mapped[list['UserBets']] = relationship('UserBets', back_populates='bet')


class Users(Base):
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_admin: Mapped[Optional[int]] = mapped_column(TINYINT)

    user_bets: Mapped[list['UserBets']] = relationship('UserBets', back_populates='telegram')


class UserBets(Base):
    __tablename__ = 'user_bets'
    __table_args__ = (
        ForeignKeyConstraint(['bet_id'], ['bets.id'], name='bet_id_user_bets'),
        ForeignKeyConstraint(['telegram_id'], ['users.telegram_id'], name='telegram_id_user_bets'),
        Index('bet_id_user_bets_idx', 'bet_id'),
        Index('telegram_id_user_bets_idx', 'telegram_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bet_id: Mapped[Optional[int]] = mapped_column(Integer)
    telegram_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    bet_value: Mapped[Optional[int]] = mapped_column(TINYINT)

    bet: Mapped[Optional['Bets']] = relationship('Bets', back_populates='user_bets')
    telegram: Mapped[Optional['Users']] = relationship('Users', back_populates='user_bets')
