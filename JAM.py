import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters.state import StatesGroup
from os import getenv
from sys import exit
import aiogram.utils.markdown as md
from aiogram.types import ParseMode
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
from functions.functions import compel_keyboard, send_master_text

bot_token = getenv("BOT_TOKEN")
master = getenv('MASTER_CHAT')

if not bot_token:
    exit("Error: no token provided")

bot = Bot(token=bot_token, parse_mode=types.ParseMode.HTML)

# Configure logging
logging.basicConfig(level=logging.INFO)

# parameters
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# in default aiogram we cannot set state to another user from other userpass
# here I define new class from the original to make this option real
class state(State):
    async def set(self, user=None):
        """Option to set state for concrete user"""
        state = dp.get_current().current_state(user=user)
        await state.set_state(self.state)


class CV(StatesGroup):
    user = state()  # user logi will be writen here
    code = state()  # Для выбора базы данных
    cv = state()  # Для выбора CV
    god = state()  # для автора - раздавать компелы
    god_message = state()  # переписка
    compel = state()  # Для игрока - принять или отклонить осложнение
    message = state()  # переписка
    god_chosen = state()  # Для автора - выбор игрока кому написать
    public = state()  # Для автора - выбор игрока кому написать
    attack = state() # для автора - начать атаку
    massacare = state() # для игрока - быть атокованным

attack_dict = {}

# dict with passwords and logins
# transfer later to the os env just like
# archer dash have been done
users = {
    'delirium': 'johny',
    'enigma13': 'dasha',
    'vydra_ela_pudru': 'arseny',
    '1337': 'r',
    'teston': 'test'
    # 'test': 'public'

}

doomsday_dict = {
    'johny': 12312,
    'dasha': 123121,
    'arseny': 123111,
    'r': 123123,
    'test': 123123
}

compel_dict_session_1 = {
    'johny': 'CV/compels/session1/Johny.txt',
    'gamedesigner': 'CV/compels/session1/olya.txt',
    'lina': 'CV/compels/session1/Lina.txt',
    'test': 'CV/compels/session1/test.txt'
}

code = ''
path_dict = {
    'akroni': {'cv': 'CV/characters/fernando_akroni/Fernando.jpg',
               'text': 'CV/characters/fernando_akroni/Fernando.txt'},
    # 'Lucio': {'cv': 'CV{0}/Lucio/Lucio.jpg',
    #         'text': 'CV/Lucio/Lucio.txt'},
    'damian': {'cv': 'CV/characters/damian_orton/Damian.jpg',
               'text': 'CV/characters/damian_orton/damian.txt'},
    #'mihail': {'cv': 'CV/characters/players/mihail.jpg',
     #          'text': 'CV/characters/players/Mihail.txt'},
    #'oleg': {'cv': 'CV/characters/players/oleg.jpeg',
      #       'text': 'CV/characters/players/Oleg.txt'},
    #'hydra': {'cv': 'CV/characters/players/Hydra.jpg',
     #         'text': 'CV/characters/players/Hydra.txt'},
    'brinn': {'cv': 'CV/characters/brinn_the_rat/Brinn.jpg',
              'text': 'CV/characters/brinn_the_rat/Brinn.txt'},
    'shuttle-center': {'cv': 'CV/locations/shattle-center/shattle-center.jpg',
                       'text': 'CV/locations/shattle-center/shattle-center.txt'},
    'apollon': {'cv': 'CV/locations/train/train.jpg',
                'text': 'CV/locations/train/train.txt'},
    'csi': {'cv': 'CV/locations/CSI/csi.jpg',
            'text': 'CV/locations/CSI/CSI.txt'},
    'mayfall': {'cv': 'CV/locations/MayFall/mayfall.jpg',
                'text': 'CV/locations/MayFall/mayfall.txt'},
    'johny more': {'cv': 'CV/characters/JohnyMore/more.jpeg',
                'text': 'CV/characters/JohnyMore/more.txt'},
    '0021': {'text': 'CV/documents/order0021/order0021.txt'},
    'hr': {'text': 'CV/characters/hr/hr.txt',
           'cv': 'CV/characters/hr/hr.jpg'}
}

char_dict = {
    'dec': {'cv': 'CV/pc/dec.jpeg',
               'text': 'CV/pc/dec.txt'},
    'killer': {
        # 'cv': 'CV/pc/dec.jpeg',
               'text': 'CV/pc/killer.txt'},
    'maxwell': {
        # 'cv': 'CV/pc/dec.jpeg',
               'text': 'CV/pc/maxwell.txt'}
}


menace_list = {
    'shattle_center': {'cv': 'CV/locations/shattle-center/shattle-center.jpg',
            'text': 'CV/locations/shattle-center/security.txt'},
    'rats': {'cv': 'CV/characters/brinn_the_rat/the_rat.jpg',
             'text': 'CV/characters/brinn_the_rat/Rats.txt'},
    'pigs': {'cv': 'CV/characters/koh/pigs.jpeg',
             'text': 'CV/characters/koh/pigs.txt'},
}

csi_past = {

    'damian': {'cv': 'CV/characters/damian_orton/Damian.jpg',
               'text': 'CV/characters/damian_orton/csi_version.txt'},
    'csi': {'cv': 'CV/locations/CSI/csi.jpg',
            'text': 'CV/locations/CSI/security.txt'},
    'death_squad': {'cv': 'CV/characters/death_squad/death_squad.jpeg',
                    'text': 'CV/characters/death_squad/death_squad.txt'},
}

let_it_fall = {
    'koh': {'cv': 'CV/characters/koh/koh.jpeg',
            'text': 'CV/characters/koh/koh.txt'},
    'metzgerai': {'cv': 'CV/locations/metzgerai/metzgerai.jpeg',
                  'text': 'CV/locations/metzgerai/metzgerai.txt'},
    'xian': {'cv': 'CV/characters/xian/png.jpg',
              'text': 'CV/characters/xian/xian.txt'},
}

personal_path_hacker = {
    'koh': {'cv': 'CV/characters/koh/koh.jpeg',
            'text': 'CV/characters/koh/koh.txt'},
    'sister': {'cv': 'CV/characters/sister/mary.jpeg',
               'text': 'CV/characters/sister/mary.txt'},
    'pigs': {'cv': 'CV/characters/koh/pigs.jpeg',
             'text': 'CV/characters/koh/pigs.txt'},
    'metzgerai': {'cv': 'CV/locations/metzgerai/metzgerai.jpeg',
                  'text': 'CV/locations/metzgerai/metzgerai.txt'},
}

personal_path_reshala = {
    'death_squad': {'cv': 'CV/characters/death_squad/death_squad.jpg',
                    'text': 'CV/characters/death_squad/death_squad.txt'},
    'rats': {'cv': 'CV/characters/brinn_the_rat/the_rat.jpg',
             'text': 'CV/characters/brinn_the_rat/Rats.txt'},
    'squad': {'cv': 'CV/characters/squad/squad.jpeg',
              'text': 'CV/characters/squad/squad.txt'},
    # 'csi hq': {'cv': 'CV/locations/MayFall/mayfall.jpg',
    #             'text': 'CV/locations/MayFall/mayfall.txt'},
}

nda3091 = {
    'slum_area': {'cv': 'CV/locations/slum_area/slum_area.jpeg',
                  'text': 'CV/locations/slum_area/slum_area.txt'},
    'chemical_plant': {'cv': 'CV/locations/chemical_plant/chemical_plant.jpeg',
                       'text': 'CV/locations/chemical_plant/chemical_plant.txt'},
}


@dp.message_handler(state='*', commands=['cancel'])
async def cancel_handler(message: types.Message, state: FSMContext):
    """Allow user to cancel action via /cancel command"""

    current_state = await state.get_state()
    if current_state is None:
        # User is not in any state, ignoring
        return
    # Cancel state and inCV user about it
    await state.finish()
    await message.reply('Cancelled.')


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message, state: FSMContext):
    await message.reply(
        "Запрос на получение доступа в систему...\nДля подключения профиля введите персональный пароль.")
    await state.set_state(CV.user.state)

@dp.message_handler(state='*', commands=['help'])
async def send_help(message: types.Message, state: FSMContext):
    await message.reply(
        "Это ваш персональный помощник, созданный компанией MayFall.\nДля начала работы введите команду /start")
    await message.reply(
        "Доступные опции в текущий момент перечислены ниже в меню управления")
    await message.reply(
        "Чтобы вернуться на опцию входа в профиль введите /cancel\nДля сообщения мастеру введите команду /message\nДля прекращения общения с мастером введите команду /stop\nЧтобы вернуться на предыдущий статус (выбор базы данных) /back")
    await message.reply(
        "По любым не решенным вопросам обратитесь к мастеру напрямую или в чат вашего юнита")


@dp.message_handler(state=CV.user)
async def process_code(message: types.Message, state: FSMContext):
    """Process user name"""

    if message.text.lower() in users.keys():
        async with state.proxy() as data:
            name = users[message.text.lower()]
            data['user'] = name
            # And send message
            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text(f"Привтствую: {md.bold(data['user'])}, предоставляю доступ к базе данных...")
                    # sep='\n',
                ),
                parse_mode=ParseMode.MARKDOWN,
            )
            await send_master_text(bot, master, data, "вошел")
        await CV.code.set()
        doomsday_dict[data['user']] = message.from_user.id
        await message.reply("Введите код доступа к базе")

    elif message.text.lower() == 'mycreator':
        await message.reply("Приветствую, создатель")
        await CV.god.set()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for name in range(1, 4):
            keyboard.add(str(name))
        keyboard.add('message')
        await message.answer("Сессия или команда:", reply_markup=keyboard)

    elif message.text.lower() == 'test':
        await message.reply("Приветствую, тестировщик")
        await CV.public.set()
        cv_list = list(path_dict.keys())
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add('/back')
        keyboard.add('/message')
        await state.update_data(code=message.text.lower())
        for name in cv_list:
            if name not in ['0021', 'hr']:
                keyboard.add(name)
        await message.answer("Выберите досье:", reply_markup=keyboard)
    # Finish our conversation
    return


@dp.message_handler(state=CV.god)
async def god_action(message: types.Message, state: FSMContext):
    async with state.proxy() as data:

        if message.text.lower() == 'message':
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            await state.set_state(CV.god_chosen.state)
            for player in list(doomsday_dict.keys()):
                keyboard.add(player)
            await message.answer("Выберите игрока:", reply_markup=keyboard)

        if message.text.lower() == '1':
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for name in compel_dict_session_1.keys():
                keyboard.add(name)
            data['god'] = 1
            await message.answer("Компел:", reply_markup=keyboard)
        elif message.text.lower() == '2':
            return
        elif message.text.lower() == '3':
            return

        if message.text.lower() in doomsday_dict.keys():
            if data['god'] == 1:
                keyboard = compel_keyboard()
                with open(compel_dict_session_1[message.text.lower()], encoding='utf-8') as f:
                    lines = f.readlines()
                text = ''.join(lines)
                await bot.send_message(chat_id=doomsday_dict[message.text.lower()], reply_markup=keyboard,
                                       text=md.text(
                                           text,
                                           sep='\n'
                                       ),
                                       parse_mode=ParseMode.MARKDOWN,
                                       )
                await bot.send_message(chat_id=doomsday_dict[message.text.lower()], text=md.text(
                    md.text(f"{compel_dict_session_1[message.text.lower()]}")
                    # sep='\n',
                ),
                                       parse_mode=ParseMode.MARKDOWN,
                                       )
                new_state = dp.current_state(chat=doomsday_dict[message.text.lower()],
                                             user=doomsday_dict[message.text.lower()])
                await new_state.set_state(CV.compel.state)
                await CV.compel.set(user=doomsday_dict[message.text.lower()])


@dp.message_handler(state=CV.compel, commands=['message'])
async def process_code(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            if data['user'] is not None:
                try:
                    await state.set_state(CV.message.state)
                    data['message'] = 'compel'
                    await message.answer("Теперь ваши сообщения получает Мастер")
                    await message.answer("Для выхода из режима напишите /stop")
                except:
                    await state.set_state(CV.code.state)
                    await message.answer("Введите код доступа к нужной базе данных")
        except:
            await message.answer("Теперь ты тут навечно. Ха-ха-ха")


@dp.message_handler(state=CV.code, commands=['message'])
async def process_code(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            if data['user'] is not None:
                try:
                    await state.set_state(CV.message.state)
                    data['message'] = 'code'
                    await message.answer("Теперь ваши сообщения получает Мастер")
                    await message.answer("Для выхода из режима напишите /stop")
                except:
                    await state.set_state(CV.code.state)
                    await message.answer("Введите код доступа к нужной базе данных")
        except:
            await message.answer("Теперь ты тут навечно. Ха-ха-ха")


@dp.message_handler(state=CV.cv, commands=['message'])
async def process_code(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            if data['user'] is not None:
                try:
                    await state.set_state(CV.message.state)
                    data['message'] = 'cv'
                    await message.answer("Теперь ваши сообщения получает Мастер")
                    await message.answer("Для выхода из режима напишите /stop")
                except:
                    await state.set_state(CV.code.state)
                    await message.answer("Введите код доступа к нужной базе данных")
        except:
            await message.answer("Теперь ты тут навечно. Ха-ха-ха")


@dp.message_handler(state=CV.message, commands=['stop'])
async def process_code(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            if data['user'] is not None:
                try:
                    if data['message'] == 'compel':
                        await state.set_state(CV.compel.state)
                        keyboard = compel_keyboard()
                        await message.answer("Примите решение по компелу:", reply_markup=keyboard)
                        await send_master_text(bot, master, data, "закончил диалог")
                    else:
                        await state.set_state(CV.code.state)
                        await message.answer("Введите код доступа к нужной базе данных")
                        await send_master_text(bot, master, data, "закончил диалог")
                except:
                    await state.set_state(CV.code.state)
                    await message.answer("Введите код доступа к нужной базе данных")
                    await send_master_text(bot, master, data, "закончил диалог")
        except:
            await message.answer("Ты застрял здесь навечно")


@dp.message_handler(state=CV.message)
async def process_code(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await send_master_text(bot, master, data, message.text)


@dp.message_handler(state=CV.compel)
async def process_code(message: types.Message, state: FSMContext):
    async with state.proxy() as data:

        if message.text.lower() == 'принять':
            await send_master_text(bot, master, data, "Осложнение принято")
            await message.answer("Вы приняли осложнение. Сейчас мастер даст вам печеньку")
            await message.answer("Введите код доступа к нужной базе данных")
            await state.set_state(CV.code.state)

        elif message.text.lower() == 'отказаться':
            await send_master_text(bot, master, data, 'Осложнение отклонено')
            await message.answer("Вы отказались от осложнения, заплатите за это.")
            await message.answer("Введите код доступа к нужной базе данных")
            await state.set_state(CV.code.state)
        elif message.text.lower() == 'обсудить':
            await send_master_text(bot, master, data, "Хочет обсудить детали")
            await state.set_state(CV.message.state)
            await message.answer("Ваши сообщения теперь полуает мастер")
            data['message'] = 'compel'

            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add("/stop")
            await message.answer("Для выхода из режима общения наберите /stop", reply_markup=keyboard)

        else:
            await message.answer("Примите решение по осложнению.")


@dp.message_handler(state=CV.god_chosen)
async def process_code(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() in list(doomsday_dict.keys()):
            await state.set_state(CV.god_message.state)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add("/compel")
            keyboard.add("/change")
            keyboard.add("/attack")
            keyboard.add("/end_message")
            data['god_message'] = message.text.lower()
            await message.answer(f"Теперь все ваши сообщения получит {message.text.lower()}")
            await message.answer("Для выхода из режима напишите /end_message")
            await message.answer("Для атаки /attack")
            await message.answer("Для смены получателя /change", reply_markup=keyboard)

        else:
            await message.answer("пиздишь он(а) с тобой не играет")


@dp.message_handler(state=CV.god_message, commands=['end_message'])
async def end_conversation(message: types.Message, state: FSMContext):
    await state.set_state(CV.god.state)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in range(1, 4):
        keyboard.add(str(name))
    keyboard.add('message')
    await message.answer(f"общение завершено", reply_markup=keyboard)


@dp.message_handler(state=CV.god_message, commands=['change'])
async def change_subj(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await state.set_state(CV.god_chosen.state)
    for player in list(doomsday_dict.keys()):
        keyboard.add(player)
    await message.answer("Выберите игрока:", reply_markup=keyboard)


@dp.message_handler(state=CV.god_message, commands=['compel'])
async def process_code(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        keyboard = compel_keyboard()
        await bot.send_message(chat_id=doomsday_dict[data['god_message']], reply_markup=keyboard
                               , text=md.text(
                md.text(f"Вам навязано осложнение")
                # sep='\n',
            ),
                               parse_mode=ParseMode.MARKDOWN,
                               )
        new_state = dp.current_state(chat=doomsday_dict[data['god_message']], user=doomsday_dict[data['god_message']])
        await new_state.set_state(CV.compel.state)

@dp.message_handler(state=CV.god_message, commands=['attack'])
async def change_subj(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await state.set_state(CV.attack.state)
        await message.answer("Задайте навык атаки:")
        data['attack'] = {'Aspect_1':None,
                          'Aspect_2':None,
                          "attack":None,
                          'defence':None,
                          'stress':None,
                          'conseq':None
                          }

@dp.message_handler(state=CV.attack)
async def change_subj(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if data['attack']['Aspect_2'] is not None and message.text == 'start a massacare':
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            await bot.send_message(chat_id=doomsday_dict[data['god_message']]
                                   , text=md.text(
                    md.text(f"Вас пытаются взломать"),
                    md.text('Что известно о враждебной сущности:'),
                    md.text('{}'.format(data['attack']))
                    # sep='\n',
                ),
                                   parse_mode=ParseMode.MARKDOWN,
                                   )
            keyboard.add('message')
            await message.answer("Сессия или команда:", reply_markup=keyboard)
            await state.set_state(CV.god.state)

        if data['attack']['attack'] is None:
            data['attack']['attack'] = message.text.lower()
            await message.answer("Навык атаки задан. Теперь защита")
        elif data['attack']['defence'] is None:
            data['attack']['defence'] = message.text.lower()
            await message.answer("Навык защиты задан. Теперь стресс")
        elif data['attack']['stress'] is None:
            data['attack']['stress'] = message.text.lower()
            await message.answer("Навык атаки задан. Теперь число последствий")
        elif data['attack']['conseq'] is None:
            data['attack']['conseq'] = message.text.lower()
            await message.answer("Число последствий задано. Теперь Аспект 1")
        elif data['attack']['Aspect_1'] is None:
            data['attack']['Aspect_1'] = message.text.lower()
            await message.answer("Число последствий задано. Теперь Аспект 2")
        elif data['attack']['Aspect_2'] is None:
            data['attack']['Aspect_2'] = message.text.lower()

        if data['attack']['Aspect_2'] is not None:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add('start a massacare')
            await message.answer("Готовы начать резню.", reply_markup=keyboard)
@dp.message_handler(state=CV.god_message)
async def process_code(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await bot.send_message(chat_id=doomsday_dict[data['god_message']], text=md.text(
            md.text(f"От мастера: \n {message.text.lower()}")
            # sep='\n',
        ),
                               parse_mode=ParseMode.MARKDOWN,
                               )


@dp.message_handler(state=CV.code)
async def process_code(message: types.Message, state: FSMContext):
    if message.text.lower() == '123':
        cv_list = list(path_dict.keys())
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add('/back')
        keyboard.add('/message')
        await state.update_data(code=message.text.lower())
        for name in cv_list:
            if name not in ['0021', 'hr']:
                keyboard.add(name)
        await state.set_state(CV.cv.state)

        # And send message

        await bot.send_message(
            message.chat.id,
            md.text(
                md.text(f"Записанный код ведет в тестовую базу данных с общими для всех сотрудников CV")
                # sep='\n',
            ),
            parse_mode=ParseMode.MARKDOWN,
        )
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text(f"Для возврата на этап ввода кода к базе данных, введите /back")
                # sep='\n',
            ),
            parse_mode=ParseMode.MARKDOWN,
        )
        await message.answer("Выберите досье:", reply_markup=keyboard)
    elif message.text.lower() == '0021':
        async with state.proxy() as data:
            await state.set_state(CV.cv.state)
            data['code'] = '0021'
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add('0021')
            keyboard.add('hr')
            await send_master_text(bot, master, data, "Открыта пасхалка")
            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text(f"Для возврата на ввода кода, введите /back")
                    # sep='\n',
                ),
                parse_mode=ParseMode.MARKDOWN,
            )
            await message.answer("Выберите досье:", reply_markup=keyboard)
    elif message.text.lower() == 'char':
        async with state.proxy() as data:
            await state.set_state(CV.cv.state)
            cv_list = list(char_dict.keys())
            data['code'] = 'char'
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add('/back')
            keyboard.add('/message')
            for name in cv_list:
                keyboard.add(name)
            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text(f"Доступ к базе данных личных дел исполнителей открыт")
                    # sep='\n',
                ),
                parse_mode=ParseMode.MARKDOWN,
            )
            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text(f"Для возврата на ввода кода, введите /back")
                    # sep='\n',
                ),
                parse_mode=ParseMode.MARKDOWN,
            )
            await message.answer("Выберите досье:", reply_markup=keyboard)
    if message.text.lower() == 'csipast':
        cv_list = list(csi_past.keys())
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add('/back')
        keyboard.add('/message')
        await state.update_data(code=message.text.lower())
        for name in cv_list:
            keyboard.add(name)
        await state.set_state(CV.cv.state)
        async with state.proxy() as data:
            # And send message
            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text(f"Записанный код ведет в вашу личную базу данных")
                    # sep='\n',
                ),
                parse_mode=ParseMode.MARKDOWN,
            )
            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text(f"Для возврата на ввода кода, введите /back")
                    # sep='\n',
                ),
                parse_mode=ParseMode.MARKDOWN,
            )
        await message.answer("Выберите досье:", reply_markup=keyboard)
    if message.text.lower() == 'letitfall':
        cv_list = list(let_it_fall.keys())
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add('/back')
        keyboard.add('/message')
        await state.update_data(code=message.text.lower())
        for name in cv_list:
            keyboard.add(name)
        await state.set_state(CV.cv.state)
        async with state.proxy() as data:
            # And send message
            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text(f"Записанный код ведет в вашу личную базу данных")
                    # sep='\n',
                ),
                parse_mode=ParseMode.MARKDOWN,
            )
            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text(f"Для возврата на ввода кода, введите /back")
                    # sep='\n',
                ),
                parse_mode=ParseMode.MARKDOWN,
            )
        await message.answer("Выберите досье:", reply_markup=keyboard)
    if message.text.lower() == 'menace':
        cv_list = list(menace_list.keys())
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add('/back')
        keyboard.add('/message')
        await state.update_data(code=message.text.lower())
        for name in cv_list:
            keyboard.add(name)
        await state.set_state(CV.cv.state)
        async with state.proxy() as data:
            # And send message
            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text(f"Записанный код ведет в вашу личную базу данных")
                    # sep='\n',
                ),
                parse_mode=ParseMode.MARKDOWN,
            )
            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text(f"Для возврата на ввода кода, введите /back")
                    # sep='\n',
                ),
                parse_mode=ParseMode.MARKDOWN,
            )
        await message.answer("Выберите досье:", reply_markup=keyboard)
    if message.text.lower() == 'char':
        cv_list = list(char_dict.keys())
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add('/back')
        keyboard.add('/message')
        await state.update_data(code=message.text.lower())
        for name in cv_list:
            keyboard.add(name)
        await state.set_state(CV.cv.state)
        async with state.proxy() as data:
            # And send message
            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text(f"Записанный код ведет в вашу личную базу данных")
                    # sep='\n',
                ),
                parse_mode=ParseMode.MARKDOWN,
            )
            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text(f"Для возврата на ввода кода, введите /back")
                    # sep='\n',
                ),
                parse_mode=ParseMode.MARKDOWN,
            )
        await message.answer("Выберите досье:", reply_markup=keyboard)

    if message.text.lower() == 'maryyyyyyyyyy':
        cv_list = list(personal_path_hacker.keys())
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add('/back')
        keyboard.add('/message')
        await state.update_data(code=message.text.lower())
        for name in cv_list:
            keyboard.add(name)
        await state.set_state(CV.cv.state)
        async with state.proxy() as data:
            # And send message
            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text(f"Ваш код: {md.bold(data['code'])}, записан")
                    # sep='\n',
                ),
                parse_mode=ParseMode.MARKDOWN,
            )
            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text(f"Записанный код ведет в вашу личную базу данных")
                    # sep='\n',
                ),
                parse_mode=ParseMode.MARKDOWN,
            )
            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text(f"Для возврата на ввода кода, введите /back")
                    # sep='\n',
                ),
                parse_mode=ParseMode.MARKDOWN,
            )
        await message.answer("Выберите досье:", reply_markup=keyboard)

    elif message.text.lower() == 'diaryyyyyyyyyy':
        cv_list = list(personal_path_reshala.keys())
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        await state.update_data(code=message.text.lower())
        for name in cv_list:
            if name not in ['0021', 'hr']:
                keyboard.add(name)
        await state.set_state(CV.cv.state)

        # Finish our conversation
        async with state.proxy() as data:
            # And send message
            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text(f"Ваш код: {md.bold(data['code'])}, записан")
                    # sep='\n',
                ),
                parse_mode=ParseMode.MARKDOWN,
            )
            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text(f"Записанный код ведет в вашу личную базу данных")
                    # sep='\n',
                ),
                parse_mode=ParseMode.MARKDOWN,
            )
            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text(f"Для возврата на ввода кода, введите /back")
                    # sep='\n',
                ),
                parse_mode=ParseMode.MARKDOWN,
            )
        await message.answer("Выберите досье:", reply_markup=keyboard)

    elif message.text.lower() == 'nda3091':
        cv_list = list(nda3091.keys())
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        await state.update_data(code=message.text.lower())
        for name in cv_list:
            if name not in ['0021', 'hr']:
                keyboard.add(name)
        await state.set_state(CV.cv.state)

        # Finish our conversation
        async with state.proxy() as data:
            # And send message
            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text(f"Ваш код: {md.bold(data['code'])}, записан")
                    # sep='\n',
                ),
                parse_mode=ParseMode.MARKDOWN,
            )
            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text(
                        f"Записанный код ведет в базу данных, сформированную из собранных данных из мозга сотрудника CSI")
                    # sep='\n',
                ),
                parse_mode=ParseMode.MARKDOWN,
            )
            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text(f"Для возврата на ввода кода, введите /back")
                    # sep='\n',
                ),
                parse_mode=ParseMode.MARKDOWN,
            )
        await message.answer("Выберите досье:", reply_markup=keyboard)

    else:
        await message.answer("Указанный код не ведет ни к одной из существующих баз данных")


@dp.message_handler(state=CV.cv, commands=['back'])
async def send_file(message: types.Message, state: FSMContext):
    await message.answer("Введите код к нужной базе данных")
    await state.set_state(CV.code.state)

@dp.message_handler(state=CV.public)
async def send_file(message: types.Message, state: FSMContext):
    current_cv = message.text.lower()
    if current_cv in path_dict.keys():
        photo = open(path_dict[current_cv]['cv'], "rb")
        with open(path_dict[current_cv]['text'], encoding='utf-8') as f:
            lines = f.readlines()
        text = ''.join(lines)
        await bot.send_photo(message.from_user.id, photo)
        await message.reply(text)
    else:
        await message.reply('Указаного CV нет в вашей базе')

@dp.message_handler(state=CV.cv)
async def send_file(message: types.Message, state: FSMContext):
    current_cv = message.text.lower()
    async with state.proxy() as data:
        if data['code'] == '123':
            if current_cv in path_dict.keys():
                photo = open(path_dict[current_cv]['cv'], "rb")
                with open(path_dict[current_cv]['text'], encoding='utf-8') as f:
                    lines = f.readlines()
                text = ''.join(lines)
                await bot.send_photo(message.from_user.id, photo)
                await message.reply(text)
            else:
                await message.reply('Указаного CV нет в вашей базе')
        if data['code'] == 'char':
            if current_cv in char_dict.keys():
                try:
                    photo = open(char_dict[current_cv]['cv'], "rb")
                    await bot.send_photo(message.from_user.id, photo)
                except:
                    pass
                with open(char_dict[current_cv]['text'], encoding='utf-8') as f:
                    lines = f.readlines()
                text = ''.join(lines)
                await message.reply(text)
            else:
                await message.reply('Указаного CV нет в вашей базе')
        elif data['code'] == '0021':
            try:
                photo = open(path_dict[current_cv]['cv'], "rb")
                await bot.send_photo(message.from_user.id, photo)
            except:
                pass
            with open(path_dict[current_cv]['text'], encoding='utf-8') as f:
                lines = f.readlines()
            text = ''.join(lines)
            await message.reply(text)
        elif data['code'] == 'menace':
            try:
                photo = open(menace_list[current_cv]['cv'], "rb")
                await bot.send_photo(message.from_user.id, photo)
            except:
                pass
            with open(menace_list[current_cv]['text'], encoding='utf-8') as f:
                lines = f.readlines()
            text = ''.join(lines)
            await message.reply(text)
        elif data['code'] == '0021':
            try:
                photo = open(path_dict[current_cv]['cv'], "rb")
                await bot.send_photo(message.from_user.id, photo)
            except:
                pass
            with open(path_dict[current_cv]['text'], encoding='utf-8') as f:
                lines = f.readlines()
            text = ''.join(lines)
            await message.reply(text)
        elif data['code'] == 'mary':
            try:
                photo = open(personal_path_hacker[current_cv]['cv'], "rb")
                await bot.send_photo(message.from_user.id, photo)
            except:
                pass
            with open(personal_path_hacker[current_cv]['text'], encoding='utf-8') as f:
                lines = f.readlines()
            text = ''.join(lines)
            await message.reply(text)
        elif data['code'] == 'diary':
            try:
                photo = open(personal_path_reshala[current_cv]['cv'], "rb")
                await bot.send_photo(message.from_user.id, photo)
            except:
                pass
            with open(personal_path_reshala[current_cv]['text'], encoding='utf-8') as f:
                lines = f.readlines()
            text = ''.join(lines)
            await message.reply(text)
        elif data['code'] == 'nda3091':
            try:
                photo = open(nda3091[current_cv]['cv'], "rb")
                await bot.send_photo(message.from_user.id, photo)
            except:
                pass
            with open(nda3091[current_cv]['text'], encoding='utf-8') as f:
                lines = f.readlines()
            text = ''.join(lines)
            await message.reply(text)
        elif data['code'] == 'menace':
            try:
                photo = open(menace_list[current_cv]['cv'], "rb")
                await bot.send_photo(message.from_user.id, photo)
            except:
                pass
            with open(menace_list[current_cv]['text'], encoding='utf-8') as f:
                lines = f.readlines()
            text = ''.join(lines)
            await message.reply(text)
        elif data['code'] == 'letitfall':
            try:
                photo = open(let_it_fall[current_cv]['cv'], "rb")
                await bot.send_photo(message.from_user.id, photo)
            except:
                pass
            with open(let_it_fall[current_cv]['text'], encoding='utf-8') as f:
                lines = f.readlines()
            text = ''.join(lines)
            await message.reply(text)
        elif data['code'] == 'csipast':
            try:
                photo = open(csi_past[current_cv]['cv'], "rb")
                await bot.send_photo(message.from_user.id, photo)
            except:
                pass
            with open(csi_past[current_cv]['text'], encoding='utf-8') as f:
                lines = f.readlines()
            text = ''.join(lines)
            await message.reply(text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
