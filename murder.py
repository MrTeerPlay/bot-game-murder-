import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, BotCommand

bot = Bot(token='8187696469:AAHR8LCtDK6CCh9-vDpNDOAuFa3p98hPxmU')

dp = Dispatcher(bot=bot)
router = Router()
dp.include_router(router)

async def set_bot_commands():
    commands = [
        BotCommand(command="startgame", description="Почати гру"),
        BotCommand(command="test", description="тест, чи працює бот (легкий)"),
    ]
    await bot.set_my_commands(commands)

@router.message(Command("test"))
async def send_test(message: Message):
    await message.answer("successful")

@router.message(Command("help"))
async def send_help(message: Message):
    commands = await bot.get_my_commands()
    for commands in commands:
        await message.answer("/" + commands.command + " - " + commands.description)

@router.message(Command("startgame"))
async def send_game(message: Message):
    button = InlineKeyboardButton(text="Приєднатися", callback_data="callback_data")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
    await message.answer("Кімната вже запущена, приєднуйся до гри!!!", reply_markup=keyboard)

@router.callback_query(lambda callback_query: callback_query.data == "callback_data")
async def callback(query: CallbackQuery):
    await query.answer("")

async def main():
    await set_bot_commands()
    await dp.start_polling(bot)

asyncio.run(main())
