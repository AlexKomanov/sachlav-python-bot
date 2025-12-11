from openai import OpenAI
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.methods import DeleteWebhook
from aiogram.types import Message
from aiohttp import web
import os
from dotenv import load_dotenv

load_dotenv()

PORT = 5000  

api_key = os.getenv("OPENAI_API_KEY")
model = "gpt-5-nano"
system_instruction = "You are a Python programmer bot. Help the user with Python code."

client = OpenAI(api_key=api_key)

TOKEN = os.getenv("BOT_TOKEN") # ⁡⁢⁡⁢⁣⁣ПОМЕНЯЙТЕ ТОКЕН БОТА НА ВАШ⁡

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(TOKEN)
dp = Dispatcher()

# ⁡⁢⁣⁡⁢⁣⁣ОБРАБОТЧИК КОМАНДЫ СТАРТ⁡⁡
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer('Привет! Я бот с подключенной нейросетью, отправь свой запрос', parse_mode = 'HTML')
    
    

# ⁡⁢⁣⁣ОБРАБОТЧИК ЛЮБОГО ТЕКСТОВОГО СООБЩЕНИЯ⁡
@dp.message(lambda message: message.text)
async def filter_messages(message: Message):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": message.text}
        ]
    )
    await message.answer(response.choices[0].message.content, parse_mode="Markdown")

# API
routes = web.RouteTableDef()

@routes.get("/")
async def index(request):
    """Используется для health check"""
    return web.Response(text="OK")

@routes.post(f"/{TOKEN}")
async def handle_webhook_request(request):
    """Обрабатывает webhook из telegram"""

    # Достаем токен
    url = str(request.url)
    index = url.rfind("/")
    token = url[index + 1 :]

    # Проверяем токен
    if token == TOKEN:
        request_data = await request.json()
        update = types.Update(**request_data)
        await dp._process_update(bot=bot, update=update)

        return web.Response(text="OK")
    else:
        return web.Response(status=403)


if __name__ == "__main__":
    logger.info("Сервер заработал ...")

    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, host="0.0.0.0", port=PORT)
