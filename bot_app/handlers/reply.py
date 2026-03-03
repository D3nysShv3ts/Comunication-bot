import aiosqlite
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from ..states import ReplyToStudent
from ..bot_config import DB_NAME

router = Router()


@router.callback_query(F.data.startswith("reply:"))
async def reply_start(callback: CallbackQuery, state: FSMContext):
    await state.update_data(student_id=int(callback.data.split(":")[1]))
    await callback.message.answer("✏️ Введи відповідь:")
    await state.set_state(ReplyToStudent.text)


@router.message(ReplyToStudent.text)
async def reply_send(message: Message, state: FSMContext):
    data = await state.get_data()

    async with aiosqlite.connect(DB_NAME) as db:
        cur = await db.execute(
            "SELECT name FROM users WHERE user_id=?",
            (message.from_user.id,)
        )
        name = (await cur.fetchone())[0]

    await message.bot.send_message(
        data["student_id"],
        f"📩 Відповідь від {name}:\n\n{message.text}"
    )

    await message.answer("✅ Відповідь надіслана")
    await state.clear()
