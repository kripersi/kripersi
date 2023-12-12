from aiogram import Bot, Dispatcher, executor, types
from gtts import gTTS
import os

API_TOKEN = '6732238493:AAFea5XHwhXI5t0FpxO3AUfPbebgU_TGRnk'

processing_request = False

bot = Bot(API_TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start', 'начать', 'START', 'go'])
async def start(message: types.Message):
    await message.answer('Привет! Я бот который отправляет голосовое сообщение с твоим текстом!\n '
                         'Скинь мне текст и увидишь результат\n'
                         'ТГ создателя: Marpexiz')


@dp.message_handler()
async def get_text_for_voice(message: types.Message):
    await message.answer('Ожидайте...')

    tts = gTTS(message.text)
    tts.save(f'{message.from_user.id}{message.text[0]}.mp3')

    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id + 1)
    await bot.send_audio(chat_id=message.from_user.id, audio=open(f'{message.from_user.id}{message.text[0]}.mp3', 'rb'), caption='Готово!')

    os.remove(f'{message.from_user.id}{message.text[0]}.mp3')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
