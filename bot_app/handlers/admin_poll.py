import aiosqlite
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from ..bot_config import DB_NAME, ADMIN_IDS
from ..states import AdminStates

router = Router()



@router.message(Command("send_poll"))
@router.message(F.text == "📊 Почати опитування")
async def send_poll(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ Немає прав")
        return

    await message.answer("✏️ Введи питання:")
    await state.set_state(AdminStates.waiting_for_poll_question)


@router.message(AdminStates.waiting_for_poll_question)
async def poll_question_received(message: Message, state: FSMContext):
    await state.update_data(question=message.text.strip())
    await message.answer("Введи варіанти через кому:")
    await state.set_state(AdminStates.waiting_for_poll_options)


@router.message(AdminStates.waiting_for_poll_options)
async def poll_options_received(message: Message, state: FSMContext):
    data = await state.get_data()
    question = data["question"]

    options = [o.strip() for o in message.text.split(",") if o.strip()]

    if len(options) < 2:
        await message.answer("❌ Потрібно хоча б 2 варіанти")
        return

    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "INSERT INTO polls(question) VALUES (?)",
            (question,)
        )
        poll_id = cursor.lastrowid

        for opt in options:
            await db.execute(
                "INSERT INTO poll_options(poll_id, option_text) VALUES (?,?)",
                (poll_id, opt)
            )

        await db.commit()


        async with db.execute("SELECT user_id FROM users") as cur:
            users = await cur.fetchall()


        for user in users:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[])

            for i, opt in enumerate(options):
                keyboard.inline_keyboard.append([
                    InlineKeyboardButton(
                        text=opt,
                        callback_data=f"vote:{poll_id}:{i}"
                    )
                ])

            msg = await message.bot.send_message(
                user[0],
                f"📊 {question}",
                reply_markup=keyboard
            )

            await db.execute(
                "INSERT INTO poll_messages(poll_id,user_id,message_id) VALUES (?,?,?)",
                (poll_id, user[0], msg.message_id)
            )

        await db.commit()

    await state.clear()
    await message.answer("✅ Опитування відправлено всім")



@router.callback_query(F.data.startswith("vote:"))
async def vote_callback(callback: CallbackQuery):
    data = callback.data.split(":")
    poll_id = int(data[1])
    option_index = int(data[2])
    user_id = callback.from_user.id

    async with aiosqlite.connect(DB_NAME) as db:

        async with db.execute(
            "SELECT option_id FROM poll_options WHERE poll_id=? ORDER BY option_id",
            (poll_id,)
        ) as cur:
            options = await cur.fetchall()

        option_id = options[option_index][0]


        await db.execute("""
            INSERT INTO poll_results(poll_id,user_id,option_id)
            VALUES(?,?,?)
            ON CONFLICT(poll_id,user_id)
            DO UPDATE SET option_id=excluded.option_id
        """, (poll_id, user_id, option_id))

        await db.commit()


        results = {}
        for i, opt in enumerate(options):
            async with db.execute(
                "SELECT COUNT(*) FROM poll_results WHERE poll_id=? AND option_id=?",
                (poll_id, opt[0])
            ) as cur2:
                results[i] = (await cur2.fetchone())[0]

        async with db.execute(
            "SELECT question FROM polls WHERE poll_id=?",
            (poll_id,)
        ) as cur3:
            question_text = (await cur3.fetchone())[0]


        text_result = f"📊 {question_text}\n\n"

        for i, opt in enumerate(options):
            async with db.execute(
                "SELECT option_text FROM poll_options WHERE option_id=?",
                (opt[0],)
            ) as cur4:
                opt_text = (await cur4.fetchone())[0]

            text_result += f"{opt_text}: {results[i]} голосів\n"


        async with db.execute(
            "SELECT user_id,message_id FROM poll_messages WHERE poll_id=?",
            (poll_id,)
        ) as cur5:
            rows = await cur5.fetchall()

        for u_id, msg_id in rows:
            try:
                await callback.bot.edit_message_text(
                    text_result,
                    u_id,
                    msg_id
                )
            except:
                pass

    await callback.answer("✅ Голос зараховано!")




@router.message(Command("poll_results"))
@router.message(F.text == "👀 Переглянути результати")
async def show_poll_results(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ Немає прав")
        return

    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT poll_id, question FROM polls ORDER BY poll_id DESC LIMIT 1"
        ) as cur:
            poll = await cur.fetchone()

        if not poll:
            await message.answer("❌ Опитувань ще не було")
            return

        poll_id, question = poll

        async with db.execute(
            "SELECT option_id, option_text FROM poll_options WHERE poll_id=? ORDER BY option_id",
            (poll_id,)
        ) as cur2:
            options = await cur2.fetchall()

        text_result = f"📊 Результати опитування:\n{question}\n\n"

        for opt_id, opt_text in options:
            async with db.execute(
                "SELECT COUNT(*) FROM poll_results WHERE poll_id=? AND option_id=?",
                (poll_id, opt_id)
            ) as cur3:
                count = (await cur3.fetchone())[0]

            text_result += f"{opt_text}: {count} голосів\n"

    await message.answer(text_result)
