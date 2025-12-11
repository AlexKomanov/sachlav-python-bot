from google import genai
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.methods import DeleteWebhook
from aiogram.types import Message

api_key = "AIzaSyDsajaQzNUeY1tnEdm2jIaYbW84rNlSs34" # API плюч Gemini
model = "gemini-2.5-flash" # Модель Gemini
system_instruction = "You are a Python programmer bot. Help the user with Python code."

client = genai.Client(api_key=api_key)

TOKEN = '8508851859:AAHPEeJEp0WUAeodaX40FOJnT7JUQakVwy0' # ⁡⁢⁡⁢⁣⁣ПОМЕНЯЙТЕ ТОКЕН БОТА НА ВАШ⁡

logging.basicConfig(level=logging.INFO)
bot = Bot(TOKEN)
dp = Dispatcher()

# ⁡⁢⁣⁡⁢⁣⁣ОБРАБОТЧИК КОМАНДЫ СТАРТ⁡⁡
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer('Привет! Я бот с подключенной нейросетью, отправь свой запрос', parse_mode = 'HTML')
    
    

# ⁡⁢⁣⁣ОБРАБОТЧИК ЛЮБОГО ТЕКСТОВОГО СООБЩЕНИЯ⁡
@dp.message(lambda message: message.text)
async def filter_messages(message: Message):
    response = client.models.generate_content(
        model=model,
        contents=message.text,
        config=genai.types.GenerateContentConfig(
            system_instruction=system_instruction
        )
    )
    await message.answer(response.text, parse_mode="Markdown")

async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())