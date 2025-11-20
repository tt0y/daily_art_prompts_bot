import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

import config
from services.storage import Storage
from services.word_service import WordService
from handlers import common

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def send_daily_words(bot: Bot, storage: Storage, word_service: WordService):
    chats = await storage.get_all_chats()
    if not chats:
        logger.info("Нет активных чатов для рассылки.")
        return

    words = word_service.get_random_words(config.WORDS_COUNT)
    
    # Формируем список слов
    words_list = "\n".join([f"✨ <b>{word.upper()}</b> ✨" for word in words])
    message_text = f"🎲 Ваше случайное слово на сегодня:\n\n{words_list}"

    for chat_id in chats:
        try:
            await bot.send_message(chat_id, message_text, parse_mode="HTML")
        except Exception as e:
            logger.error(f"Не удалось отправить сообщение в чат {chat_id}: {e}")
            # Можно добавить логику удаления чата, если бот заблокирован

async def main():
    # Инициализация сервисов
    storage = Storage(config.DB_FILE)
    await storage.init_db()
    
    word_service = WordService(config.WORDS_FILE)
    
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()

    # Регистрация хендлеров
    # Передаем storage в хендлеры через middleware или dependency injection (в aiogram 3 это workflow_data)
    dp.include_router(common.router)

    # Настройка шедулера
    scheduler = AsyncIOScheduler()
    
    # Парсим время из конфига (HH:MM)
    hour, minute = map(int, config.SCHEDULE_TIME.split(':'))
    
    scheduler.add_job(
        send_daily_words,
        CronTrigger(hour=hour, minute=minute),
        kwargs={"bot": bot, "storage": storage, "word_service": word_service}
    )
    
    scheduler.start()
    logger.info(f"Бот запущен. Рассылка запланирована на {config.SCHEDULE_TIME}")

    # Регистрация команд в меню
    await bot.set_my_commands([
        types.BotCommand(command="start", description="Начать работу"),
        types.BotCommand(command="help", description="Справка"),
        types.BotCommand(command="word", description="Случайное слово"),
        types.BotCommand(command="about", description="О боте"),
    ])

    # Запуск поллинга
    # Передаем storage в workflow_data, чтобы он был доступен в хендлерах
    await dp.start_polling(bot, storage=storage, word_service=word_service)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен")
