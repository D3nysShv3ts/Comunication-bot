from aiogram.fsm.state import State, StatesGroup


class Register(StatesGroup):
    waiting_for_name = State()
    waiting_for_grade = State()


class EditName(StatesGroup):
    waiting_for_new_name = State()


class EditGrade(StatesGroup):
    waiting_for_new_grade = State()


class PMTeacher(StatesGroup):
    subject = State()
    teacher = State()
    text = State()


class ReplyToStudent(StatesGroup):
    text = State()


class AdminStates(StatesGroup):
    waiting_for_poll_question = State()
    waiting_for_poll_options = State()
