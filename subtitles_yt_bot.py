from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware

import os
from youtube_transcript_api import YouTubeTranscriptApi

API_TOKEN = 'YOUR TOKEN'

processing_request = False

bot = Bot(API_TOKEN)
dp = Dispatcher(bot=bot)

all_lang = ['af', 'ak', 'sq', 'am', 'ar', 'hy', 'as', 'ay', 'az', 'bn', 'eu', 'be', 'bh', 'bs', 'bg', 'my', 'ca',
            'ce', 'zh', 'zh', 'co', 'hr', 'cs', 'da', 'dv', 'nl', 'en', 'eo', 'et', 'ee', 'fi', 'fi', 'fr', 'gl',
            'lg', 'ka', 'de', 'el', 'gn', 'gu', 'ht', 'ha', 'ha', 'iw', 'hi', 'hm', 'hu', 'is', 'ig', 'id', 'ga',
            'it', 'ja', 'jv', 'kn', 'kk', 'km', 'rw', 'ko', 'kr', 'ku', 'ky', 'lo', 'la', 'lv', 'ln', 'lt', 'lb',
            'mk', 'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mn', 'ne', 'ns', 'no', 'ny', 'or', 'om', 'ps', 'fa', 'pl',
            'pt', 'pa', 'qu', 'ro', 'ru', 'sm', 'sa', 'gd', 'sr', 'sn', 'sd', 'si', 'sk', 'sl', 'so', 'st', 'es',
            'su', 'sw', 'sv', 'tg', 'ta', 'tt', 'te', 'th', 'ti', 'ts', 'tr', 'tk', 'uk', 'ur', 'ug', 'uz', 'vi',
            'cy', 'fy', 'xh', 'yi', 'yo', 'zu']


@dp.message_handler(commands=['start', 'начать', 'START', 'go'])
async def start(message: types.Message):
    await message.answer('Привет! Я бот который отправляет текстовый документ субтитров из видео ютуба.\n '
                         'Скинь мне ссылку на видео и я отправлю тебе файл с субтитрами\n'
                         'ТГ создателя: Marpexiz')


@dp.message_handler()
async def get_url(message: types.Message):
    global processing_request

    if processing_request:
        await message.reply("Другой запрос обрабатывается, подождите немного.")
        return

    processing_request = True
    await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)

    if message.text.startswith('https://www.youtube'):
        url = message.text[32:43].strip()  # получение id видео из ссылки
        srt = YouTubeTranscriptApi.get_transcript(url, languages=all_lang)  # извлекаем субтитры

        for txt in srt:
            with open(f'{message.from_user.id}{message.text[-1]}_downl.txt', 'a', encoding='UTF-8') as file:
                file.write(txt['text'] + ' ')

        await message.reply_document(open(f'{message.from_user.id}{message.text[-1]}_downl.txt', 'rb'),
                                     caption='Готово!')

        os.remove(f'{message.from_user.id}{message.text[-1]}_downl.txt')  # удаление файла с субтитрами
        processing_request = False

    elif message.text.startswith('https://youtu.be'):
        url = message.text.split('?si=')[0].split('.be/')[-1]  # получение id видео из ссылки
        srt = YouTubeTranscriptApi.get_transcript(url, languages=all_lang)  # извлекаем субтитры

        for txt in srt:
            with open(f'{message.from_user.id}{message.text[-1]}_downl.txt', 'a', encoding='UTF-8') as file:
                file.write(txt['text'] + ' ')

        await message.reply_document(open(f'{message.from_user.id}{message.text[-1]}_downl.txt', 'rb'),
                                     caption='Готово!')

        os.remove(f'{message.from_user.id}{message.text[-1]}_downl.txt')  # удаление файла с субтитрами
        processing_request = False

    else:
        await message.answer('Неверный формат ссылки!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
