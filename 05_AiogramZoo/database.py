import datetime
import random
import aiosqlite
import json
from aiogram.types import FSInputFile

from config import DEBUG


def get_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


data_example = {
    'quiz_status': False,  # Завершена викторина?
    'result': '',  # Имя животного (детали в animal)
    'stages': {
        1: {
            'status': False,  # Завершен этап?
            'result': '',  # Таблица с ответами
            'questions': {
                1: {
                    'status': False,  # Завершен вопрос?
                    'result': '',
                },
                2: {
                    'status': False,  # Завершен вопрос?
                    'result': '',
                },
                3: {
                    'status': False,  # Завершен вопрос?
                    'result': '',
                },
                4: {
                    'status': False,  # Завершен вопрос?
                    'result': '',
                },
                5: {
                    'status': False,  # Завершен вопрос?
                    'result': '',
                },
                6: {
                    'status': False,  # Завершен вопрос?
                    'result': '',
                },
                7: {
                    'status': False,  # Завершен вопрос?
                    'result': '',
                },
                8: {
                    'status': False,  # Завершен вопрос?
                    'result': '',
                },
                9: {
                    'status': False,  # Завершен вопрос?
                    'result': '',
                },
                10: {
                    'status': False,  # Завершен вопрос?
                    'result': '',
                },
                11: {
                    'status': False,  # Завершен вопрос?
                    'result': '',
                },
                12: {
                    'status': False,  # Завершен вопрос?
                    'result': '',
                },
                13: {
                    'status': False,  # Завершен вопрос?
                    'result': '',
                },
                14: {
                    'status': False,  # Завершен вопрос?
                    'result': '',
                },
                15: {
                    'status': False,  # Завершен вопрос?
                    'result': '',
                },
            },
        },
        2: {
            'status': False,
            'result': '',
            'questions': {
                1: {
                    'status': False,  # Завершен вопрос?
                    'result': '',
                },
                2: {
                    'status': False,  # Завершен вопрос?
                    'result': '',
                },
                3: {
                    'status': False,  # Завершен вопрос?
                    'result': '',
                },
                4: {
                    'status': False,  # Завершен вопрос?
                    'result': '',
                },
            },
        },
    },
},


class DataBase:
    def __init__(self):
        self.DATABASE_FILE = 'userdata.db'

    # Функция инициализации базы данных
    async def initialize_database(self):
        async with aiosqlite.connect(self.DATABASE_FILE) as db:
            await db.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, data TEXT)''')
            await db.execute('''CREATE TABLE IF NOT EXISTS review (id INTEGER PRIMARY KEY, time TEXT, data TEXT)''')
            await db.commit()

    # Функция получения данных пользователя по user_id
    async def get_user_data(self, user_id):
        async with aiosqlite.connect(self.DATABASE_FILE) as db:
            cursor = await db.execute("SELECT data FROM users WHERE user_id=?", (user_id,))
            row = await cursor.fetchone()
            if row:
                try:
                    return json.loads(row[0])[0]
                except (TypeError, KeyError):
                    return json.loads(row[0])
            else:
                return None

    # Функция обновления данных пользователя или добавления нового пользователя
    async def update_user(self, user_id, data=None):
        async with aiosqlite.connect(self.DATABASE_FILE) as db:
            if data == 'new':
                data = data_example
            cursor = await db.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
            existing_user = await cursor.fetchone()
            if existing_user:
                if data is not None:
                    await db.execute("UPDATE users SET data=? WHERE user_id=?", (json.dumps(data), user_id))
                else:
                    return None
            else:
                await db.execute("INSERT INTO users (user_id, data) VALUES (?, ?)", (user_id, json.dumps(data)))
            await db.commit()
        if DEBUG:
            print('Был совершен апдейт юзера: ', user_id)

    async def set_result(self, data, user_id) -> None:
        """ Если викторина пройдена - определяет животное. """
        if DEBUG:
            print('Start set result')
        if data['quiz_status']:
            if data['result'] == '':  # Если нет итогово животного
                if data['stages']['1']['result'] == '':  # Если нет таблицы 1го этапа - делаем ее
                    res = {}
                    stage = data['stages']['1']
                    for quest in stage['questions'].values():  # Парсинг результатов
                        for i in quest['result'].split(':'):
                            # i = ['mammal', '1']
                            if '+' in i:
                                name, num = i.split('+')
                                num = int(num)
                            elif '-' in i:
                                name, num = i.split('-')
                                num = -int(num)
                            if name in res:
                                res[name] = res[name] + num
                            else:
                                res[name] = num
                    data['stages']['1']['result'] = res  # Добавляем таблицу и комитим в бд
                    await self.update_user(user_id, data)
                    await self.set_result(data, user_id)  # Рекурсия
                else:
                    table = data['stages']['1']['result']
                    max_key = max(table, key=table.get)
                    pet = random.choice(list(animal[max_key].keys()))  # Получаю рандомного животного из категории
                    data['result'] = pet  # добавляю животного в бд
                    if DEBUG:
                        print('RESULT set_result: ' + pet)
                    await self.update_user(user_id, data)

    # DEBUG
    async def get_all_users(self):
        async with aiosqlite.connect(self.DATABASE_FILE) as db:
            cursor = await db.execute("SELECT * FROM users")
            rows = await cursor.fetchall()
            users = []
            for row in rows:
                user_id, data_json = row
                user_data = json.loads(data_json)
                users.append({"user_id": user_id, "data": user_data})
            return users

    # Функция получения всех данных из таблицы review
    async def get_review(self):
        async with aiosqlite.connect(self.DATABASE_FILE) as db:
            cursor = await db.execute("SELECT * FROM review")
            rows = await cursor.fetchall()
            return rows

    async def add_review(self, review_data):
        async with aiosqlite.connect(self.DATABASE_FILE) as db:
            review_time = get_time()
            await db.execute("INSERT INTO review (time, data) VALUES (?, ?)", (review_time, json.dumps(review_data)))
            await db.commit()


start_message = """
Стартовое сообщение! Сообщения удобно изменяются в файле database.py, включая вопросы викторины и содержание животных.
"""
logo = FSInputFile(f"logo.jpg")
text_quiz = 'Викторина\nТекст описание викторины.\n\n'
animal = {
    'img': 'https://sun9-30.userapi.com/impg/spZMSB9cZZicKjZwKqu5-U6kD6-priY87Y48Og/5iNNpPHusrg.jpg?size=1662x1486&quality=96&sign=bf6567b404cafb9c064e204bec3deca7&c_uniq_tag=hYWNbiHP_Wx-oql7PGDzNuQqlqNDfGjt1TwWvwmQ3tQ&type=album',
    'mammal': {
        'mammal_animal1': {
            'name': 'mammal_animal1',
            'text': 'text_mammal_animal1',
            'img': '',
        },
        'mammal_animal2': {
            'name': 'mammal_animal2',
            'text': 'text_mammal_animal2',
            'img': '',
        },
        'mammal_animal3': {
            'name': 'mammal_animal3',
            'text': 'text_mammal_animal3',
            'img': '',
        },
    },
    'bird': {
        'bird_animal4': {
            'name': 'bird_animal5',
            'text': 'text_bird_animal5',
            'img': '',
        },
        'bird_animal5': {
            'name': 'bird_animal5',
            'text': 'text_bird_animal5',
            'img': '',
        },
        'bird_animal6': {
            'name': 'bird_animal6',
            'text': 'text_bird_animal6',
            'img': '',
        },
    },
    'invertebrates': {
        'invertebrates_animal7': {
            'name': 'invertebrates_animal7',
            'text': 'text_invertebrates_animal7',
            'img': '',
        },
        'invertebrates_animal8': {
            'name': 'invertebrates_animal8',
            'text': 'text_invertebrates_animal8',
            'img': '',
        },
        'invertebrates_animal9': {
            'name': 'invertebrates_animal9',
            'text': 'text_invertebrates_animal9',
            'img': '',
        },
    },
    'reptile': {
        'reptile_animal10': {
            'name': 'reptile_animal10',
            'text': 'text_reptile_animal10',
            'img': '',
        },
        'reptile_animal11': {
            'name': 'reptile_animal11',
            'text': 'text_reptile_animal11',
            'img': '',
        },
        'reptile_animal12': {
            'name': 'reptile_animal12',
            'text': 'text_reptile_animal12',
            'img': '',
        },
    },
    'fish': {
        'fish_animal13': {
            'name': 'fish_animal13',
            'text': 'text_fish_animal13',
            'img': '',
        },
        'fish_animal14': {
            'name': 'fish_animal14',
            'text': 'text_fish_animal14',
            'img': '',
        },
        'fish_animal15': {
            'name': 'fish_animal15',
            'text': 'text_fish_animal15',
            'img': '',
        },
    },
    'amphibian': {
        'amphibian_animal16': {
            'name': 'amphibian_animal16',
            'text': 'text_amphibian_animal16',
            'img': '',
        },
        'amphibian_animal17': {
            'name': 'amphibian_animal17',
            'text': 'amphibian_animal17',
            'img': '',
        },
        'amphibian_animal18': {
            'name': 'amphibian_animal18',
            'text': 'amphibian_animal18',
            'img': '',
        },
    },
}
questions = {
    1: {
        1: {
            'img': 'https://avatars.mds.yandex.net/get-images-cbir/2404260/7zAtfqPy2iVPrXi9S3Y8bg4626/ocr',
            'question_text': '🗺️Какой тип среды обитания предпочитаете вы?',
            'answers': {
                1: {
                    'text': '🪵 Леса и поля',
                    'result': 'mammal+1:bird+2:invertebrates-1'
                },
                2: {
                    'text': '🪨 Горы и скалы',
                    'result': 'mammal+1:reptile+2:fish-1'
                },
                3: {
                    'text': '💧Водные пространства',
                    'result': 'mammal-1:fish+2:amphibian+1'
                },
            },
        },
        2: {
            'img': 'https://cdn.fishki.net/upload/users/2022/06/12/1782919/c4eaec1713428c400c2a8e09003fa23d.jpg',
            'question_text': 'Какую погоду вы предпочитаете?',
            'answers': {
                1: {
                    'text': '🌞Тепло и солнечно',
                    'result': 'amphibian-1:bird+2:fish-1'
                },
                2: {
                    'text': '❄️Прохладно и влажно',
                    'result': 'mammal+1:reptile-1:invertebrates+2'
                },
            },
        },
        3: {
            'img': 'https://shlyahta.com.ua/wp-content/uploads/snimok-ekrana-2021-06-03-v-14-42-29.png',
            'question_text': 'Что вы цените больше всего в животных?',
            'answers': {
                1: {
                    'text': '🤓Их интеллект и социальные связи',
                    'result': 'mammal+2:bird+1:invertebrates-1'
                },
                2: {
                    'text': '😎Их красоту и изящество',
                    'result': 'bird+2:fish+1:reptile-1'
                },
            },
        },
        4: {
            'img': 'https://www.meme-arsenal.com/memes/bd88585c48d3849491438ca3ec11a8a8.jpg',
            'question_text': 'Какой тип движения в воде вам ближе?',
            'answers': {
                1: {
                    'text': '🫳Плавание',
                    'result': 'fish+2:amphibian+1:mammal-1'
                },
                2: {
                    'text': '🫴Подводное скольжение',
                    'result': 'invertebrates-2:fish+1:reptile+1'
                },
            },
        },
        5: {
            'img': 'https://img.joinfo.com/i/2018/03/800x0/5aab9fbc66ec9.jpg',
            'question_text': 'Какое время суток вы предпочитаете для активности?',
            'answers': {
                1: {
                    'text': '🌝Дневное',
                    'result': 'bird+2:mammal+1:reptile-1'
                },
                2: {
                    'text': '🌚Ночное',
                    'result': 'reptile+2:invertebrates+1:bird-1'
                },
            },
        },
        6: {
            'img': 'https://blog.performars.com/hs-fs/hubfs/Illustration%202_Source_XPLANE%20Corporate%20Innovation%20Ecosystem.png?width=1600&name=Illustration%202_Source_XPLANE%20Corporate%20Innovation%20Ecosystem.png',
            'question_text': 'Какая экосистема вам больше нравится?',
            'answers': {
                1: {
                    'text': '🏖️Тропические леса',
                    'result': 'bird+2:mammal+2:reptile-1'
                },
                2: {
                    'text': '🏜️Пустыни и степи',
                    'result': 'reptile+2:invertebrates+1:mammal-1'
                },
            },
        },
        7: {
            'img': 'https://avatars.mds.yandex.net/get-images-cbir/4120691/GsuS7BdpxgVYzmPyCMwSlg4318/ocr',
            'question_text': '🌍Какая часть природы вас больше привлекает?',
            'answers': {
                1: {
                    'text': '☁️Воздушное пространство',
                    'result': 'bird+2:invertebrates-1:reptile+1'
                },
                2: {
                    'text': '🗻Подземный мир',
                    'result': 'invertebrates+2:amphibian+1:bird-1'
                },
            },
        },
        8: {
            'img': 'https://sun1-23.userapi.com/impg/x1OTBOtngxwSZ4PIjRN71Gncln3xo81h9iY53g/-_FYT8k6mdQ.jpg?size=811x530&quality=96&sign=1ee40cc4a3f1cd84143d2cc7bea08b2e&c_uniq_tag=k4It0jK6K8LblgWGTmXPGBBKlneq46uJVq7-232nn04&type=album',
            'question_text': '🍝Какой тип пищи вы предпочитаете?',
            'answers': {
                1: {
                    'text': '🥦Растительная',
                    'result': 'bird+1:mammal+1:reptile-2'
                },
                2: {
                    'text': '🍗Мясная',
                    'result': 'mammal+2:reptile+1:amphibian-1'
                },
            },
        },
        9: {
            'img': 'https://kartinkof.club/uploads/posts/2022-03/1648289844_1-kartinkof-club-p-komnata-zhenikha-mem-2.jpg',
            'question_text': 'Что важнее для вас в среде обитания?',
            'answers': {
                1: {
                    'text': '🌊Наличие воды',
                    'result': 'fish+2:amphibian+1:bird+1'
                },
                2: {
                    'text': '🏝️Богатство растительности',
                    'result': 'mammal+1:reptile-2:bird+1'
                },
            },
        },
        10: {
            'img': 'https://avatars.mds.yandex.net/get-images-cbir/994836/RXxb5EnuiaAc8g9ppfjYxg4179/ocr',
            'question_text': 'Какой аспект поведения животных вам интереснее?',
            'answers': {
                1: {
                    'text': '🤺Стратегии охоты и питания',
                    'result': 'mammal+2:fish+1:invertebrates-1'
                },
                2: {
                    'text': '👨‍👩‍👧‍👦Социальное взаимодействие и иерархия в стае',
                    'result': 'mammal+1:amphibian-1:bird+1'
                },
            },
        },
        11: {
            'img': 'https://pic.rutubelist.ru/video/fa/53/fa5372439fc875a463fd4b98811761a7.jpg',
            'question_text': 'Что важнее в выборе места для обитания?',
            'answers': {
                1: {
                    'text': '🛖Укрытия и места для скрытности',
                    'result': 'reptile+2:bird-1:invertebrates+1'
                },
                2: {
                    'text': '🍗Доступ к пище и воде',
                    'result': 'fish+2:amphibian+1:mammal+1'
                },
            },
        },
        12: {
            'img': 'https://avatars.mds.yandex.net/get-mpic/4080763/img_id1828394638027319486.jpeg/orig',
            'question_text': 'Какое поведение во время опасности вам ближе?',
            'answers': {
                1: {
                    'text': '🚴Быстрый бег или полет на безопасное расстояние.',
                    'result': 'mammal+1:bird+2:invertebrates-1'
                },
                2: {
                    'text': '🥷Маскировка или защитные механизмы.',
                    'result': 'reptile+2:invertebrates+1:amphibian-1'
                },
            },
        },
        13: {
            'img': 'https://avatars.mds.yandex.net/get-images-cbir/2162455/Cq8Im3nqw42ifX0idfNdwg4023/ocr',
            'question_text': 'Какой тип связи между особями вам интереснее?',
            'answers': {
                1: {
                    'text': '🧖‍♀️Партнерство на всю жизнь.',
                    'result': 'mammal+2:bird+1:fish-1'
                },
                2: {
                    'text': '🧖‍♂️Периодические или сезонные встречи.',
                    'result': 'bird+2:fish+1:reptile-1'
                },
            },
        },
        14: {
            'img': 'https://cdn6.aptoide.com/imgs/1/c/a/1ca441abbb3d07fdd56b3be1d6627c09_fgraphic.jpg',
            'question_text': 'Какие звуки в природе вы цените больше всего?',
            'answers': {
                1: {
                    'text': '🎸Пение птиц.',
                    'result': 'mammal+1:bird+2:fish-1'
                },
                2: {
                    'text': '🎺Шелест листвы и звуки леса.',
                    'result': 'mammal+1:invertebrates-1:reptile+1'
                },
            },
        },
        15: {
            'img': 'https://kz-russia.ru/wp-content/uploads/5/2/d/52da88a578877bd95947283a235a7055.jpeg',
            'question_text': 'Какая степень независимости в выборе жизненных партнеров вам ближе?',
            'answers': {
                1: {
                    'text': '💵Выбор основывается на собственных предпочтениях',
                    'result': 'mammal+2:bird+1:reptile-1'
                },
                2: {
                    'text': '🔨Выбор зависит от внешних факторов и условий среды',
                    'result': 'fish+2:invertebrates-1:amphibian+1'
                },
            },
        },
    },
    2: {
        1: {
            'img': 'https://sneg.top/uploads/posts/2023-04/1682407286_sneg-top-p-pustie-karmani-kartinki-krasivo-48.jpg',
            'question_text': 'Тут должны были быть вопросы для определения отряда животных, но на это у меня не хватает'
                             'времени :С\nДальше будут вопросы не влияющие на результат викторины, но повлияют на вашу карму.',
            'answers': {
                1: {
                    'text': 'Ладно',
                    'result': ''
                },
            },
        },
        2: {
            'img': 'https://sun9-16.userapi.com/mGmLJJyhDnTP5o-NZVVr9UOGt9uQRFi7R4YrwA/szpc9p8pU9Y.jpg',
            'question_text': 'Вы любите животных?',
            'answers': {
                1: {
                    'text': 'Да',
                    'result': ''
                },
                2: {
                    'text': 'Нет',
                    'result': ''
                },
            },
        },
        3: {
            'img': 'https://sun9-63.userapi.com/impg/By0735Fy16FPw64sY_zWC4jLnGdR_sanDRzv-A/m3vq6_x_8Tc.jpg?size=1280x720&quality=95&sign=07535a0d07301982bc82146a62346f2c&c_uniq_tag=0oJqJtaOEtY2LxVKqXtcQAk_WXJ2fK4eD5D4GO5uDGk&type=album',
            'question_text': 'Вам понравился мой бот?',
            'answers': {
                1: {
                    'text': 'Да',
                    'result': ''
                },
                2: {
                    'text': 'Очень сильно',
                    'result': ''
                },
            },
        },
        4: {
            'img': 'https://www.passionforum.ru/upload/313/u31371/b/b/bbe11ed7.jpg',
            'question_text': 'Вы поставите мне высший бал за эту прекрасную работу?',
            'answers': {
                1: {
                    'text': 'Да',
                    'result': ''
                },
                2: {
                    'text': '11/10',
                    'result': ''
                },
                3: {
                    'text': 'Ладно',
                    'result': ''
                },
            },
        },
    },
}

