from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

rkp = ReplyKeyboardMarkup(resize_keyboard=True)
rkp.add(KeyboardButton('начать'))

rkp2 = ReplyKeyboardMarkup(resize_keyboard=True)
rkp2.add(KeyboardButton('/cancel'))


class ClientStatesGroup(StatesGroup):

    photo = State()
    desc = State()


API_TOKEN = 'TOKEN'

storage = MemoryStorage()
bot = Bot(API_TOKEN)
dp = Dispatcher(bot=bot,
                storage=storage)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('start',
                         reply_markup=rkp)


@dp.message_handler(commands=['cancel'], state='*')
async def start(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state is None:
        return

    await message.reply('отменили',
                        reply_markup=rkp)
    await state.finish()


@dp.message_handler(Text(equals='начать', ignore_case=True), state=None) #  ignore_case - ignore регистер
async def start_job(message: types.Message):
    await ClientStatesGroup.photo.set()
    await message.answer('отправьте пожалуйста фотку',
                         reply_markup=rkp2)


@dp.message_handler(lambda message: not message.photo, state=ClientStatesGroup.photo)
async def check_photo(message: types.Message):
    return await message.reply('This is not photo!')


@dp.message_handler(lambda message: message.photo, content_types=['photo'], state=ClientStatesGroup.photo)
async def load_photo(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id

    await ClientStatesGroup.next() # изменение состояния
    await message.reply('А теперь отправьте описание')


@dp.message_handler(state=ClientStatesGroup.desc)
async def load_photo(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text

    await message.reply('описание сохранено')

    async with state.proxy() as data2:
        await bot.send_photo(chat_id=message.from_user.id,
                             photo=data2['photo'],
                             caption=data2['desc'])

    await state.finish()  # изменение состояния в конце!


if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True)
