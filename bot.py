from aiogram import executor
import config
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup
import logging

from googletrans import Translator
import googletrans

global lang

translator=Translator()

def translate_func(string,lang):
    return translator.translate(string, dest=str(lang))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start_message(message: types.Message):
    await message.answer("Привіт, я бот! 👋\nВведи - /help, щоб отримати список команд, які я вмію виконувати 📋")

@dp.message_handler(commands='help')
async def start_message(message: types.Message):
    await message.answer("Команди, які я вмію виконувати ⬇️\n/start - запуск/перезапуск бота 🔄\n/help - список команд 📋\n/translate - переклад на іншу мову ✏️")

@dp.message_handler(commands='translate')
async def start_message(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Polish 🇵🇱', 'French 🇫🇷', 'German 🇩🇪', 'Spanish 🇪🇸', 'Portuguese 🇵🇹', 'Italian 🇮🇹', 'Greek 🇬🇷', 'English 🇬🇧']
    keyboard.add(*buttons)
    await message.answer("Вибери на яку мову перекласти повідомлення", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text=='English 🇬🇧' or message.text=='French 🇫🇷' or
                    message.text=='German 🇩🇪' or message.text=='Spanish 🇪🇸' or message.text=='Portuguese 🇵🇹' or 
                    message.text=='Italian 🇮🇹' or message.text=='Greek 🇬🇷' or message.text=='Polish 🇵🇱')
async def dest_lang(message: types.Message):
    global lang
    languages={'Polish 🇵🇱':'pl','French 🇫🇷':'fr','German 🇩🇪':'de',
                'Spanish 🇪🇸':'es','Portuguese 🇵🇹':'pt','Italian 🇮🇹':'it',
                'Greek 🇬🇷':'el','English 🇬🇧':'en'}
    lang=languages[message.text]
    await message.reply('Який текст потрібно перевести?')

@dp.message_handler()
async def print_result(message:types.Message):
    global lang
    translated = translate_func(message.text,lang)
    await message.reply(translated.text)

if __name__ == '__main__':
    executor.start_polling(dp)