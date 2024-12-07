import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, BotCommand # type: ignore
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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

##################################################################################################################################################
#####################################################################################################
queue = []
queue_active = False

def active_or_inactive():
    if queue_active==True:
        return InlineKeyboardButton(text="Вийти", callback_data="leave_queue")
    else:
        return InlineKeyboardButton(text="Приєднатися", callback_data="join_queue")

@router.message(Command("startgame"))
async def send_game(message: Message):
    button = InlineKeyboardButton(text="Приєднатися", callback_data="callback_data")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[active_or_inactive()]])
    await message.answer("Кімната вже готова, приєднуйся до гри!!!", reply_markup=keyboard)

@router.callback_query(lambda callback_query: callback_query.data == "callback_data")
async def callback(query: CallbackQuery):
    await query.answer("")

@router.callback_query(lambda c: c.data in ['join_queue', 'leave_queue'])
async def process_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    global queue_active

    if callback_query.data == "join_queue":
        if user_id not in queue:
            queue.append(user_id)
            queue_active = True  # Черга стає активною
            await bot.answer_callback_query(callback_query.id, text="Ви приєдналися до черги!")
        else:
            await bot.answer_callback_query(callback_query.id, text="Ви вже в черзі!")
    
    elif callback_query.data == "leave_queue":
        if user_id in queue:
            queue.remove(user_id)
            if not queue:  # Якщо черга порожня, вона більше не активна
                queue_active = False
            await bot.answer_callback_query(callback_query.id, text="Ви вийшли з черги!")
        else:
            await bot.answer_callback_query(callback_query.id, text="Ви не в черзі!")

    # Оновлюємо кнопку
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[active_or_inactive()]])




async def main():
    await set_bot_commands()
    await dp.start_polling(bot)

asyncio.run(main())
