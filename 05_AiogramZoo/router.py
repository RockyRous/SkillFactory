import time

from aiogram import Router, types, F
from aiogram.types import Message, InputMediaPhoto
from aiogram.filters import CommandStart
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest

import keyboards
from database import DataBase, questions, text_quiz, animal, start_message, logo, get_time
from config import DEBUG

db = DataBase()
router = Router()


#########################################################


@router.message(CommandStart())
async def command_start(message: Message) -> None:
    await message.answer_photo(caption=f"{start_message}", reply_markup=keyboards.start_keyboard(DEBUG),
                               photo=logo)
    if DEBUG:
        print(f'{get_time()} - {message.from_user.id} user use /start')
    # Создадим в бд экземпляр пользователя, если его там еще нет
    await db.update_user(message.from_user.id)


# В заморозке - Не работает клавиатура :/
# @router.callback_query(F.data == "get_desc")
# async def get_desc(callback: types.CallbackQuery):
#     """ Вывод описания """
#     await callback.message.edit_media(media=InputMediaPhoto(
#         media=logo,
#         caption="""
# Внимание! Смысловое содержание викторины было сгенерировано с помощью чатаГПТ, а не на анализе информации из сайта зоопарка.\n
# Прошу понять, что работа собиралась 2 дня после рабочего дня и я бы не успел сделать хорошую викторину.\n
# В остальном код был реализован с базой данных и имеет очень гибкую систему викторины, которую можно изменить под нужные вопросы.\n
# В качестве расширения можно перенести вопросы в бд или изменяемый файл и сделать админку, в которой будет интерфейс взаимодействия с вопросами через интерфейс телеграма.
# Считаю функционал сломать не получиться из интерфейса телеграма, остаётся только косметический ремонт.
# Хотел сделать код гибким, он такой и вышел, но в нем очень много зависимостей на мой взгляд :С
# Стек: Aiogram, aiosqlite
#         """,
#         reply_markup=keyboards.start_keyboard(DEBUG),
#     ))
#     await callback.answer()


@router.callback_query(F.data == "contact_zoo")
async def contact_zoo(callback: types.CallbackQuery):
    """ Связь с сотрудником зоопарка """
    await callback.answer(
        text="Можно сделать выбор из нескольких тем кнопками, и по нажатию - отправлять данные о юзере и тему для связи"
             " сотруднику или тп.",
        show_alert=True
    )
    if DEBUG:
        print(f'{get_time()} - user {callback.from_user.id} use contact_zoo')


@router.callback_query(F.data == "review")
async def review(callback: types.CallbackQuery):
    """ Отзывы """
    await callback.answer(
        text="Тут можно принимать сообщение от юзера и кому-нибудь его пересылать. "
             "А само сообщение сохранять в бд (функции для этого уже есть, см. в бд)",
        show_alert=True
    )
    if DEBUG:
        print(f'{get_time()} - {callback.from_user.id} user left a review')


@router.callback_query(F.data == "quiz_reset")
async def quiz_reset(callback: types.CallbackQuery):
    """ Рестарт викторины """
    await callback.message.edit_media(media=InputMediaPhoto(
        media=logo,
        caption=f"Вы точно уверены в этом? Это действие не отменить.", ),
        reply_markup=keyboards.quiz_reset(), )
    await callback.answer()
    if DEBUG:
        print(f'{get_time()} - user {callback.from_user.id} reset the quiz')


async def update_quiz_text(message: types.Message, data: dict):
    """ Модуль викторины. Обновляет диалог по викторине. """
    with suppress(TelegramBadRequest):
        exiting = False
        for i in range(1, 3):  # Определяем этап
            if not data['stages'][str(i)]['status']:

                len_quests = len(data['stages'][str(i)]['questions'])
                for j in range(1, len_quests + 1):  # Определяем вопрос
                    if not data['stages'][str(i)]['questions'][str(j)]['status']:
                        info_quest = f"{i}.{j}"  # Это номер этапа.вопроса для последующей записи ответа
                        await message.edit_media(media=InputMediaPhoto(
                            media=questions[i][j]['img'],
                            caption=f"{text_quiz}Вопрос {j} из {len_quests}:\n{questions[i][j]['question_text']}", ),
                            reply_markup=keyboards.quiz_keyboard(questions[i][j], info_quest), )
                        exiting = True
                        if exiting:
                            break
            if exiting:
                break
        if data['stages']['1']['status'] and data['stages']['2']['status']:  # Тут получается этапы закрыты
            if DEBUG:
                print(f'Пользователь {message.from_user.id} закрыл викторину [message]')
            data['quiz_status'] = True
            await db.update_user(message.from_user.id, data)
            await db.set_result(data, message.from_user.id)
            await message.edit_media(media=InputMediaPhoto(
                media='https://avatars.mds.yandex.net/get-images-cbir/2404260/7zAtfqPy2iVPrXi9S3Y8bg4626/ocr',
                caption=f"Викторина пройдена! получить результаты?", ),
                reply_markup=keyboards.quiz_finish(), )


@router.callback_query(F.data == "quiz_start")
async def quiz_start(callback: types.CallbackQuery):
    """ Старт викторины (и вывод результата) """
    data = await db.get_user_data(callback.from_user.id)
    if not data:
        await db.update_user(callback.from_user.id, 'new')
        data = await db.get_user_data(callback.from_user.id)

    if data['quiz_status']:
        if data['result'] == '':
            await db.set_result(data, callback.from_user.id)
            time.sleep(1)  # Возможно лишнее
            data = await db.get_user_data(callback.from_user.id)

        res = data['stages']['1']['result']
        table = [f'Группа {name} = {num} бал(а/ов)' for name, num in res.items()]
        table = '\n'.join(table)  # Таблица результатов
        data_name = data['result']  # имя\id животного ~ mammal_animal1
        animal_img = animal['img']  # Картинка животного (сейчас общая на всех)
        animal_name = animal[data_name.split('_')[0]][data_name]['name']  # Имя
        animal_text = animal[data_name.split('_')[0]][data_name]['text']  # Текст для животного
        await callback.message.edit_media(media=InputMediaPhoto(
            media=animal_img,
            caption=f"Викторина завершена! Ваши результаты:\n{table}\n\n"
                    f"И ваше животное: {animal_name}\n"
                    f"Описание: {animal_text}\n"
                    f"У каждого животного также должна быть индивидуальная картинка (функционал есть, но нет картинок)", ),
            reply_markup=keyboards.main_menu(), )
    else:
        await update_quiz_text(callback.message, data)
    await callback.answer()


@router.callback_query(F.data.startswith("quiz_"))
async def callbacks_update(callback: types.CallbackQuery):
    """ Главный обработчик ответов викторины. """
    data = await db.get_user_data(callback.from_user.id)
    info_quest = callback.data.split("_")[1].strip()
    answer = callback.data.split("_")[2].strip()
    if DEBUG:
        print(answer)

    if answer == 'menu':
        await callback.message.edit_media(media=InputMediaPhoto(
            media=logo,
            caption=f"{start_message}", ),
            reply_markup=keyboards.start_keyboard(), )

    if answer == 'delete':
        await db.update_user(callback.from_user.id, 'new')  # Вставляем пустую дату
        if DEBUG:
            print(f'Юзер {callback.from_user.id}, удалил свои ответы.')
        await callback.message.edit_media(media=InputMediaPhoto(
            media=logo,
            caption=f"{start_message}", ),
            reply_markup=keyboards.start_keyboard(), )

    if float(info_quest) > 0:  # Ответ касается вопросов викторины
        stage, quest = info_quest.split('.')
        if DEBUG:
            print(f"Пользователь {callback.from_user.id} ответил на вопрос {quest} в этапе {stage} [callback]")
        data['stages'][stage]['questions'][quest]['result'] = answer
        data['stages'][stage]['questions'][quest]['status'] = True
        await db.update_user(callback.from_user.id, data)

        exiting = False
        for i in range(1, 3):  # Определяем этап
            if not data['stages'][str(i)]['status']:
                len_quests = len(data['stages'][str(i)]['questions'])
                for j in range(1, len_quests + 1):  # Определяем вопрос
                    if not data['stages'][str(i)]['questions'][str(j)]['status']:
                        await update_quiz_text(callback.message, data)
                        exiting = True
                        if exiting:
                            break
                if exiting:
                    break
                else:
                    data['stages'][str(i)]['status'] = True
                    if DEBUG:
                        print(f'Пользователь {callback.from_user.id} закрыл этап {i} [callback]')
                    await db.update_user(callback.from_user.id, data)
        if data['stages']['1']['status'] and data['stages']['2']['status']:
            if DEBUG:
                print(f'Пользователь {callback.from_user.id} закрыл викторину [callback]')
            data['quiz_status'] = True
            await db.update_user(callback.from_user.id, data)
            await db.set_result(data, callback.from_user.id)
            await callback.message.edit_media(media=InputMediaPhoto(
                media='https://avatars.mds.yandex.net/get-images-cbir/2404260/7zAtfqPy2iVPrXi9S3Y8bg4626/ocr',
                caption=f"Викторина пройдена! получить результаты?", ),
                reply_markup=keyboards.quiz_finish(), )

    await callback.answer()


# DEBUG
@router.callback_query(F.data == 'get_data')
async def debug_get_data(callback: types.CallbackQuery):
    data = await db.get_user_data(callback.from_user.id)
    await callback.message.answer(f'{callback.from_user.id=}')
    await callback.message.answer(f'{data}')


@router.callback_query(F.data == 'get_result')
async def debug_get_result(callback: types.CallbackQuery):
    data = await db.get_user_data(callback.from_user.id)
    await callback.message.answer(f'{callback.from_user.id=}')
    await callback.message.answer(f"{data['result']=}\n{data['stages']['1']['result']=}")
