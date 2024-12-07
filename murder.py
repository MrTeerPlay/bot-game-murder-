import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

bot = Bot(token='8187696469:AAHR8LCtDK6CCh9-vDpNDOAuFa3p98hPxmU')

dp = Dispatcher(bot=bot)
router = Router()
dp.include_router(router)

@router.message(Command("test"))
async def send_test(message: Message):
    await message.answer("successful")

@router.message(Command("startgame"))
async def send_game(message: Message):
    button = InlineKeyboardButton(text="Приєднатися", callback_data="callback_data")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
    await message.answer("Кімната вже запущена, приєднуйся до гри!!!", reply_markup=keyboard)

@router.callback_query(lambda callback_query: callback_query.data == "callback_data")
async def callback(query: CallbackQuery):
    await query.answer("")

async def main():
    await dp.start_polling(bot)

asyncio.run(main())
