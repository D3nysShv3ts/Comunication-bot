import aiosqlite
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from ..bot_config import DB_NAME, ADMIN_IDS
from ..states import Register
from ..keyboards import main_keyboard, admin_keyboard, teacher_keyboard
from ..utils import is_teacher, is_admin, is_valid_name, normalize_grade

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    if message.from_user.username is None:
        await message.answer("❗ Створи username у Telegram")
        return

    uid = message.from_user.id

    async with aiosqlite.connect(DB_NAME) as db:
        cur = await db.execute("SELECT name FROM users WHERE user_id=?", (uid,))
        user = await cur.fetchone()

    if user:
        kb = admin_keyboard() if uid in ADMIN_IDS else main_keyboard()
        if is_teacher(uid):
            kb = teacher_keyboard()
        await message.answer(f"👋 Привіт, {user[0]}!", reply_markup=kb)
    else:
        await message.answer(
            "👋 Вітаю! Як тебе звати?",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(Register.waiting_for_name)


@router.message(Register.waiting_for_name)
async def reg_name(message: Message, state: FSMContext):
    if not is_valid_name(message.text):
        await message.answer("❌ Некоректне імʼя")
        return

    await state.update_data(name=message.text)

    if is_teacher(message.from_user.id) or is_admin(message.from_user.id):
        await message.answer("📚 Введи клас або `не керую`")
    else:
        await message.answer("📚 З якого ти класу?")

    await state.set_state(Register.waiting_for_grade)


@router.message(Register.waiting_for_grade)
async def reg_grade(message: Message, state: FSMContext):
    uid = message.from_user.id
    data = await state.get_data()

    grade = "не керую" if message.text.lower() == "не керую" else normalize_grade(message.text)
    if not grade:
        await message.answer("❌ Некоректний клас")
        return

    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT OR REPLACE INTO users VALUES (?,?,?)",
            (uid, data["name"], grade)
        )
        await db.commit()

    await state.clear()

    kb = main_keyboard()
    if is_teacher(uid):
        kb = teacher_keyboard()
    if is_admin(uid):
        kb = admin_keyboard()

    await message.answer("✅ Реєстрація завершена", reply_markup=kb)
