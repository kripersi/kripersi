import random

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext


settings_img = ReplyKeyboardMarkup(resize_keyboard=True)
settings_img.add('1').add('2').add('3').add('/cancel')

settings_img3 = ReplyKeyboardMarkup(resize_keyboard=True)
settings_img3.add('начать угадывать число')

API_TOKEN = '6732238493:AAFea5XHwhXI5t0FpxO3AUfPbebgU_TGRnk'

storage = MemoryStorage()
bot = Bot(API_TOKEN)
dp = Dispatcher(bot=bot,
                storage=storage)

num = ''

class ClientStatesGroup(StatesGroup):

    first = State()
    second = State()
    third = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    global num

    num = str(random.randint(1, 3)) + str(random.randint(1, 3))
    await message.answer('хочешь начать угадывать число?', reply_markup=settings_img3)


@dp.message_handler(commands=['cancel'], state='*')
async def cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state is None:
        return

    await message.reply('отменили',
                        reply_markup=rkb)

    num = ''
    await state.finish()


@dp.message_handler(Text(equals='начать угадывать число', ignore_case=True), state=None)
async def start_job(message: types.Message):
    await ClientStatesGroup.first.set()
    await message.answer('отправьте пожалуйста цифру',
                         reply_markup=settings_img)


@dp.message_handler(state=ClientStatesGroup.first)
async def load_num1(message: types.Message, state=FSMContext):
    if str(message.text)[0] == str(num)[0]:
        async with state.proxy() as data:
            data['first'] = message.text

        await ClientStatesGroup.next()
        await message.reply('Верно!\nвведите вторую цифру', reply_markup=settings_img)
    else:
        await message.reply('Неверно, попытайтесь еще', reply_markup=settings_img)


@dp.message_handler(state=ClientStatesGroup.second)
async def load_num2(message: types.Message, state=FSMContext):
    if str(message.text)[0] == str(num)[1]:
        async with state.proxy() as data:
            data['second'] = message.text

        await message.reply('<b>WIN</b>', parse_mode='html', reply_markup=settings_img3)
        await state.finish()  # изменение состояния в конце!
    else:
        await message.reply('Неверно, попытайтесь еще', reply_markup=settings_img)


@dp.message_handler()
async def no_command(message: types.Message):
    await message.answer('Нету такой комманды')


if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True)
