from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
import random

API_TOKEN = '6732238493:AAFea5XHwhXI5t0FpxO3AUfPbebgU_TGRnk'

num = 0

bot = Bot(API_TOKEN)
dp = Dispatcher(bot)

ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('plus', callback_data='1 app'), InlineKeyboardButton('minus', callback_data='1 min')],
    [InlineKeyboardButton('random', callback_data='1 random')]
])


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    global num
    num = 0

    await message.answer(f'текущее число {num}',
                         reply_markup=ikb)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('1')) #  определенная клава
async def start(callback: types.CallbackQuery):
    global num

    if callback.data == '1 app':
        num += 1
        await callback.message.edit_text(f'текущее число {num}',
                                         reply_markup=ikb)
    elif callback.data == '1 min':
        num -= 1
        await callback.message.edit_text(f'текущее число {num}',
                                         reply_markup=ikb)
    elif callback.data == '1 random':
        num = random.randint(1,60)
        await callback.message.edit_text(f'текущее число {num}',
                                         reply_markup=ikb)


if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True)
