import re
import time
from bot_config import ADMIN_IDS, TEACHERS, GRADES



def is_admin(uid):
    return uid in ADMIN_IDS


def is_teacher(uid):
    return any(uid in teachers.values() for teachers in TEACHERS.values())


def get_role(uid):
    if is_admin(uid) and is_teacher(uid):
        return "Вчитель, Адміністратор"
    if is_admin(uid):
        return "Адміністратор"
    if is_teacher(uid):
        return "Вчитель"
    return "Учень"


def normalize_grade(text):
    if text.lower() == "не керую":
        return "не керую"

    text = text.replace(" ", "").replace("–", "-").replace("—", "-").lower()
    match = re.fullmatch(r"(\d{1,2})(?:-?([абв]))?", text)

    if not match:
        return ""

    num, letter = match.groups()
    grade = f"{int(num)}-{letter.upper()}" if letter else str(int(num))

    return grade if grade in GRADES else ""


def is_valid_name(name):
    return 10 <= len(name) <= 24 and name.replace(" ", "").replace("'", "").isalpha()

RATE_LIMITS = {
    "message": 5.0,
    "callback": 100.0,
    "pm": 180.0,
    "vote": 120.0
    }

def is_rate_limited(user_id: int, action: str, _user_actions=None) -> bool:
    now = time.time()
    last = _user_actions[user_id][action]
    if now - last < RATE_LIMITS.get(action, 1.5):
        return True
    _user_actions[user_id][action] = now
    return False