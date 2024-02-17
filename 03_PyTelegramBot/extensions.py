import requests


class APIException(Exception):
    def __init__(self, bot, message, text: str) -> None:
        super().__init__(text)
        print('Send error message to telegram. Error:')
        print(text)
        bot.send_message(message.chat.id, f'Error: {text}')


def error_catcher(fn):
    """ Декоратор для отлова ошибок """
    def wrapper(*args, **kwargs):
        try:
            result = fn(*args, **kwargs)
        except APIException as Error:
            pass
        else:
            return result
    return wrapper


class ValueAPI:
    def __init__(self, bot):
        self.api_url = 'https://min-api.cryptocompare.com/data/price?'
        self.bot = bot
        self.values = {
            'BTC': 'BTC',
            'ETH': 'ETH',
            'USDT': 'USDT',
            'USDC': 'USDC',
            'BNB': 'BNB',
            'USD': 'USD',
            'RUB': 'RUB',
            'EUR': 'EUR',
            'XMR': 'XMR',
            'ZEC': 'ZEC',
            'REP': 'REP',
        }

    def request_validation(self, message):
        """ :return base, quote and amount from text """
        text = message.text.split(' ')
        if len(text) == 3:
            if text[0] != text[1]:
                try:
                    amount = float(text[2])
                except:
                    raise APIException(self.bot, message, 'Вы ввели не корректное кол-во!')
                else:
                    try:
                        a = self.values[text[0]]
                    except:
                        raise APIException(self.bot, message, f'Не получилось распознать валюту {text[0]}')
                    try:
                        a = self.values[text[1]]
                    except:
                        raise APIException(self.bot, message, f'Не получилось распознать валюту {text[1]}')
                    else:

                        return text

            else:
                raise APIException(self.bot, message, 'Вы ввели одинаковые валюты!')
        else:
            raise APIException(self.bot, message, 'Вы ввели не верное кол-во параметров!')

    @error_catcher
    def get_price(self, message):
        """ desc """
        base, quote, amount = self.request_validation(message)
        res = requests.get(f'{self.api_url}fsym={base}&tsyms={quote}').json()
        result = float(res[quote]) * float(amount)
        text = (f'Ценна 1 {base} = {res[quote]} {quote}.\n'
                f'{amount} {base} = *{result}* {quote}')
        return text

    @staticmethod
    def last_news():
        """ return 5 last news post """
        res = requests.get(f'https://min-api.cryptocompare.com/data/v2/news/?feeds=cryptocompare,cointelegraph,coindesk&extraParams=YourSite').json()
        return res

    def send_news(self, message):
        """ Cycle send news """
        news = self.last_news()
        try:
            text = message.text.split(' ')
            num = int(text[1])
        except:
            num = 5
        finally:
            for i in range(0, num):
                self.bot.send_message(message.chat.id, f"Заголовок: {news['Data'][i]['title']}\n"
                                                       f"Читать больше: {news['Data'][i]['url']}")
