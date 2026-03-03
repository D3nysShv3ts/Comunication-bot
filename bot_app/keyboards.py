from aiogram.types import *
from bot_config import TEACHERS



def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👤 Мій профіль")],
            [KeyboardButton(text="✏️ Змінити ім'я"), KeyboardButton(text="📚 Змінити клас")],
            [KeyboardButton(text="✉️ Написати вчителю")],
            [KeyboardButton(text="🗑️ Видалити профіль")]
        ],
        resize_keyboard=True
    )


def admin_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👤 Мій профіль")],
            [KeyboardButton(text="✏️ Змінити ім'я"), KeyboardButton(text="📚 Змінити клас")],
            [KeyboardButton(text="✉️ Написати вчителю")],
            [KeyboardButton(text="📊 Почати опитування"), KeyboardButton(text="👀 Переглянути результати")]
        ],
        resize_keyboard=True
    )


def teacher_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👤 Мій профіль")],
            [KeyboardButton(text="✏️ Змінити ім'я"), KeyboardButton(text="📚 Змінити клас")],
            [KeyboardButton(text="📊 Почати опитування"), KeyboardButton(text="👀 Переглянути результати")]
        ],
        resize_keyboard=True
    )


def subjects_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=s, callback_data=f"subj:{s}")]
            for s in TEACHERS
        ]
    )


def teachers_keyboard(subject):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=name, callback_data=f"teacher:{tid}")]
            for name, tid in TEACHERS[subject].items()
        ]
    )


def reply_keyboard(student_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="↩️ Відповісти", callback_data=f"reply:{student_id}")
        ]]
    )

def play_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Переглянути свої бали")],
            [InlineKeyboardButton(text="Жребі"), InlineKeyboardButton(text="Дартс")],
            [InlineKeyboardButton(text="Кільце")]
        ]
    )