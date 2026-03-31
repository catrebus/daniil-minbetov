import asyncio
import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import select, func

from db import Bets


async def daily_bet_creator(session_factory):
    while True:
        now = datetime.datetime.now(ZoneInfo("Europe/Moscow"))
        today = now.date()

        if today.weekday() not in (5, 6):
            async with session_factory() as session:
                existing = await session.execute(
                    select(Bets).where(func.date(Bets.date) == today)
                )
                if not existing.scalar_one_or_none():
                    bet = Bets(date=now)
                    session.add(bet)
                    await session.commit()

        next_midnight = (now + datetime.timedelta(days=1)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        seconds_until_midnight = (next_midnight - now).total_seconds()
        await asyncio.sleep(seconds_until_midnight)