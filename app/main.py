import uvicorn
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base

import asyncio
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import CommandStart

from app import config
from app.db.database import lifespan
from app.api.endpoints import router as product_router
from app.db.utils import CustomScheduler

app = FastAPI(lifespan=lifespan)
app.include_router(product_router)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# Base = declarative_base()


# Telegram Bot
tg_router = Router()
bot: Bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()
dp.include_router(tg_router)


class GetProductData(StatesGroup):
    waiting_for_artikul = State()


@tg_router.message(CommandStart())
async def command_start_handler(message: types.Message,
                                state: FSMContext) -> None:
    await message.answer(
        "Привет! Нажмите кнопку 'Получить данные по товару'",
        reply_markup=types.ReplyKeyboardMarkup(keyboard=[
            [types.KeyboardButton(text="Получить данные по товару")]],
                                               resize_keyboard=True)
    )


@tg_router.message(F.text == "Получить данные по товару")
async def get_product_data(message: types.Message, state: FSMContext):
    await message.answer("Введите артикул товара:")
    await state.set_state(GetProductData.waiting_for_artikul)

@tg_router.message(GetProductData.waiting_for_artikul)
async def process_artikul(message: types.Message, session: AsyncSession = Depends()):
    await message.answer("Некорректный артикул. Введите число.")
    # try:
    #     artikul = int(message.text)
    #     product = await session.get(Product, artikul)
    #     if product:
    #         await message.answer(f"Название: {product.name}\nЦена: {product.price}\nРейтинг: {product.rating}\nКоличество на складах: {product.total_quantity}")
    #     else:
    #         await message.answer("Товар не найден.")
    # except ValueError:
    #     await message.answer("Некорректный артикул. Введите число.")


async def start_bot():
    await dp.start_polling(bot)


async def start_fastapi():
    config = uvicorn.Config(
        app, host="127.0.0.0", port=8080, log_level="debug", reload=True
    )
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    scheduler = CustomScheduler(store_url=config.DATABASE_URL)
    # scheduler.add_job()
    scheduler.start()
    await asyncio.gather(start_bot(), start_fastapi())


if __name__ == "__main__":
    asyncio.run(main())


# sudo docker run  --rm  --name wb_database -p 5416:5432 -e POSTGRES_USER=user -e POSTGRES_PASSWORD=qwerty -e POSTGRES_DB=wb_data -d postgres:14
#  psql -U user -d wb_data -h localhost -p 5416
