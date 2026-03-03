import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

API_TOKEN = "8249519106:AAG4BNI6hhm38RD45ICpWa97FwF-GklW6CI"

DB_NAME = os.path.join(BASE_DIR, "data", "users.db")

ADMIN_IDS = [111111111, 111111111]

TEACHERS = {
    "📘 Українська мова": {
        "XXXXX XXXXXX": 111111111,
        "XXXXXXXX XXXX": 222222222
    },
    "📗 Математика": {
        "XXXXXX XXXXXXXX": 333333333
    },
    "📙 Англійська мова": {
        "XXXX XXXXXXXXXXXXXX": 444444444
    },
    "📕 Історія": {
        "XXX XXXXXX ": 5080156881
    }
}

GRADES = [
    "5","5-А","5-Б","5-В",
    "6","6-А","6-Б","6-В",
    "7","7-А","7-Б","7-В",
    "8","8-А","8-Б","8-В",
    "9","9-А","9-Б","9-В",
    "10","10-А","10-Б","10-В",
    "11","11-А","11-Б","11-В",
]
