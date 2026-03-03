import aiosqlite
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from ..bot_config import DB_NAME
from ..utils import get_role, is_teacher

router = Router()


@router.message(Command("profile"))
@router.message(F.text == "👤 Мій профіль")
async def profile(message: Message):
    uid = message.from_user.id

    async with aiosqlite.connect(DB_NAME) as db:
        cur = await db.execute(
            "SELECT name, grade FROM users WHERE user_id=?", (uid,)
        )
        user = await cur.fetchone()

    if not user:
        await message.answer("❌ Профіль не знайдено")
        return

    name, grade = user
    role = get_role(uid)

    text = f"👤 Імʼя: {name}\n🎭 Ви: {role}\n"
    text += f"📚 Клас: {grade}"

    await message.answer(text)
