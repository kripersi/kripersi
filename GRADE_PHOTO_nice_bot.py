# scraping
import requests
from bs4 import BeautifulSoup
# tg bot
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

link = 'https://zastavok.net/eda/'

header = {'user-agent': 'random_people'}
all_image = []
name_image = []

for page in range(1, 5): # scraping 4 pages
    responce = requests.get(link + f'/{page}/', headers=header).text
    block = BeautifulSoup(responce, 'lxml')

    all_image_block = block.find('div', class_='block-photo').find_all('div', class_='short_full')

    for i in all_image_block: # get url and name of the image
        all_image.append('https://zastavok.net' + i.find('img').get('src'))
        name_image.append(i.find('img').get('alt'))

'''There is Telegram(aiogram) code in the down part code'''

ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('<-', callback_data='btn left-'), InlineKeyboardButton('->', callback_data='btn right+')],
    [InlineKeyboardButton('❤️', callback_data='btn like')]
])

ikb_no_like = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('<-', callback_data='btn left-'), InlineKeyboardButton('->', callback_data='btn right+')]
])


API_TOKEN = 'YOUR TOKEN'

count_img = 0 # external picture counter

bot = Bot(API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    '''send first image with keyboard'''
    await bot.send_photo(chat_id=message.from_user.id,
                         photo=all_image[0],
                         reply_markup=ikb)


@dp.message_handler(commands=['creator'])
async def start(message: types.Message):
    await message.answer('TG: Marpexiz\nINST: Kripersi_it')


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('btn'))
async def get_grade(callback: types.CallbackQuery):
    '''processing button clicks'''
    global count_img

    if callback.data != 'btn like':
        count_img = eval(f'count_img{callback.data[-1]}1') # get last element and insert it

        await bot.edit_message_media(chat_id=callback.message.chat.id,
                                         message_id=callback.message.message_id,
                                         media=InputMediaPhoto(media=all_image[count_img],
                                                               caption=name_image[count_img]),
                                         reply_markup=ikb)

    elif callback.data == 'btn like':
        if 'liked' not in name_image[count_img]:
            name_image[count_img] = str(name_image[count_img]) + ' liked ❤️'

            await bot.edit_message_media(chat_id=callback.message.chat.id,
                                         message_id=callback.message.message_id,
                                         media=InputMediaPhoto(media=all_image[count_img],
                                                               caption=name_image[count_img]),
                                         reply_markup=ikb_no_like)
        else:
            await bot.edit_message_media(chat_id=callback.message.chat.id,
                                         message_id=callback.message.message_id,
                                         media=InputMediaPhoto(media=all_image[count_img],
                                                               caption='You have already liked!😡'),
                                         reply_markup=ikb_no_like)


if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True)
