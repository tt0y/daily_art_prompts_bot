from aiogram import Router, types
from aiogram.filters import Command
from services.storage import Storage
from services.word_service import WordService
import config

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, storage: Storage):
    await storage.add_chat(message.chat.id)
    await message.answer(
        "Привет! Я буду присылать тебе темы для рисования каждый день.\n"
        "Просто добавь меня в чат, и я начну работать."
    )

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "Я бот для художников.\n"
        "Каждый день я присылаю случайные слова-ассоциации для рисования.\n"
        "Команды:\n"
        "/start - начать работу (подписаться на рассылку)\n"
        "/help - справка\n"
        "/word - получить случайное слово прямо сейчас"
    )

@router.message(Command("word"))
async def cmd_word(message: types.Message, word_service: WordService):
    words = word_service.get_random_words(1)
    await message.answer(
        f"🎲 Ваше случайное слово:\n\n✨ <b>{words[0].upper()}</b> ✨",
        parse_mode="HTML"
    )

@router.message(Command("about"))
async def cmd_about(message: types.Message, word_service: WordService):
    total_words = word_service.get_total_count()
    await message.answer(
        f"ℹ️ <b>О боте</b>\n\n"
        f"🕒 Время рассылки: <b>{config.SCHEDULE_TIME}</b>\n"
        f"📝 Слов в рассылке: <b>{config.WORDS_COUNT}</b>\n"
        f"📚 Слов в базе: <b>{total_words}</b>",
        parse_mode="HTML"
    )
