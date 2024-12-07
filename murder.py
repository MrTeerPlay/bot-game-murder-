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

@router.message(Command("startgame"))
async def send_game(message: Message):
    global queue_active
    global current_message_text
    global message_text
    button = InlineKeyboardButton(text="", callback_data="")
    current_active_or_inactive()
    if  queue_active==True:
        message_text = f"Кількість гравців: {len(queue)}"
    else:
        message_text = f"Кімната вже готова, приєднуйся до гри!!!"
    await message.answer(message_text, reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Приєднатися", callback_data="join_queue")]]))

def current_active_or_inactive():
    if queue_active==True:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Вийти", callback_data="leave_queue")]])
    
    else:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Приєднатися", callback_data="join_queue")]])


@router.callback_query(lambda c: c.data in ['join_queue', 'leave_queue'])
async def process_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    global queue_active
    global queue
    global message_text
    global current_message_text

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

    if callback_query.data == "join_queue":
        current_message_text = f"Кількість гравців: {len(queue)}"
    else:
        current_message_text = f"Кімната вже готова, приєднуйся до гри!!!"

    await callback_query.message.edit_text(text=current_message_text, reply_markup=current_active_or_inactive())

async def main():
    await set_bot_commands()
    await dp.start_polling(bot)

asyncio.run(main())
