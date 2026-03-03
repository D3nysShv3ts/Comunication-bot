import aiosqlite
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from ..states import PMTeacher
from ..keyboards import subjects_keyboard, teachers_keyboard, reply_keyboard
from ..bot_config import DB_NAME
from ..utils import is_rate_limited


router = Router()




@router.message(F.text == "✉️ Написати вчителю")
async def write_teacher(message: Message, state: FSMContext):
    if is_rate_limited(message.from_user.id, "pm"):
        await message.answer("⏳ Зачекайте трохи перед повторною відправкою.")
        return

    if message.from_user.username is None:
        await message.answer("❗ Спочатку створіть username у Telegram.")
        return

    await message.answer(
        "📚 Оберіть предмет:",
        reply_markup=subjects_keyboard()
    )

    await state.set_state(PMTeacher.subject)



@router.callback_query(F.data.startswith("subj:"))
async def choose_subject(callback: CallbackQuery, state: FSMContext):
    if is_rate_limited(callback.from_user.id, "callback"):
        await callback.answer("⏳ Зачекайте...", show_alert=False)
        return

    subject = callback.data.split("subj:")[1]
    await state.update_data(subject=subject)

    await callback.message.edit_text(
        "👩‍🏫 Оберіть вчителя:",
        reply_markup=teachers_keyboard(subject)
    )




@router.callback_query(F.data.startswith("teacher:"))
async def choose_teacher(callback: CallbackQuery, state: FSMContext):
    if is_rate_limited(callback.from_user.id, "callback"):
        await callback.answer("⏳ Зачекайте...", show_alert=False)
        return

    teacher_id = int(callback.data.split(":")[1])
    await state.update_data(teacher_id=teacher_id)

    await callback.message.answer("✏️ Напишіть повідомлення:")
    await state.set_state(PMTeacher.text)




@router.message(PMTeacher.text)
async def send_teacher(message: Message, state: FSMContext):
    if is_rate_limited(message.from_user.id, "pm"):
        await message.answer("⏳ Зачекайте трохи перед повторною відправкою.")
        return

    data = await state.get_data()
    teacher_id = data.get("teacher_id")

    if not teacher_id:
        await message.answer("❌ Сталася помилка. Спробуйте ще раз.")
        await state.clear()
        return

    async with aiosqlite.connect(DB_NAME) as db:
        cur = await db.execute(
            "SELECT name, grade FROM users WHERE user_id=?",
            (message.from_user.id,)
        )
        user = await cur.fetchone()

    if not user:
        await message.answer("❌ Профіль не знайдено.")
        await state.clear()
        return

    name, grade = user

    await message.bot.send_message(
        teacher_id,
        f"📩 Повідомлення від {name} ({grade} клас):\n\n{message.text}",
        reply_markup=reply_keyboard(message.from_user.id)
    )

    await message.answer("✅ Повідомлення надіслано.")
    await state.clear()
