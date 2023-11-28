from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text

API_TOKEN = '6732238493:AAFea5XHwhXI5t0FpxO3AUfPbebgU_TGRnk'

all_num = []

bot = Bot(API_TOKEN)
dp = Dispatcher(bot)

ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('сумма всех чисел', callback_data='btn sum'),
     InlineKeyboardButton('все числа', callback_data='btn all_num')],
     [InlineKeyboardButton('обновить счетчик', callback_data='btn restart'),
      InlineKeyboardButton('Удалить последнее число', callback_data='btn del')]
])

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f'Сумма всех чисел: {sum(all_num)}\nВсего за сегодня добавлено: {len(all_num)}',
                         reply_markup=ikb)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('btn'))
async def btn_func(callback: types.CallbackQuery):
    global all_num

    if callback.data == 'btn sum':
        await callback.message.edit_text(f'Сумма: {sum(all_num)}',
                             reply_markup=ikb)
    elif callback.data == 'btn all_num':
        await callback.message.edit_text(f'Все числа: {"  |  ".join(list(map(lambda x: str(x), all_num)))}',
                             reply_markup=ikb)
    elif callback.data == 'btn del':
        all_num = all_num[:-1]
        await callback.message.edit_text('Последнее число удалено!',
                             reply_markup=ikb)
    elif callback.data == 'btn restart':
        all_num = []
        await callback.message.edit_text(f'Обновленно!',
                             reply_markup=ikb)


@dp.message_handler()
async def add_num(message: types.Message):
    global all_num

    if message.text.isnumeric():
        all_num.append(int(message.text))
        await message.answer(f'Число {str(message.text)} добавленно\nСумма всех чисел: {sum(all_num)}',
                             reply_markup=ikb)
    else:
        await message.answer('Введите число!',
                             reply_markup=ikb)


if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True)
