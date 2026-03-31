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
    closed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    user_guesses: Mapped[list['UserGuesses']] = relationship('UserGuesses', back_populates='bet')


class Users(Base):
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_admin: Mapped[Optional[int]] = mapped_column(TINYINT)

    user_guesses: Mapped[list['UserGuesses']] = relationship('UserGuesses', back_populates='telegram')


class UserGuesses(Base):
    __tablename__ = 'user_guesses'
    __table_args__ = (
        ForeignKeyConstraint(['bet_id'], ['bets.id'], name='bet_id_user_guesses'),
        ForeignKeyConstraint(['telegram_id'], ['users.telegram_id'], name='telegram_id_user_guesses'),
        Index('bet_id_user_guesses_idx', 'bet_id'),
        Index('telegram_id_user_guesses_idx', 'telegram_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bet_id: Mapped[Optional[int]] = mapped_column(Integer)
    telegram_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    guess: Mapped[Optional[int]] = mapped_column(TINYINT)

    bet: Mapped[Optional['Bets']] = relationship('Bets', back_populates='user_guesses')
    telegram: Mapped[Optional['Users']] = relationship('Users', back_populates='user_guesses')
