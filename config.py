import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WORDS_FILE = os.getenv("WORDS_FILE", "data/words.json")
DB_FILE = os.getenv("DB_FILE", "data/bot.db")
# Время рассылки в формате "HH:MM"
SCHEDULE_TIME = os.getenv("SCHEDULE_TIME", "21:55")
# Количество слов в день
WORDS_COUNT = int(os.getenv("WORDS_COUNT", "1"))
