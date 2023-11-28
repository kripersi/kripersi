import requests
import os
import io
from PIL import Image, ImageFilter
from random import choice

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext

settings_img = ReplyKeyboardMarkup(resize_keyboard=True)
settings_img.add('BLUR').add('CONTOUR').add('DETAIL').add('MedianFilter').add('/cancel')

rkb = ReplyKeyboardMarkup(resize_keyboard=True)
rkb.add(KeyboardButton('начать изменять фотку'))

rkb2 = ReplyKeyboardMarkup(resize_keyboard=True)
rkb2.add(KeyboardButton('/cancel'))

ses_set = ''

class ClientStatesGroup(StatesGroup):

    desc = State()
    settings_img_cl = State()
    photo = State()


API_TOKEN = '6732238493:AAFea5XHwhXI5t0FpxO3AUfPbebgU_TGRnk'

storage = MemoryStorage()
bot = Bot(API_TOKEN)
dp = Dispatcher(bot=bot,
                storage=storage)

URI = f'https://api.telegram.org/bot{API_TOKEN}/getFile?file_id='
URI2 = f'https://api.telegram.org/file/bot{API_TOKEN}/'


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    global ses_set
    ses_set = ''
    await message.answer('start',
                         reply_markup=rkb)


@dp.message_handler(commands=['cancel'], state='*')
async def start(message: types.Message, state: FSMContext):
    global ses_set

    current_state = await state.get_state()

    if current_state is None:
        return

    await message.reply('отменили',
                        reply_markup=rkb)
    ses_set = ''
    await state.finish()


@dp.message_handler(Text(equals='начать изменять фотку', ignore_case=True), state=None) #  ignore_case - ignore регистер
async def start_job(message: types.Message):
    await ClientStatesGroup.desc.set()
    await message.answer('отправьте пожалуйста описание',
                         reply_markup=rkb2)


@dp.message_handler(state=ClientStatesGroup.desc)
async def load_photo(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text

    await ClientStatesGroup.next()
    await message.reply('описание сохранено\nотправьте как изменить фотку', reply_markup=settings_img)


@dp.message_handler(state=ClientStatesGroup.settings_img_cl)
async def load_photo(message: types.Message, state=FSMContext):
    global ses_set

    if message.text in ['BLUR', 'CONTOUR', 'DETAIL', 'MedianFilter']:
        async with state.proxy() as data:
            data['settings_img_cl'] = {
            'BLUR': ImageFilter.BLUR,
            'CONTOUR': ImageFilter.CONTOUR,
            'DETAIL': ImageFilter.DETAIL,
            'MedianFilter': ImageFilter.MedianFilter
        }[message.text]

        ses_set = {
            'BLUR': ImageFilter.BLUR,
            'CONTOUR': ImageFilter.CONTOUR,
            'DETAIL': ImageFilter.DETAIL,
            'MedianFilter': ImageFilter.MedianFilter
        }[message.text]

        await ClientStatesGroup.next()
        await message.reply('отправьте фотку', reply_markup=rkb2)


#if not photo
@dp.message_handler(lambda message: not message.photo, state=ClientStatesGroup.photo)
async def check_photo(message: types.Message):
    return await message.reply('This is not photo!', reply_markup=rkb2)

# elif photo
@dp.message_handler(lambda message: message.photo, content_types=['photo'], state=ClientStatesGroup.photo)
async def load_photo(message: types.Message, state=FSMContext):
    global ses_set

    await message.reply('ждите pls')

    for_name = 'qwertyujwenfakscbzxcvbnmjhgfds'

    file_id = message.photo[3].file_id
    URI_info = URI + file_id
    responce = requests.get(URI_info).json()['result']['file_path']

    image = requests.get(URI2 + responce).content
    img = Image.open(io.BytesIO(image))
    img = img.filter(ses_set)

    if not os.path.exists('static'):
        os.mkdir('static')

    img_name = choice(for_name) + choice(for_name) + choice(for_name) + choice(for_name)
    img.save(f'static/{img_name}.png', format='PNG')

    async with state.proxy() as data:
        data['photo'] = img_name

    await message.answer_photo(photo=open(f'static/{img_name}.png', 'rb'),
                               caption=data['desc'])
    os.remove(f'static/{img_name}.png')
    ses_set = ''
    await state.finish()


@dp.message_handler()
async def no_command(message: types.Message):
    await message.answer('Нету такой комманды')

if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True)
