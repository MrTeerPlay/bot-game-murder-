import asyncio
import random
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, BotCommand # type: ignore
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


bot = Bot(token='8187696469:AAHR8LCtDK6CCh9-vDpNDOAuFa3p98hPxmU')

dp = Dispatcher(bot=bot)
router = Router()
dp.include_router(router)
################################################################################################
async def set_bot_commands():
    commands = [
        BotCommand(command="startgame", description="Почати гру"),
        BotCommand(command="test", description="тест, чи працює бот (легкий)"),
    ]
    await bot.set_my_commands(commands)
#######################################################################################
@router.message(Command("test"))
async def send_test(message: Message):
    await message.answer("successful")
#########################################################
@router.message(Command("help"))
async def send_help(message: Message):
    commands = await bot.get_my_commands()
    for commands in commands:
        await message.answer("/" + commands.command + " - " + commands.description)

##################################################################################################################################################
#####################################################################################################
queue = []
queue_active = False
active_players = []
roles = {}
items = {}
game_in_progress = False  # Змінна, яка вказує, чи можна писати
################################################################################################################################
@router.message(Command("startgame"))
async def send_game(message: Message):
    global queue_active
    global current_message_text
    button = InlineKeyboardButton(text="", callback_data="")
    current_active_or_inactive()
    if  queue_active==True:
        message_text = f"Кількість гравців: {len(queue)}"
    else:
        message_text = f"Кімната вже готова, приєднуйся до гри!!!"
    await message.answer(message_text, reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Приєднатися", callback_data="join_queue")]]))
###########################################################################################################################
def current_active_or_inactive():
    buttons = []
    if len(queue) > 0:  # Якщо у черзі є хоча б один гравець
        buttons.append(InlineKeyboardButton(text="Почати гру", callback_data="start_game"))

    if queue_active:  # Черга активна
        buttons.append(InlineKeyboardButton(text="Вийти", callback_data="leave_queue"))
    else:  # Черга неактивна
        buttons.append(InlineKeyboardButton(text="Приєднатися", callback_data="join_queue"))
    
    return InlineKeyboardMarkup(inline_keyboard=[buttons])
#############################################################################################################################
@router.callback_query(lambda c: c.data == "start_game")
async def start_game_callback(callback_query: CallbackQuery):
    global queue, active_players, roles, items

    # Очистимо чергу, адже гра розпочалася
    active_players = queue.copy()
    fake_players = [2, 3, 4]
    players2 = active_players + fake_players
    queue = []

    for player_id in players2:
        roles = assign_role(players2)  # Функція для призначення ролей
        items = assign_item(players2)  # Функція для призначення предметів
    
    for player_id in players2:
        try:
            role = roles[player_id]
            item = items[player_id]
            await bot.send_message(player_id, f"Гра розпочалася! Ваша роль: {role}. Ваш предмет: {item}.")
        except Exception as e:
            print(f"Не вдалося відправити повідомлення користувачу {player_id}: {e}")


    # Оновлюємо текст і клавіатуру в повідомленні
    message_text_1 = "Гра розпочалася, черга очищена!"
    await callback_query.message.edit_text(text=message_text_1, reply_markup=None)
######################################################################################
def assign_role(players):
    mafia = random.choice(players)
    detective = random.choice([p for p in players if p != mafia])
    player_roles = {mafia: 'Мафія', detective: 'Детектив'}
    for player in players:
        if player != detective and player != mafia:
            player_roles[player] = 'Виживший'
    return player_roles

# Функція для призначення предметів
def assign_item(players):
    items_list = ["спічки", "мотузка", "ножниці", "молоток"]
    random.shuffle(items_list)
    player_items = {}
    for i, player in enumerate(players):
        player_items[player] = items_list[i]
    return player_items
##############################################################################################
@router.message()
async def restrict_messages(message: Message):
    if not game_in_progress:
        # Видалити повідомлення
        await message.delete()


            

#####################################################################################################################################
@router.callback_query(lambda c: c.data in ['join_queue', 'leave_queue'])
async def process_callback(callback_query: types.CallbackQuery):

    user_id = callback_query.from_user.id
    global queue_active
    global queue
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
##########################################################################################################################################
async def main():
    await set_bot_commands()
    await dp.start_polling(bot)

asyncio.run(main())
