from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import time

API_TOKEN = 'TOKEN'

text_game = ['🌕', '🌑', '🌑', '🌑', '🌑']

bot = Bot(API_TOKEN)
dp = Dispatcher(bot)

ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('left', callback_data='btn left')],
    [InlineKeyboardButton('right', callback_data='btn right')]
])


@dp.message_handler(commands=['game', 'start'])
async def start(message: types.Message):
    await message.answer(''.join(text_game), reply_markup=ikb)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('btn'))
async def ikb_query_close(callback: types.CallbackQuery):
    global text_game

    if callback.data == 'btn right' and text_game[-1] != '🌕':
        ind_1 = text_game.index('🌕')
        ind_2 = text_game.index('🌕') + 1

        text_game[ind_1] = '🌑'
        text_game[ind_2] = '🌕'

        await callback.message.edit_text(''.join(text_game), reply_markup=ikb)

    elif callback.data == 'btn left' and text_game[0] != '🌕':
        ind_1 = text_game.index('🌕')
        ind_2 = text_game.index('🌕') - 1

        text_game[ind_1] = '🌑'
        text_game[ind_2] = '🌕'

        await callback.message.edit_text(''.join(text_game), reply_markup=ikb)

    elif callback.data == 'btn right' and text_game[-1] == '🌕':
        text_game = ['🌕', '🌑', '🌑', '🌑', '🌑']

        await callback.message.edit_text(''.join(text_game), reply_markup=ikb)

    elif callback.data == 'btn left' and text_game[0] == '🌕':
        text_game = ['🌑', '🌑', '🌑', '🌑','🌕']

        await callback.message.edit_text(''.join(text_game), reply_markup=ikb)


if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True)
