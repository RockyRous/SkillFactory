import asyncio
import aiohttp
from random import sample
from googletrans import Translator

from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, types, F
from aiogram.utils.keyboard import ReplyKeyboardBuilder

router = Router()
translator = Translator()


class FakeDatabase(StatesGroup):
    waiting_for_num = State()
    waiting_for_id = State()


async def get_url_json(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as resp:
            data = await resp.json()
            return data


@router.message(Command("category_search_random"))
async def category_search_random(message: Message, command: CommandObject, state: FSMContext):
    """ Получение команды с кол-вом выводимых ответов и формирование дальнейшей логики. """
    if command.args is None:
        await message.answer("Ошибка: не переданы аргументы. Укажите кол-во рецептов (цифрой).")
        return
    try:
        recipes_num = int(command.args)
    except ValueError:
        await message.answer("Ошибка: передана не цифра. Укажите кол-во рецептов (цифрой).")
        return

    await state.set_data({'recipes_num': recipes_num})  # Записываем число рецептов
    data = await get_url_json('https://www.themealdb.com/api/json/v1/1/list.php?c=list')

    # Кнопки
    builder = ReplyKeyboardBuilder()
    for meals in data['meals']:
        builder.add(types.KeyboardButton(text=list(meals.values())[0]))
    builder.adjust(5)

    await message.answer(
        f"Выберите категорию:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )

    await state.set_state(FakeDatabase.waiting_for_num.state)


@router.message(FakeDatabase.waiting_for_num)
async def recipes_by_category(message: types.Message, state: FSMContext):
    """ Получение данных по выбранной категории. Продолжение логики. """
    try:
        data = await state.get_data()  # Получаем ранее записанные данные
        num = data['recipes_num']

        resp = await get_url_json(f'https://www.themealdb.com/api/json/v1/1/filter.php?c={message.text}')
        meals = resp['meals']  # Список с блюдами-словарями {strMeal:..., strMealThumb:..., idMeal:...}

        # Data
        result: list = sample(meals, k=num)
        ids = [i['idMeal'] for i in result]
        await state.set_data({'id': ids})

        # Translate
        text = '\n'.join(i['strMeal'] for i in result)
        translation = translator.translate(text, dest='ru')

        # Button
        kb = [[
            types.KeyboardButton(text="Покажи рецепты"),
        ], ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

        await message.answer(f'Как Вам такие варианты:\n{translation.text}', reply_markup=keyboard)
        await state.set_state(FakeDatabase.waiting_for_id.state)
    except Exception:
        await message.answer(f"Ошибка: переданы не корректные данные.")


@router.message(FakeDatabase.waiting_for_id)
async def get_recipes(message: types.Message, state: FSMContext):
    """ Вывод рецептов. Завершение логики. """
    try:
        ids = await state.get_data()  # Получаем ранее записанные данные
        tasks = [
            get_url_json(f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={id_meal}') for id_meal in ids['id']
        ]
        result = await asyncio.gather(*tasks)

        for meal in result:
            meal = meal['meals'][0]

            name = meal['strMeal']
            recipes = meal['strInstructions']
            img = meal['strMealThumb']
            video = meal['strYoutube']

            # Махинации с ингридиентами
            list_ingredient: list = []
            for i in range(1, 21):
                if meal[f'strIngredient{i}'] != 'None' and meal[f'strIngredient{i}'] is not None and meal[f'strIngredient{i}'].strip() != '':
                    list_ingredient.append(f'{meal[f"strIngredient{i}"]} - {meal[f"strMeasure{i}"]}')
            ingredients = '\n'.join(i for i in list_ingredient)

            # Translate
            text = f"{name}\nFoto:\n{img}\n\nRecipe:\n{recipes}\n\nIngredients:\n{ingredients}\n\nVideo:\n{video}\n"
            translation = translator.translate(text, dest='ru')
            await message.answer(translation.text)
    except Exception:
        await message.answer(f"Ошибка: переданы не корректные данные.")