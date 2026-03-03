import time
from collections import defaultdict
from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery


class RateLimitMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

        # Ліміти в секундах
        self.limits = {
            "message": 1.5,
            "callback": 1.0
        }

        # user_id -> action -> last_time
        self.user_actions: Dict[int, Dict[str, float]] = defaultdict(dict)

    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any]
    ):

        user_id = None
        action_type = None


        if isinstance(event, Message):
            user_id = event.from_user.id
            action_type = "message"

        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
            action_type = "callback"


        if not user_id or not action_type:
            return await handler(event, data)

        now = time.time()
        last_time = self.user_actions[user_id].get(action_type, 0)
        limit = self.limits.get(action_type, 1.0)


        if now - last_time < limit:


            if isinstance(event, CallbackQuery):
                await event.answer("⏳ Зачекайте...", show_alert=False)
            else:
                await event.answer("⏳ Не спамте. Зачекайте трохи.")
            return

        self.user_actions[user_id][action_type] = now

        return await handler(event, data)
