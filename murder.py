import asyncio
import random
from asyncio import TimeoutError
from asyncio import wait_for
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, BotCommand, User
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramRetryAfter

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
###################################################################################################################

async def safe_edit_message(message, text, reply_markup=None):
    while True:
        try:
            await message.edit_text(text=text, reply_markup=reply_markup)
            break  # Якщо успішно, виходимо з циклу
        except TelegramRetryAfter as e:
           print(f"Перевищено ліміт, очікуємо {e.retry_after} секунд...")
           await asyncio.sleep(e.retry_after)  # Очікуємо час, вказаний у помилці
        except Exception as ex:
            print(f"Інша помилка: {ex}")
            break  # Виходимо, якщо це не помилка TelegramRetryAfter

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
    global keyboard2
    global mafia_players
    global item_keyboard
    global callback_queue

    # Очистимо чергу, адже гра розпочалася
    active_players = queue.copy()
    fake_players = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    queue = []
    whrite = False
    kill = False
    gameover = False
    players2 = active_players + fake_players
    callback_queue = asyncio.Queue()

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
    gameover_players = len(players2) - mafia_players
    message_text_1 = "Гра розпочалася, черга очищена!"
    await asyncio.sleep(1)
    
    for i in range(5, -1, -1):
        message_text_1 = f"Підготуйтеся до гри {i}"
        try:
            # Оновлюємо повідомлення кожну секунду
 #           await callback_query.message.edit_text(text=message_text_1, reply_markup=None)
            await asyncio.sleep(1)  # Затримка на 1 секунду
        except Exception as e:
            print(f"Не вдалося оновити повідомлення: {e}")

        if i == 0: 
            message_text_1 = "Гра розпочалася!"
  #          await callback_query.message.edit_text(text=message_text_1, reply_markup=None)
            await asyncio.sleep(1)
            message_text_1 = "Сонце зійшло, все стало яскравим, всі зійшлись"
   #         await callback_query.message.edit_text(text=message_text_1, reply_markup=None)
    while gameover != True:
        game_in_progress = True
        await asyncio.sleep(1)
        for i in range(2, 0, -1):
 #           message_text_1 = f"Залишилось {i} секунд"
  #          await callback_query.message.edit_text(text=message_text_1, reply_markup=None)
            await asyncio.sleep(1)  # Затримка на 1 секунду
        message_text_1 = "Настала ніч, все потемніло, всі розійшлись"
        await callback_query.message.edit_text(text=message_text_1, reply_markup=None)
        game_in_progress = False
        await asyncio.sleep(1)
        for player_id in players2:
                    if role == 'Мафія':
                        try:
                        # Якщо роль Мафія, то надсилаємо повідомлення з проханням вибрати жертву
                            mafia_players = [player_id for player_id, role in roles.items() if role == "Мафія"]
                            keyboard2 = create_player_buttons(players2, mafia_players)
                            await bot.send_message(player_id, "Виберіть кого вбити", reply_markup=keyboard2)
                            kill_callback = await wait_for_callback_query(bot, player_id, timeout=20)  # Очікування вибору (макс. 60 секунд)
                            if kill_callback.data.startswith("kill_"):
                                selected_victim = kill_callback.data.split('_')[1]  # Отримуємо ID вибраного гравця
                                await kill_callback.answer(f"Ви вибрали {selected_victim} як жертву.")
                                # Замінюємо кнопки на вибір предмету
                                item_keyboard = create_item_buttons()
                                await bot.send_message(player_id, f"Виберіть предмет для вбивства {selected_victim}", reply_markup=item_keyboard)
                                # Очікуємо вибору предмету
                                item_callback = await wait_for_callback_query(bot, player_id, timeout=20)
                                if item_callback.data.startswith("item_"):
                                    selected_item = item_callback.data.split('_')[1]  # Отримуємо вибраний предмет
                                    await item_callback.answer(f"Ви вибрали {selected_item} для вбивства {selected_victim}.")
                                    await bot.send_message(player_id, f"Ви вбили {selected_victim} за допомогою {selected_item}.")
                                    players2.remove(selected_victim)  # Видаляємо жертву з гри
                                    kill = True
                            else:
                                await bot.send_message(player_id, "Ви не вибрали жертву")
                        except Exception as e:
                            print(f"Не вдалося відправити повідомлення користувачу {player_id}: {e}")
                # Виводимо повідомлення про вбивство
        if kill == True:
                    await callback_query.message.edit_text(f"Сонце зійшло, все стало яскравим, всі зійшлись. \nГравець {selected_victim} був вбитий!", reply_markup=None)
                    whrite = False
                    await asyncio.sleep(1)
        else:
                    message_text_1 = ("Сонце зійшло, все стало яскравим, всі зійшлись. \nСьогодні ніхто не помер")
                    await callback_query.message.edit_text(text=message_text_1, reply_markup=None)
                    await asyncio.sleep(1)

###################################################################################################################
def assign_role(players):
    global mafia_players
    player_roles = {}

    if 4 <= len(players2) <= 6:
        num_mafia = 1
        num_detectives = 1
    elif 7 <= len(players2) <= 10:
        num_mafia = 2
        num_detectives = 2
    else:
        num_mafia = max(1, len(players2) // 3)
        num_detectives = max(1, len(players2) // 3)
    mafia = random.sample(players2, num_mafia)

#deldeldeldeldeldeldeldeldeldeldeldeldeldeldel
    for player in active_players:
            mafia.append(player)

#deldeldeldeldeldeldeldeldeldeldeldeldeldeldel

    detectives = random.sample([p for p in players2 if p not in mafia], num_detectives)
    for player in players:
        for player in mafia:
            player_roles[player] = 'Мафія'
        for player in detectives:
            player_roles[player] = 'Детектив'
        if player not in mafia and player not in detectives:
            player_roles[player] = 'Виживший'
    mafia_players = len(mafia)
    return player_roles

# Функція для призначення предметів
def assign_item(players):
    global players2
    items_list = ["спічки", "мотузка", "ножниці", "молоток"]

    if len(players) > len(items_list):
        # Повторюємо предмети стільки разів, скільки потрібно, щоб покрити всіх гравців
        items_list = items_list * (len(players) // len(items_list)) + items_list[:len(players) % len(items_list)]

    random.shuffle(items_list)
    player_items = {}
    for i, player in enumerate(players):
        player_items[player] = items_list[i]
    return player_items
##################################################################################################################################

async def wait_for_callback_query(user_id, timeout=20):
    global callback_queue
    try:
        # Очікуємо відповідний callback-запит
        callback_query = await asyncio.wait_for(callback_queue.get(), timeout=timeout)
        if callback_query.from_user.id == user_id:  # Перевіряємо, чи це потрібний користувач
            return callback_query
    except asyncio.TimeoutError:
        return None  # Тайм-аут

######################################################################################################################
def create_player_buttons(players2, mafia_players):
    target_players = [str(player) for player in players2 if player not in mafia_players]
    buttons = [[InlineKeyboardButton(text=player, callback_data=f"kill_{player}")] for player in target_players]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

#Заміна кнопок для предметів
def create_item_buttons():
    global item_keyboard
    item_keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])
    buttons = [InlineKeyboardButton(text=item, callback_data=f"item_{item}") for item in items]
    item_keyboard.add(*buttons)  # Додаємо всі кнопки
    return item_keyboard
#############################################################################################################################

@router.callback_query()
async def handle_any_callback_query(callback_query: CallbackQuery):
    global callback_queue
    await callback_queue.put(callback_query)

#################################################################################################################
@router.callback_query(lambda c: c.data.startswith("kill_"))
async def handle_kill_callback(callback_query: CallbackQuery):
    global selected_victim

    try:
        # Очікуємо вибір гравця
        kill_callback = await asyncio.wait_for(callback_queue.get(), timeout=20)
        if kill_callback.data.startswith("kill_"):
            selected_victim = kill_callback.data.split('_')[1]
            await callback_query.answer(f"Ви вибрали {selected_victim} як жертву.")
        else:
            await callback_query.answer("Час вийшов, ви не вибрали жертву.")
    except asyncio.TimeoutError:
        await callback_query.answer("Тайм-аут. Ви не зробили вибір.")
  # Отримуємо ім'я гравця після "kill_"
################################################################################################################################

@router.callback_query(lambda c: c.data.startswith("item_"))
async def item_selection_callback(callback_query: CallbackQuery):
    global selected_victim
    # Отримуємо назву вибраного предмета
    selected_item = callback_query.data.split('_')[1]  # Отримуємо назву предмету

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
