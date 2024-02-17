import telebot
from config import TELEGRAM_API_KEY
from extensions import *


bot = telebot.TeleBot(TELEGRAM_API_KEY)
app = ValueAPI(bot)  # Передаем экземпляр бота


@bot.message_handler(commands=['start'])
def handle_start(message):
    """ Send a message when the command /start is issued """
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}!\n"
                                      f"Я простенький бот, даже без кнопок, потому что не придумал зачем.\n"
                                      f"Чтобы узнать что я умею - вводи /help")


@bot.message_handler(commands=['help'])
def handle_help(message):
    """ Send a message when the command /help is issued """
    bot.send_message(message.chat.id, f"Основная моя задача показывать соотношение валют в заданном кол-ве!\n"
                                      f"Чтобы этим воспользоваться напиши мне:\n\n"
                                      f"*<имя валюты, цену которой хотим узнать>*\n"
                                      f"*<имя валюты, в которой надо узнать цену первой валюты>*\n"
                                      f"*<количество первой валюты>.*\n\n"
                                      f"Это всё должно быть в одной строке, через пробел и без лишнего. Пример:\n"
                                      f"*BTC RUB 1*\n"
                                      f"Т.е. сколько стоит 1 биткоин в рублях.\n"
                                      f"Чтобы узнать список доступных валют - введите /values\n\n"
                                      f"Еще я могу показывать последние новости, для этого введите\n"
                                      f"/news <кол-во выводимых новостей>", parse_mode="Markdown")


@bot.message_handler(commands=['values'])
def handle_help(message):
    """ Send a message when the command /values is issued """
    bot.send_message(message.chat.id, f"Вот список всех работающих сейчас валют:\n"
                                      f"*{[*app.values.keys()]}*\n"
                                      f"_Используйте только буквы без кавычек._", parse_mode="Markdown")


@bot.message_handler(commands=['news'])
def handle_help(message):
    """ Send a message when the command /values is issued """
    app.send_news(message)


@bot.message_handler(content_types=['voice'])
def handle_audio(message):
    """ Funny processing of voice messages """
    bot.send_photo(message.chat.id, 'https://ibb.co/zbzbT0R')


@bot.message_handler(content_types=['text'])
def handle_text(message):
    """ Main handler for the bot """
    print(message)
    res = app.get_price(message)
    bot.send_message(message.chat.id, res, parse_mode="Markdown")


if __name__ == '__main__':
    print('Bot starting')
    bot.polling(none_stop=True)
    print('Bot stopped')
