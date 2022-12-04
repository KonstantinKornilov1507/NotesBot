import asyncio
import logging
from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.dispatcher.filters import Text, state
from aiogram.dispatcher import FSMContext
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import keyboard as kb
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import pickle
import ObjectsandNames as ON
import pickle
from Token import TOKEN
from Globals import Nam

def extract(path):
    with open(path, 'rb') as inputFile:
        OBJECT = pickle.load(inputFile)
        return OBJECT

def save(path, skills):
    with open(path, 'wb') as outputFile:
        pickle.dump(skills, outputFile)

bot = Bot(token=TOKEN)

memmory = MemoryStorage()

dp = Dispatcher(bot, storage=memmory)

class Make(StatesGroup):
    name = State()
    text = State()
    change = State()
    delete = State()
    change_note = State()
    send = State()
    send_name = State()
    send_note = State()
    registration_name = State()
    privacy = State()
    share_first = State()
    share_second = State()
    share_third = State()

@dp.message_handler(commands=['start'], state=None)
async def process_start_command(messege: types.Message):
    if messege.from_user.id not in OBJECT.Notes_of_Ussers.keys():
      OBJECT.create_user(messege.from_user.id)
      await messege.reply("!Привет!\nЯ буду работать с твоими заметками!\n "
                          "Для начала пройди регистрациюю \n "
                          "Введи мне свой ник")
      await Make.registration_name.set()
    else:
        await bot.send_message(messege.from_user.id,"Ты уже зарегестрирован",
                               reply_markup=kb.help_kb)

@dp.message_handler(state = Make.registration_name)
async def command_start(messege: types.Message, state: FSMContext):
    reg_name = messege.text
    if reg_name  in OBJECT.Nick.keys():
        await bot.send_message(messege.from_user.id,"Такой ник уже существует,"
                                                    " попробуй еще раз")
    else:
        OBJECT.registration(messege.from_user.id, reg_name)
        await bot.send_message(messege.from_user.id, reg_name + ", молодец тепер давай определимся с твоим аккаунтом.\n"
                                                                " Если ты хочешь, чтобы другие пользователи"
                                                                " могли отсылать тебе заметки нажми: \n "
                                                                "/public \n иначе нажми /private ")
    await state.finish()

@dp.message_handler(commands=['private'])
async def process_start_command(messege: types.Message, state: FSMContext):
    OBJECT.set_privacy("private", messege.from_user.id)
    await messege.reply("Молодец, ты закончил этап регистрации, "
                        "теперь нажми /help, чтобы узнать, что я могу:")

@dp.message_handler(commands=['public'], state=None)
async def process_start_command(messege: types.Message):
    OBJECT.set_privacy("public", messege.from_user.id)
    await messege.reply("Молодец, ты закончил этап регистрации, "
                        "теперь нажми /help, чтобы узнать, что я могу:")


@dp.message_handler(commands=['help'], state=None)
async def process_start_command(message: types.Message):
    await message.reply("Я могу делать следующее:", reply_markup=kb.help_kb)

@dp.message_handler(commands=['deleteac'], state=None)
async def process_start_command(message: types.Message):
    OBJECT.Delete(message.from_user.id)
    await message.reply("Ваш аккаунт был удален"
                        "\n нажмите /start чтобы начать все заново")


@dp.message_handler(state= None)
async def process_start_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Извините я не понимаю что делать,"
                                                 " выберите одну из команд ",
                           reply_markup=kb.help_kb)


@dp.callback_query_handler(lambda c: c.data == '1', state= None)
async def show(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Введите название заметки")
    await Make.name.set()


@dp.message_handler(state= Make.name)
async def command_start(messege: types.Message, state: FSMContext):
    Nam.append(messege.text)
    await bot.send_message(messege.chat.id, 'Введите заметку')
    await Make.text.set()


@dp.message_handler(state = Make.text)
async def command_start(messege: types.Message, state: FSMContext):
    f = messege.text
    OBJECT.make_note(Nam[0], f, messege.from_user.id)
    Nam.clear()
    await bot.send_message(messege.from_user.id, 'Ваша заметка успешно добавлена,\n '
                                                 'чтобы ее просмотреть нажмите /help'
                                                 ' и перейдите в раздел мои заметки')
    await state.finish()


@dp.callback_query_handler(lambda c: c.data == '2', state= None)
@dp.message_handler(state=None)
async def command_start(messege: types.Message, state: FSMContext):
    if OBJECT.Userlen(messege.from_user.id) == 0:
        await bot.send_message(messege.from_user.id, "у тебя нет заметок, "
                                                     "нажми /help,  чтобы ее сделать\n")
    else:
        dict = OBJECT.Notes_of_Ussers[messege.from_user.id]
        for note in dict.keys():
            await bot.send_message(messege.from_user.id, note + "\n" + dict[note])


@dp.callback_query_handler(lambda c: c.data == '4', state= None)
@dp.message_handler(state=None)
async def command_start(messege: types.Message, state: FSMContext):
    if OBJECT.Userlen(messege.from_user.id) == 0:
        await bot.send_message(messege.from_user.id, "у тебя нет заметок,"
                                                     "\nно ты можешь ее сделать", reply_markup=kb.help_kb)
    else:
        await bot.send_message(messege.from_user.id, "Введите название заметки,"
                                                     " которую хотите удалить")
        await Make.delete.set()


@dp.message_handler(state = Make.delete)
async def command_start(messege: types.Message, state: FSMContext):
    txt = messege.text
    if txt not in OBJECT.Notes_of_Ussers[messege.from_user.id].keys():
        await bot.send_message(messege.from_user.id,'Увы, такой заметки не существует,'
                                                    ' попробуйте еще раз',
                               reply_markup=kb.help_kb)
        await state.finish()
    else:
        OBJECT.delete_note(messege.from_user.id, txt)
        await bot.send_message(messege.from_user.id, 'Ваша заметка успешна удалена',
                               reply_markup=kb.help_kb)
        await state.finish()


@dp.callback_query_handler(lambda c: c.data == '5', state= None)
@dp.message_handler(state=None)
async def command_start(messege: types.Message, state: FSMContext):
    if OBJECT.Userlen(messege.from_user.id) == 0:
        await bot.send_message(messege.from_user.id, "У тебя нет заметок,"
                                                     "\nно ты можешь ее сделать",
                               reply_markup=kb.help_kb)
    else:
        await bot.send_message(messege.from_user.id, "Введите название заметки,"
                                                     " которую хотите изменить")
        await Make.change.set()


@dp.message_handler(state=Make.change)
async def command_start(messege: types.Message, state: FSMContext):
    Nam.append(messege.text)
    if Nam[0] not in OBJECT.Notes_of_Ussers[messege.from_user.id].keys():
        await bot.send_message(messege.from_user.id,
                               "Увы,  такой заметки не существует,"
                               " попробуйте еще раз", reply_markup=kb.help_kb)
        Nam.clear()
        await state.finish()
    else:
        old_note =  OBJECT.Notes_of_Ussers[messege.from_user.id][Nam[0]]
        await bot.send_message(messege.from_user.id, 'Вот твоя заметка, скопируй ее,'
                                                     ' внеси поправки и отошли мне')
        await bot.send_message(messege.from_user.id, old_note)
        await Make.change_note.set()

@dp.message_handler(state=Make.change_note)
async def command_start(messege: types.Message, state: FSMContext):
    new_note = messege.text
    OBJECT.change(messege.from_user.id, new_note, Nam[0])
    Nam.clear()
    await bot.send_message(messege.from_user.id, 'Ваша заметка успешно изменена',
                           reply_markup=kb.help_kb)
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == '3', state= None)
@dp.message_handler(state=None)
async def command_start(messege: types.Message, state: FSMContext):
    if OBJECT.Userlen(messege.from_user.id) == 0:
        await bot.send_message(messege.from_user.id, "У вас нет заметок,"
                                                     " которыми вы можете поделиться",
                               reply_markup=kb.help_kb)
    else:
        await bot.send_message(messege.from_user.id, "Введите название заметки,"
                                                     " которой хотите поделиться")
        await Make.share_first.set()

@dp.message_handler(state=Make.share_first)
async def command_start(messege: types.Message, state: FSMContext):
    Nam.append(messege.text)
    if Nam[0] not in OBJECT.Notes_of_Ussers[messege.from_user.id].keys():
        await bot.send_message(messege.from_user.id, "У вас нет такой заметки, попробуйте заново",
                               reply_markup=kb.help_kb)
        Nam.clear()
        await state.finish()
    else:
        await bot.send_message(messege.from_user.id, "Введите ник пользователя, с которым хотите поделиться"
                                                     " \nЧтобы узнать доступных пользователей \n"
                                                     " нажми /givemeusers")
        await Make.share_second.set()

@dp.message_handler(commands=['givemeusers'], state= Make.share_second)
async def process_start_command(message: types.Message, state: FSMContext):
     available_user = OBJECT.nick_to_share(message.from_user.id)
     if len(available_user) == 0:
        await bot.send_message(message.from_user.id, "Увы пока-что нет пользователей",
                               reply_markup=kb.help_kb)
        await state.finish()
     else:
        for i in available_user:
            await bot.send_message(message.from_user.id, i)

@dp.message_handler(state=Make.share_second)
async def command_start(messege: types.Message, state: FSMContext):
    nic = messege.text
    available_usser = OBJECT.nick_to_share(messege.from_user.id)
    Nam.append(nic)
    if nic not in OBJECT.Nick.keys():
        await bot.send_message(messege.from_user.id, "Такого пользователя не существует",
                               reply_markup=kb.help_kb)
        Nam.clear()
        await state.finish()
    elif nic not in available_usser:
        await bot.send_message(messege.from_user.id, "Этот пользователь не хочет,"
                                                     " чтобы с ним делились заметками",
                               reply_markup=kb.help_kb)
        Nam.clear()
        await state.finish()
    else:
        OBJECT.sharing(Nam, OBJECT.Notes_of_Ussers[messege.from_user.id][Nam[0]])
        Nam.clear()
        await bot.send_message(messege.from_user.id, "Заметка успешно отправлена",
                               reply_markup=kb.help_kb)
        await state.finish()

if __name__ == '__main__':
    OBJECT = extract("pickledObjects.pkl")
    executor.start_polling(dp)
    save("pickledObjects.pkl", OBJECT)