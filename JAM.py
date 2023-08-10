import logging
import aiogram as aio
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

bot_token = getenv("BOT_TOKEN")
master = getenv('MASTER_CHAT')

if not bot_token:
    exit("Error: no token provided")

bot = Bot(token=bot_token, parse_mode=types.ParseMode.HTML)

# Configure logging
logging.basicConfig(level=logging.INFO)

## parameters
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class state(State):
    async def set(self, user=None):
        """Option to set state for concrete user"""
        state = dp.get_current().current_state(user=user)
        await state.set_state(self.state)


class CV(StatesGroup):
    user = state()  # user logi will be writen here
    code = state()  # Will be represented in storage as 'Form:name'
    cv = state()  # Will be represented in storage as 'Form:age'
    contract = state()  # Will be represented in storage as 'Form:gender'
    god = state()  # для автора - раздавать компелы
    god_message = state()  # переписка
    compel = state()
    message = state()  # переписка
    god_chosen = state()


# dict with passwords and logins
# transfer later to the os env just like
# archer dash have been done
users = {
    'delirium': 'johny',
    'drozd': 'lina',
    'hse': 'gamedesigner',
    'test': 'test'
}

doomsday_dict = {
    'johny': 12312,
    'revolution': 123121,
    'gamedesigner': 123111,
    'test': 123123
}

compel_dict_session_1 = {
    'johny': 'Принять контракт от MayFall, убить или похитить ученого, доставить его разработку в корпорацию.',
    'gamedesigner': 'Принять контракт от MayFall, убить или похитить ученого, доставить его разработку в корпорацию.',
    'lina': 'Принять контракт от MayFall, убить или похитить ученого, доставить его разработку в корпорацию.',
    'test': 'Принять контракт от MayFall, убить или похитить ученого, доставить его разработку в корпорацию.'
}

code = ''
path_dict = {
    'akroni': {'cv': 'CV/characters/Fernando_Akroni/Fernando.jpg',
               'text': 'CV/characters/Fernando_Akroni/Fernando.txt'},
    # 'Lucio': {'cv': 'CV{0}/Lucio/Lucio.jpg',
    #         'text': 'CV/Lucio/Lucio.txt'},
    'damian': {'cv': 'CV/characters/damian_orton/Damian.jpg',
               'text': 'CV/characters/damian_orton/damian.txt'},
    'mihail': {'cv': 'CV/characters/players/mihail.jpg',
               'text': 'CV/characters/players/Mihail.txt'},
    'hydra': {'cv': 'CV/characters/players/Hydra.jpg',
               'text': 'CV/characters/players/Hydra.txt'},
    'brinn': {'cv': 'CV/characters/brinn_the_rat/Brinn.jpg',
              'text': 'CV/characters/brinn_the_rat/Brinn.txt'},
    'shuttle-center': {'cv': 'CV/locations/shattle-center/shattle-center.jpg',
                       'text': 'CV/locations/shattle-center/shattle-center.txt'},
    'apollon': {'cv': 'CV/locations/train/train.jpg',
                'text': 'CV/locations/train/train.txt'},
    'csi': {'cv': 'CV/locations/csi/csi.jpg',
            'text': 'CV/locations/csi/csi.txt'},
    'mayfall': {'cv': 'CV/locations/mayfall/mayfall.jpg',
                'text': 'CV/locations/mayfall/mayfall.txt'},
    '0021': {'text': 'CV/documents/order0021/order0021.txt'},
    'hr': {'text': 'CV/characters/hr/hr.txt',
           'cv': 'CV/characters/hr/hr.jpg'}
}

cv_list = list(path_dict.keys())


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


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message, state: FSMContext):
    await message.reply(
        "Запрос на получение доступа в систему...\nДля подключения профиля введите персональный пароль.")
    await state.set_state(CV.user.state)


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
            await bot.send_message(chat_id=master, text=md.text(
                md.text(f"{md.bold(data['user'])}, вошел")
                # sep='\n',
            ),
                                   parse_mode=ParseMode.MARKDOWN,
                                   )
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
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add("Принять")
                keyboard.add('Отказаться')
                keyboard.add('Обсудить')
                await bot.send_message(chat_id=doomsday_dict[message.text.lower()], reply_markup=keyboard
                                       , text=md.text(
                        md.text(f"Вам навязано осложнение")
                        # sep='\n',
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


@dp.message_handler(state=[CV.cv, CV.code], commands=['message'])
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


@dp.message_handler(state=CV.message, commands=['stop'])
async def process_code(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            if data['user'] is not None:
                try:
                    if data['message'] == 'compel':
                        await state.set_state(CV.compel.state)
                        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        keyboard.add("Принять")
                        keyboard.add('Отказаться')
                        keyboard.add('Обсудить')
                        await message.answer("Примите решение по компелу:", reply_markup=keyboard)
                        await bot.send_message(chat_id=master, text=md.text(
                            md.text(f"{md.bold(data['user'])}, закончил диалог")
                            # sep='\n',
                        ),
                                               parse_mode=ParseMode.MARKDOWN,
                                               )
                    else:
                        await state.set_state(CV.code.state)
                        await message.answer("Введите код доступа к нужной базе данных")
                        await bot.send_message(chat_id=master, text=md.text(
                            md.text(f"{md.bold(data['user'])}, закончил диалог")
                            # sep='\n',
                        ),
                                               parse_mode=ParseMode.MARKDOWN,
                                               )
                except:
                    await state.set_state(CV.code.state)
                    await message.answer("Введите код доступа к нужной базе данных")
                    await bot.send_message(chat_id=master, text=md.text(
                        md.text(f"{md.bold(data['user'])}, закончил диалог")
                        # sep='\n',
                    ),
                                           parse_mode=ParseMode.MARKDOWN,
                                           )
        except:
            await message.answer("Ты застрял здесь навечно")


@dp.message_handler(state=CV.message)
async def process_code(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await bot.send_message(chat_id=master, text=md.text(
            md.text(f"{md.bold(data['user'])}, {message.text}")
            # sep='\n',
        ), parse_mode=ParseMode.MARKDOWN,
                               )


@dp.message_handler(state=CV.compel)
async def process_code(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await bot.send_message(chat_id=master, text=md.text(
            md.text(f"{md.bold(data['user'])}, навязано осложнение")
            # sep='\n',
        ),
                               parse_mode=ParseMode.MARKDOWN,
                               )
    if message.text.lower() == 'принять':
        await bot.send_message(chat_id=master, text=md.text(
            md.text(f"{md.bold(data['user'])}, Осложнение принято")
            # sep='\n',
        ),
                               parse_mode=ParseMode.MARKDOWN,
                               )
        await message.answer("Введите код доступа к нужной базе данных")
        await state.set_state(CV.code.state)

    elif message.text.lower() == 'отказаться':
        await bot.send_message(chat_id=master, text=md.text(
            md.text(f"{md.bold(data['user'])}, Осложнение отклонено")
            # sep='\n',
        ),
                               parse_mode=ParseMode.MARKDOWN,
                               )
        await message.answer("Введите код доступа к нужной базе данных")
        await state.set_state(CV.code.state)
    elif message.text.lower() == 'обсудить':
        await state.set_state(CV.message.state)
        await message.answer("Ваши сообщения теперь полуает мастер")
        data['message'] = 'compel'

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("/stop")

    else:
        await message.answer("Примите решение.")


@dp.message_handler(state=CV.god_chosen)
async def process_code(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() in list(doomsday_dict.keys()):
            await state.set_state(CV.god_message.state)
            data['god_message'] = message.text.lower()
            await message.answer(f"Теперь все ваши сообщения получит {message.text.lower()}")
            await message.answer("Для выхода из режима напишите /end_message")
            await message.answer("Для смены получателя /change")
        else:
            await message.answer("пиздишь он(а) с тобой не играет")


@dp.message_handler(state=CV.god_message, commands=['end_message'])
async def end_conversation(message: types.Message, state: FSMContext):
    await state.set_state(CV.god.state)
    await message.answer(f"общение завершено")


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
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("Принять")
        keyboard.add('Отказаться')
        keyboard.add('Обсудить')
        await bot.send_message(chat_id=doomsday_dict[data['god_message']], reply_markup=keyboard
                               , text=md.text(
                md.text(f"Вам навязано осложнение")
                # sep='\n',
            ),
                               parse_mode=ParseMode.MARKDOWN,
                               )
        new_state = dp.current_state(chat=doomsday_dict[data['god_message']], user=doomsday_dict[data['god_message']])
        await new_state.set_state(CV.compel.state)


@dp.message_handler(state=CV.god_message)
async def process_code(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await bot.send_message(chat_id=doomsday_dict[data['god_message']], text=md.text(
            md.text(f"От мастера: {message.text.lower()}")
            # sep='\n',
        ),
                               parse_mode=ParseMode.MARKDOWN,
                               )


@dp.message_handler(state=CV.code)
async def process_code(message: types.Message, state: FSMContext):
    """Process user name"""
    if message.text.lower() == '123':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        await state.update_data(code=message.text.lower())
        for name in cv_list:
            if name not in ['0021','hr']:
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
                    md.text(f"Записанный код ведет в тестовую базу данных с общими для всех сотрудников CV")
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
    elif message.text.lower() == '0021':
        async with state.proxy() as data:
            await state.set_state(CV.cv.state)
            data['code'] = '0021'
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add('0021')
            keyboard.add('hr')
            await bot.send_message(chat_id=master, text=md.text(
                md.text(f"{md.bold(data['user'])}, Открыта пасхалка")
                # sep='\n',
            ),parse_mode=ParseMode.MARKDOWN,)
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



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
