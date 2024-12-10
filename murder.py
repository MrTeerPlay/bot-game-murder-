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
    global game_in_progress
    global players2
    global role
    global whrite
    global kill
    global keyboard
    global kill2
    # Очистимо чергу, адже гра розпочалася
    active_players = queue.copy()
    fake_players = [2, 3, 4]
    players2 = active_players + fake_players
    queue = []
    whrite = False
    kill = False
    gameover = False

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
    message_text_1 = "Гра розпочалася, черга очищена!"
    await asyncio.sleep(1)
    for i in range(5, -1, -1):
        message_text_1 = f"Підготуйтеся до гри {i}"
        try:
            # Оновлюємо повідомлення кожну секунду
            await callback_query.message.edit_text(text=message_text_1, reply_markup=None)
            await asyncio.sleep(1)  # Затримка на 1 секунду
        except Exception as e:
            print(f"Не вдалося оновити повідомлення: {e}")

        if i == 0: 
            message_text_1 = "Гра розпочалася!"
            await callback_query.message.edit_text(text=message_text_1, reply_markup=None)
            await asyncio.sleep(1)
    while gameover != True:
        message_text_1 = "Сонце зійшло, все стало яскравим, всі зійшлись"
        await callback_query.message.edit_text(text=message_text_1, reply_markup=None)
        game_in_progress = True
        await asyncio.sleep(1)

    # Цикл for тепер знаходиться всередині циклу while, і він виконується під час кожної ітерації while
        for i in range(10, 0, -1):
            message_text_1 = f"Залишилось {i} секунд"
            try:
            # Оновлюємо повідомлення кожну секунду
                await callback_query.message.edit_text(text=message_text_1, reply_markup=None)
                await asyncio.sleep(1)  # Затримка на 1 секунду
            except Exception as e:
                print(f"Не вдалося оновити повідомлення: {e}")
            if i == 1:
                await asyncio.sleep(1)
                message_text_1 = "Настала ніч, все потемніло, всі розійшлись"
                await callback_query.message.edit_text(text=message_text_1, reply_markup=None)
                game_in_progress = False
                await asyncio.sleep(1)
                for player_id in players2:
                    role = roles.get(player_id)
                    if role == "Мафія":
                        try:
                        # Якщо роль Мафія, то надсилаємо повідомлення з проханням вибрати жертву
                            await bot.send_message(player_id, "Вибери кого вбити", reply_markup=keyboard)
                            if kill2 == True:
                                await callback_query.message.edit_text(f"Вибери предмет для вбивства гравця {player3}", reply_markup=create_item_buttons())
                                item = callback_query.data.split('_')[1]  # Отримуємо вибраний предмет
                                player3 = callback_query.message.text.split()[-1]  # Отримуємо ID гравця, з яким був пов'язаний вибір
                                kill = True
                            else:
                                kill = False
                        # Виводимо повідомлення про вбивство
                        except Exception as e:
                            print(f"Не вдалося відправити повідомлення користувачу {player_id}: {e}")

                            if kill == True:
                                await callback_query.message.edit_text(f"Гравець {player3} був вбитий!")
                                whrite = False
                            else:
                                message_text_1 = "Сьогодні ніхто не помер"
            

#########################################################################################################################################################
async def vote_player(callback_query: CallbackQuery):
    global kill2
    player3 = callback_query.data.split('_')[1]  # Отримуємо ім'я гравця, за якого була натиснута кнопка
    kill2 = True

###################################################################################################################
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

roles = assign_role(players2)
items = assign_item(players2)

###################################################################################################
def create_player_buttons(players2):
    global keyboard
    keyboard = InlineKeyboardMarkup(row_width=2)  # Кількість кнопок у рядку
    for player in players2:
        button = InlineKeyboardButton(text=player, callback_data=f"vote_{player}")
        keyboard.add(button)
    return keyboard

#Заміна кнопок для предметів
def create_item_buttons():
    global keyboard
    keyboard = InlineKeyboardMarkup(row_width=2)  # Кількість кнопок у рядку
    for item in items:
        button = InlineKeyboardButton(text=item, callback_data=f"item_{item}")
        keyboard.add(button)
    return keyboard

#####################################################################################################################
@router.message()
async def handle_private_message(message: Message):
    global players2  # Список гравців, які залишились в грі
    global roles
    global kill
    global game_in_progress
    global whrite

    if game_in_progress == False:
        if whrite == True:
            if roles.get(message.from_user.id) == "Мафія":
                return
        # Видалити повідомлення
        await message.delete()
    else:
        b = 1
            

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
