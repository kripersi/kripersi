from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text

API_TOKEN = 'TOKEN'

primer = '' # сюда будет записываться пример

bot = Bot(API_TOKEN)
dp = Dispatcher(bot)

# кнопки с цифрами и итерациями
ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('1', callback_data='btn 1'), InlineKeyboardButton('2', callback_data='btn 2'),
     InlineKeyboardButton('3', callback_data='btn 3'), InlineKeyboardButton('C', callback_data='iter C')],

    [InlineKeyboardButton('4', callback_data='btn 4'), InlineKeyboardButton('5', callback_data='btn 5'),
     InlineKeyboardButton('6', callback_data='btn 6'), InlineKeyboardButton('*', callback_data='iter *')],

    [InlineKeyboardButton('7', callback_data='btn 7'), InlineKeyboardButton('8', callback_data='btn 8'),
     InlineKeyboardButton('9', callback_data='btn 9'), InlineKeyboardButton(':', callback_data='iter /')],

    [InlineKeyboardButton('-', callback_data='iter -'), InlineKeyboardButton('0', callback_data='btn 0'),
     InlineKeyboardButton('+', callback_data='iter +'), InlineKeyboardButton('.', callback_data='iter .')],

    [InlineKeyboardButton('=', callback_data='iter =')]
])


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    '''начало программы, выводит пустой пример с кнопками'''
    global primer
    primer = ''

    await message.answer(f'Пример: {primer.rjust(20, " ") + "📍"}',
                         reply_markup=ikb)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('btn'))
async def start(callback: types.CallbackQuery):
    '''добавление цифр в пример'''
    global primer

    primer += str(callback.data)[-1]

    await callback.message.edit_text(f'Пример: {primer.ljust(20, " ") + "📍"}',
                         reply_markup=ikb)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('iter'))
async def start(callback: types.CallbackQuery):
    '''итерации (+-=*/)'''
    global primer

    if str(callback.data)[-1] == 'C':
        # удаление всех символов
        primer = ''

        await callback.message.edit_text(f'Пример: {primer.ljust(20, " ") + "📍"}',
                             reply_markup=ikb)

    elif str(callback.data)[-1] != '=':
        # проверяем нужно ли выводить ответ, в этом случае нет
        if len(primer) == 0 and callback.data[-1] == '-':
            # добавление в начало минус если длина примера равна нулю и выбранный символ это -
            primer = '-'

            await callback.message.edit_text(f'Пример: {primer.ljust(20, " ") + "📍"}',
                                                         reply_markup=ikb)

        elif len(primer) != 0:
            # если длина примера не равна нулю
            if primer[-1] not in '+-/*.':
                # если послдений символ не итерация до добавление в пример
                primer += str(callback.data)[-1]

                await callback.message.edit_text(f'Пример: {primer.ljust(20, " ") + "📍"}',
                                                     reply_markup=ikb)

            elif primer[-1] in '+/*.-' and len(primer) > 1:
                '''если же итерация то будет проверка равен ли 
                последний символ примера последнему символу вводимого числа, если нет то будет замена'''
                if primer[-1] != str(callback.data)[-1]:
                    primer = primer[:-1] + str(callback.data)[-1]
                    await callback.message.edit_text(f'Пример: {primer.ljust(20, " ") + "📍"}',
                                                         reply_markup=ikb)
            elif primer[-1] == '-' and len(primer) > 1:
                '''если же последний символ примера это минус и длина больше 1 то проверка
                 равен ли посдений символ примера вводимого числа и чтобы предпоследний символ был не итерацией'''
                if primer[-1] != str(callback.data)[-1] and primer[-2] not in '-+/*.':
                    primer = primer[:-1] + str(callback.data)[-1]

                    await callback.message.edit_text(f'Пример: {primer.ljust(20, " ") + "📍"}',
                                                         reply_markup=ikb)

    elif str(callback.data)[-1] == '=':
        try:
            await callback.message.edit_text(f'Ответ: {eval(primer).ljust(20, " ") + "📍"}',
                                 reply_markup=ikb)

            primer = str(eval(primer))
        except Exception:
            await callback.message.edit_text(f'Пример: "{primer}" невозможно решить!',
                                             reply_markup=ikb)

            primer = ''



if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True)

