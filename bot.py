import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import (
    Message,
    WebAppInfo,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("8120362026:AAFQ3Sk-BimJjfT9Qskf7PZgIg56g8UxjIM")  # положи сюда токен в .env
WEBAPP_URL = os.getenv("WEBAPP_URL")  # сюда положи публичный https, например https://xyz.ngrok-free.app/

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text="🎮 Играть в Крестики-Нолики",
                web_app=WebAppInfo(url=WEBAPP_URL)  # открывает наш Flask front
            )
        ]]
    )
    await message.answer(
        "ГЛАВНОЕ МЕНЮ\nВыберите действие:",
        reply_markup=kb
    )

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
