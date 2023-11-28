# bot
import telebot
from telebot import types
# scraping
import requests
from bs4 import BeautifulSoup
# oth.
import re

bot = telebot.TeleBot('TOKEN')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     f'Привет <b>{message.from_user.first_name}</b>, я бот Wikipedia, напиши мне запрос и я cкину текст из статьи в Wikipedia\nПримеры: Беларусь, Английский, Наполеон I, Computer',
                     parse_mode='html')


@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id, 'Бот берет материал из сайта wikipedia.org\n'
                                      'Если нашли ошибку пишите tg: Marpexiz\n'
                                      'Примеры запросов: Python, собака, имя, дерево')


@bot.message_handler(commands=['developer'])
def developer_info(message):
    bot.send_message(message.chat.id, 'Рад что ты спросил! Создатель этого бота Артём, tg: Marpexiz \n t.me/Marpexiz')


@bot.message_handler(func=lambda x: True)
def wikipedia_pars(message):
    if len(message.text.lower()) > 30:
        bot.send_message(message.chat.id, 'Слишком длинный запрос, попробуйте снова')

    bot.send_message(message.chat.id, 'Подождите... \n')

    link = 'https://ru.wikipedia.org/wiki/' + str(message.text)
    s = ''

    try:
        responce = requests.get(link).text
        soup = BeautifulSoup(responce, 'lxml')

        block = soup.find('div', id="content")
        info = block.find_all('span')[0].text

        block2 = soup.find('div', class_="mw-parser-output")
        info = block.find_all('p')

        for info_blocks in info:
            if len(info_blocks.text.strip()) < 4000 and len(s + info_blocks.text.strip()) < 4000:
                s += info_blocks.text.strip() + '\n'
            else:
                break

        end_text = re.sub(r'\[\d+\]', '', s.replace('[⇨]', ''))
        mes_user = bot.send_message(message.chat.id,
                                    f'{end_text}\nСимволов <u>{len(end_text)}</u>\n         <b>Материал взят из <u>wikipedia</u>.</b>',
                                    parse_mode='html')
        bot.delete_message(message.chat.id, mes_user.id - 1)
    except:
        bot.send_message(message.chat.id, 'Извините произошла ошибка! Попробуйте снова. Вероятные ошибки: ваш текст '
                                          'слишком длинный, бот не распознал текст, ошибки в самом боте. О проблемах '
                                          'писать tg: Marpexiz')

    bot.send_message(5381172828, f'{message.from_user}  завикипедил \n\n\n'
                                 f'{message.text}')


bot.polling(none_stop=True)
