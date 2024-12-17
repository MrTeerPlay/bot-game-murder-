import asyncio
import random
import time
import logging
from asyncio import wait_for
from aiogram.exceptions import TelegramRetryAfter
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.context import FSMContext
from asyncio import TimeoutError
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, BotCommand, User 
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramRetryAfter
from collections import Counter
from collections import defaultdict

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
#########################################################################################################
def create_vote_buttons(players2):
    vote_counts = {}
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"Голосувати за {player}", callback_data=f"vote_{player}")] for player in players2
    ])
    return keyboard
#######################################################################################################
if 'message_text_current' not in locals():
    message_text_current = " "

vote_counts = defaultdict(int)
################################################################################################
#async def process_votes():
    #global votes
    #global message4
    #global most_voted_players
    #global max_votes
    #global message5

    #vote_count = {player_id: 0 for player_id in players2}
    # Підраховуємо кількість голосів за кожного гравця
    #for vote in votes.values():
        #if vote in vote_count:
            #vote_count[vote] += 1
        #else:
            #vote_count[vote] = 1

    # Знаходимо гравця з найбільшим числом голосів
    #for player_voted in votes.values():  # votes містить ID гравців, за яких проголосували
        #if player_voted in vote_count:
            #vote_count[player_voted] += 1

    #most_voted_players = []
    #max_votes = 0

    #for player_id in vote_count:
        #if vote_count[player_id] > max_votes:
                    #most_voted_players = [player_id]  # Скидаємо список і додаємо нового лідера
                    #max_votes = vote_count[player_id]
        #elif vote_count[player_id] == max_votes:
                    #most_voted_players.append(player_id)
    
    # Виводимо результати голосування в груповому чаті

        #message4 = (f"Голосування завершено! Гравець {most_voted_players} отримав {max_votes} голосів.")

        #message5 = (f"Голосування завершено! Нікого не було страчено")
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
#@router.message(Command["end_vote"])
global_message = None
async def end_vote(global_message):
    global continue5
    global vote_counts
    global eliminated_player
    global players_with_max_votes
    if not vote_counts:
        return
    players_with_max_votes = get_players_with_max_votes(vote_counts)
    print(f"players_with_max_votes: {players_with_max_votes}")
    eliminated_player = int(players_with_max_votes[0])
    if not vote_counts:  # Якщо ніхто не голосував
        await global_message.edit_text("Ніхто ні за кого не проголосував!")
        return  # Завершуємо голосування, гра продовжується
    else:
        await bot.send_message(players2[0], f"Гравець, якого виключено: {eliminated_player}")
    if eliminated_player in players2:
        players2.remove(eliminated_player)
    #else:
        #await bot.send_message(players2[0], "Не вдалося визначити гравця для виключення.")

    # Очікуємо, поки `continue5` стане True
    #while not continue5:
        #await asyncio.sleep(0.1)  # Уникаємо блокування асинхронного циклу

    #if not votes:
    #if not vote_counts:
        #await message.answer("Голосування завершене. Ніхто не проголосував. Гра продовжується.")
        #return

    # Підрахунок голосів
    #max_votes = max(votes.values(), default=0)
    #players_with_max_votes = [player for player, count in vote_counts.items() if count == max_votes]
    # Обробка результатів голосування
    #if max_votes == 0 or len(players_with_max_votes) > 1:
    #if len(players_with_max_votes) > 1:
        #await bot.send_message(players2[0],"Голосування завершене. Результат не визначений. Гра продовжується.")
    # Вилучаємо гравця з найбільшою кількістю голосів
    #else:    
        #eliminated_player = players_with_max_votes[0]
    #if eliminated_player in players2:
    
        #await message.answer(f"Гравець {eliminated_player} отримав найбільше голосів і вилучається з гри.")
        #await message.answer(f"Залишилися гравці: {', '.join(map(str, players2))}")
#####################################################################################################
queue = []
queue_active = False
active_players = []
roles = {}
items = {}
game_in_progress = False  # Змінна, яка вказує, чи можна писати
###################################################################################################################

#async def safe_edit_message(message, text, reply_markup=None):
    #global message_text_current
   # global current_message
    #while True:
      #  try:
      #      if text != message_text_current or current_message.reply_markup is None:
      #          await message.edit_text(text=text, reply_markup=reply_markup)
      #      break  # Якщо успішно, виходимо з циклу
     #   except TelegramRetryAfter as e:
     #      print(f"Перевищено ліміт, очікуємо {e.retry_after} секунд...")
     #      await asyncio.sleep(e.retry_after)  # Очікуємо час, вказаний у помилці
     #   except Exception as ex:
      #      print(f"Інша помилка: {ex}")
#      break  # Виходимо, якщо це не помилка TelegramRetryAfter

################################################################################################################################
@router.message(Command("startgame"))
async def send_game(message: Message):
    global queue_active
    button = InlineKeyboardButton(text="", callback_data="")
    if queue_active==True:
        message_text = f"Кількість гравців: {len(queue)}"
    else:
        message_text = f"Кімната вже готова, приєднуйся до гри!!!"
    await message.answer(message_text, reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Приєднатися", callback_data="join_queue")]]))
    current_active_or_inactive()
###########################################################################################################################
def current_active_or_inactive():
    buttons = []
    if len(queue) > 0:  # Якщо у черзі є хоча б один гравець
        buttons.append(InlineKeyboardButton(text="Почати гру", callback_data="start_game"))

    if queue_active:  # Черга активна
        buttons.append(InlineKeyboardButton(text="Вийти", callback_data="leave_queue"))
    #else:  # Черга неактивна
        #buttons.append(InlineKeyboardButton(text="Приєднатися", callback_data="join_queue"))
    
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
    global message_text_current
    global current_message
    global startkill
    global continue1
    global vote_timer
    global contiune2
    global votes
    global players_voted
    global players_with_max_votes

    # Очистимо чергу, адже гра розпочалася
    active_players = queue.copy()
    fake_players = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    queue = []
    whrite = False
    kill = False
    gameover = False
    players2 = active_players + fake_players
    current_message = callback_query.message
    message_text_current = current_message.text
    startkill = False
    game_two = False
    contiune2 = False
    round_one = True

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
    message_text_1 = f"Підготуйтеся до гри!"
    await asyncio.sleep(3)
    try:
        # Оновлюємо повідомлення кожну секунду
        if message_text_1 != message_text_current or current_message.reply_markup is None:
            await callback_query.message.edit_text(text=message_text_1, reply_markup=None)
        #await callback_query.message.edit_text(text=message_text_1, reply_markup=None)
        await asyncio.sleep(1)  # Затримка на 1 секунду
    except Exception as e:
        print(f"Не вдалося оновити повідомлення: {e}")
    message_text_1 = "Гра розпочалася!"
    if message_text_1 != message_text_current or current_message.reply_markup is None:
            await callback_query.message.edit_text(text=message_text_1, reply_markup=None)
    #await callback_query.message.edit_text(text=message_text_1, reply_markup=None)
    await asyncio.sleep(2)
    message_text_1 = "Сонце зійшло, все стало яскравим, всі зійшлись"
    if message_text_1 != message_text_current or current_message.reply_markup is None:
            await callback_query.message.edit_text(text=message_text_1, reply_markup=None)
    #await callback_query.message.edit_text(text=message_text_1, reply_markup=None)
    while gameover != True:
        startkill = True
        continue1 = False
        vote_timer = None
        game_in_progress = True
        if game_two == True:
            if round_one == False:
                if vote_counts:
                    players2 = [player for player in players2 if player != eliminated_player]
                    votes.clear()
                    players_voted.clear()
                    vote_counts.clear()  # Очистка голосів
                    players_with_max_votes.clear() 
                    for player in players2:
            # Збираємо голоси для кожного гравця
                        pass
            vote_keyboard = create_vote_buttons(players2)
            message_text_1 = "Голосуйте за того, кого хочете стратити"
            if message_text_1 != message_text_current or current_message.reply_markup is None:
                await callback_query.message.edit_text(text=message_text_1, reply_markup=vote_keyboard)
        vote_timer = await wait_for_vote(timeout=20)
        contiune2 = True
        await end_vote(global_message)
        if not vote_counts:  # Якщо ніхто не голосував
            message_text_1 = "Ніхто ні за кого не проголосував!"
            if message_text_1 != message_text_current or current_message.reply_markup is None:
                await callback_query.message.edit_text(text=message_text_1, reply_markup=None)
                await asyncio.sleep(2)
        #if vote_timer is None:
            #if max_votes == 0:
                #if message5 != message_text_current or current_message.reply_markup is None:
                    #await callback_query.message.edit_text(text=message5, reply_markup=None)
            #else:
            #if message4 != message_text_current or current_message.reply_markup is None:
                #await callback_query.message.edit_text(text=message4, reply_markup=None)
        await asyncio.sleep(5)
        for i in range(5, 0, -1):
                message_text_1 = f"Залишилось {i} секунд"
                if message_text_1 != message_text_current or current_message.reply_markup is None:
                    await callback_query.message.edit_text(text=message_text_1, reply_markup=None)
            #await callback_query.message.edit_text(text=message_text_1, reply_markup=None)
                await asyncio.sleep(1)  # Затримка на 1 секунду
        message_text_1 = "Настала ніч, все потемніло, всі розійшлись"
        if message_text_1 != message_text_current or current_message.reply_markup is None:
                await callback_query.message.edit_text(text=message_text_1, reply_markup=None)
        game_in_progress = False
            #mafia_players1 = [player_id for player_id, role in roles.items() if role == "Мафія"]
        await asyncio.sleep(1.5)
        for player_id in players2:
                if player_id in roles and roles[player_id] == 'Мафія':
                    try:
                        # Якщо роль Мафія, то надсилаємо повідомлення з проханням вибрати жертву
                        keyboard2 = create_player_buttons(players2, mafia_players)
                        await bot.send_message(player_id, "Виберіть кого вбити", reply_markup=keyboard2)
                        #player_timer = 
                        await wait_for_victim_selection(player_id, timeout=20)
                        # Якщо час вичерпано, інформуємо користувача
                        #await bot.send_message(player_id, "Час на вибір предмета вичерпано!")

            # Після вибору жертви надаємо вибір предмета
                        #item_keyboard = create_item_buttons(["спічки", "мотузка", "ножниці", "молоток"])
                        #await bot.send_message(player_id, f"Виберіть предмет для вбивства {selected_player}", reply_markup=item_keyboard)
            
            # Очікуємо вибір предмета
                        #selected_item = await wait_for_item_selection(player_id)
                        #player_items[player_id] = selected_item
                    except Exception as e:
                        print(f"Не вдалося відправити повідомлення користувачу {player_id}: {e}")
        if continue1 == True:
                # Виводимо повідомлення про вбивство
                if kill == True:
                    startkill = False
                    if message_text_1 != message_text_current or current_message.reply_markup is None:
                        await callback_query.message.edit_text(f"Сонце зійшло, все стало яскравим, всі зійшлись. \nГравець {selected_player} був вбитий!", reply_markup=None)
                    whrite = False
                    await asyncio.sleep(0)
                else:
                        message_text_1 = ("Сонце зійшло, все стало яскравим, всі зійшлись. \nСьогодні ніхто не помер")
                        if message_text_1 != message_text_current or current_message.reply_markup is None:
                            await callback_query.message.edit_text(text=message_text_1, reply_markup=None)
                        #await callback_query.message.edit_text(text=message_text_1, reply_markup=None)
                        await asyncio.sleep(0)
        game_two = True
        round_one = False

player_victims = {}
######################################################################################################################################################

async def wait_for_victim_selection(player_id: int, timeout: int):
    victim_selected = False
    selected_player = None
    await asyncio.sleep(timeout)
    if player_id not in player_victims:
        # Якщо жертва не була вибрана, відправляємо повідомлення
        player_victims[player_id] = None
        print(f"Час для вибору жертви вичерпано для {player_id}")
    else:
        print(f"Гравець {player_id} вибрав жертву: {player_victims[player_id]}")
    return selected_player
    # Очікуємо вибір жертви
    #while player_id not in player_victims:
        #await asyncio.sleep(1)
    #return player_victims.get(player_id)

###################################################################################################################

async def wait_for_vote(timeout: int):
    global continue5
    continue5 = False
    await asyncio.sleep(timeout)
    continue5 = True


##################################################################################################################
def assign_role(players):
    global mafia_players
    global mafia
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

def create_player_buttons(players2, mafia_players):

    if not isinstance(mafia_players, list):
        mafia_players = [mafia_players]

    target_players = [str(player) for player in players2 if player not in mafia]
    print("target_players:", target_players)  # Додайте логування

    if not target_players:
        return None  # Повертаємо None замість порожньої клавіатури

    buttons = [[InlineKeyboardButton(text=player, callback_data=f"kill_{player}")] for player in target_players]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Функція для призначення предметів
def assign_item(players2):
    global player_items
    global items_list
    global mafia
    global mafia_player
    global mafia_items
    items_list = ["спічки", "провод", "ножниці", "бутилка води", "акамулятор", "електрошокер", "розбите дзеркало", "наскрізна труба", "коняча доза снодійного", "ліхтар"]

    if len(players2) > len(items_list):
        # Повторюємо предмети стільки разів, скільки потрібно, щоб покрити всіх гравців
        items_list = items_list * (len(players2) // len(items_list)) + items_list[:len(players2) % len(items_list)]

    random.shuffle(items_list)

    player_items = {}
    mafia_items = random.sample(items_list, len(mafia))
    #items_list = items_list[len(mafia):]  # Залишок предметів для інших гравців
    for i, mafia_player in enumerate(mafia):
        player_items[mafia_player] = mafia_items[i]

    remaining_items = [item for item in items_list if item not in mafia_items]
    other_players = [player for player in players2 if player not in mafia]
    if len(remaining_items) < len(other_players):
        # Призначаємо предмети за кількістю гравців
        remaining_items = (remaining_items * ((len(other_players) // len(remaining_items)) + 1))[:len(other_players)]
    # Розподіл предметів серед інших гравців
    other_players = [player for player in players2 if player not in mafia]
    for i, other_player in enumerate(other_players):
        player_items[other_player] = remaining_items[i]

    return player_items

#Заміна кнопок для предметів

##########################################################################################################
is_item_selected = False
continue1 = False
#################################################################################################################
selected_player = None
selected_player_str = str(selected_player)
#####################################################################################################################
@router.callback_query(lambda c: c.data.startswith("kill_"))
async def kill_player_callback(callback_query: CallbackQuery):
    global players2
    global user_item_selection
    global continue1
    global selected_player
    global player_victims
    global player_items
    global items_list
    # Отримуємо ID жертви
    #if startkill == True:
    try:
            #await asyncio.wait_for(wait_for_victim_selection(callback_query.from_user.id, timeout=20), timeout=20)
        # Зберігаємо вибір жертви
                selected_player = int(callback_query.data.split("kill_")[1])
                selected_player_str = str(selected_player)
                #await bot.answer_callback_query(callback_query.from_user.id, f"Ви вибрали гравця {selected_player}")
        
        # Створюємо клавіатуру для вибору предмету
                item_keyboard = create_item_buttons(callback_query.from_user.id)  # Викликаємо функцію для створення клавіатури з предметами
                await bot.send_message(callback_query.from_user.id, f"Виберіть предмет для вбивства {selected_player_str}", reply_markup=item_keyboard)

                #await bot.send_message(callback_query.from_user.id, "Ця жертва вже не доступна для вбивства!")
    except asyncio.TimeoutError:
            # Якщо час вичерпано, інформуємо користувача
            await bot.send_message(callback_query.from_user.id, "Час на вибір предмета вичерпано!")
    continue1 = True

def create_item_buttons(player_id):
    available_items = list(mafia_items)    #get_available_items_for_player(player_id)
    print("available_items:", available_items)
    if not isinstance(available_items, list):
        print("Error: available_items is not a list")
        return None  # Якщо це не список, повертаємо None
    if not available_items: 
        return None  # Повертаємо None, якщо список порожній
    buttons = [InlineKeyboardButton(text=str(item), callback_data=f"item_{item}_{selected_player}") for item in available_items]
    print (available_items)
    return InlineKeyboardMarkup(inline_keyboard=[buttons])

@router.callback_query(lambda c: c.data.startswith("item_"))
async def item_selection_callback(callback_query: CallbackQuery):
    global selected_player, players2
    global user_item_selection
    global kill
    
    # Отримуємо вибраний предмет
    selected_item = callback_query.data.split('_')[1]

    # Повідомляємо гравцю про вбивство
    await bot.send_message(callback_query.from_user.id, f"Ви вбили {selected_player} за допомогою {selected_item}.")
    user_item_selection[callback_query.from_user.id] = True
    kill = True
    # Видаляємо жертву з гри
    players2.remove(selected_player)
    
    # Можливо потрібно запитати, чи хоче він вибрати іншу жертву або чи буде продовження гри
    await bot.send_message(callback_query.from_user.id, "Гра триває, виберіть іншу жертву або дійте за іншим планом.")

user_item_selection = {}
##########################################################################################################
async def wait_for_item_selection(user_id: int):
    # Ініціалізація стану вибору для конкретного користувача
    user_item_selection[user_id] = False

    # Чекаємо, поки вибір не буде зроблений
    while not user_item_selection[user_id]:
        await asyncio.sleep(1)  # Перевірка кожну секунду
#####################################################################################################################
@router.message()
async def handle_private_message(message: Message):
    global players2  # Список гравців, які залишились в грі
    global roles
    global kill
    global game_in_progress
    #global whrite

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
    global message_text_current
    global current_message

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
        current_message_text1 = f"Кількість гравців: {len(queue)}"
    else:
        current_message_text1 = f"Кімната вже готова, приєднуйся до гри!!!"

    if current_message_text1 != message_text_current or current_message.reply_markup is None:
        await callback_query.message.edit_text(text=current_message_text1, reply_markup=current_active_or_inactive())
    #await callback_query.message.edit_text(text=current_message_text1, reply_markup=current_active_or_inactive())
##########################################################################################################################################
#votes = {}
votes = Counter()
players_voted = set()
vote_counts = Counter()
selected_player1 = None
@router.callback_query(lambda callback: callback.data.startswith("vote_"))
async def vote_callback(callback: types.CallbackQuery):
    #global vote_player
    global selected_player1
    global votes, players_voted
    global vote_counts
    #player_voted = callback_query.from_user.id  # ID користувача, який натиснув кнопку
    #vote_player = callback_query.data.split("vote_")[1]  # Гравець, за якого проголосували
    #selected_player1 = callback.data.split("vote_")[1]
    selected_player1 = int(callback.data.split("vote_")[1])

    if callback.from_user.id in players_voted:
        # Якщо користувач вже голосував, відправляємо повідомлення і не дозволяємо голосувати повторно
        await callback.answer(f"Ви вже проголосували за гравця {selected_player1}.")
        return
    
    players_voted.add(callback.from_user.id)
    vote_counts[selected_player1] += 1
    await callback.answer(f"Ваш голос за гравця {selected_player1} зараховано.")

    #player_id = callback.from_user.id
    #if player_id in players_voted:
        #await callback.answer("Ви вже проголосували!")
        #return

    #if player_voted in votes:
        #await callback_query.answer("Ви вже проголосували!", show_alert=True)
        #return


    # Додаємо голос
    #votes[player_voted] = vote_player
    #await callback_query.answer(f"Ви проголосували за {vote_player}")

    #votes[selected_player1] += 1
    #players_voted.add(player_id)
    #await callback.answer(f"Ваш голос за гравця {selected_player1} зараховано.")

    # Перевіряємо, чи всі проголосували
    # Якщо кількість голосів дорівнює кількості гравців
#####################################################################################
def get_players_with_max_votes(vote_counts):  # Якщо немає голосів, повертаємо порожній список
    if not vote_counts:
        return
    max_votes = max(vote_counts.values())  # Знаходимо максимальну кількість голосів
    players_with_max_votes = [player for player, votes in vote_counts.items() if votes == max_votes]
    print(players_with_max_votes)
    return players_with_max_votes
###########################################################################################################################################3

async def main():
    await set_bot_commands()
    await dp.start_polling(bot)

asyncio.run(main())
