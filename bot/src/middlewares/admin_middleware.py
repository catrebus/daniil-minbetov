from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from typing import Callable, Awaitable, Any

from core import container


class AdminMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict], Awaitable[Any]],
            event: TelegramObject,
            data: dict
    ) -> Any:
        user = data.get("event_from_user")

        service = container.user_service()
        exists = await service.user_exists(user.id)

        if not exists:
            return

        return await handler(event, data)