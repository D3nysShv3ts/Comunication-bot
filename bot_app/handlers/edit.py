import aiosqlite
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from ..bot_config import DB_NAME
from ..states import EditName, EditGrade
from ..keyboards import main_keyboard, admin_keyboard, teacher_keyboard
from ..utils import is_teacher, is_admin, is_valid_name, normalize_grade

router = Router()


@router.message(F.text == "✏️ Змінити ім'я")
async def edit_name(message: Message, state: FSMContext):
    await message.answer("✏️ Введи нове імʼя:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(EditName.waiting_for_new_name)


@router.message(EditName.waiting_for_new_name)
async def save_name(message: Message, state: FSMContext):
    if not is_valid_name(message.text):
        await message.answer("❌ Некоректне імʼя")
        return

    uid = message.from_user.id

    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE users SET name=? WHERE user_id=?", (message.text, uid))
        await db.commit()

    kb = main_keyboard()
    if is_teacher(uid):
        kb = teacher_keyboard()
    if is_admin(uid):
        kb = admin_keyboard()

    await message.answer("✅ Імʼя змінено", reply_markup=kb)
    await state.clear()


@router.message(F.text == "📚 Змінити клас")
async def edit_grade(message: Message, state: FSMContext):
    await message.answer("📚 Введи новий клас:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(EditGrade.waiting_for_new_grade)


@router.message(EditGrade.waiting_for_new_grade)
async def save_grade(message: Message, state: FSMContext):
    uid = message.from_user.id

    grade = "не керую" if is_teacher(uid) and message.text.lower()=="не керую" else normalize_grade(message.text)
    if not grade:
        await message.answer("❌ Некоректний клас")
        return

    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE users SET grade=? WHERE user_id=?", (grade, uid))
        await db.commit()

    kb = main_keyboard()
    if is_teacher(uid):
        kb = teacher_keyboard()
    if is_admin(uid):
        kb = admin_keyboard()

    await message.answer("✅ Клас змінено", reply_markup=kb)
    await state.clear()
