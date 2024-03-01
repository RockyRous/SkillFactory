from aiogram import types


def start_keyboard(DEBUG: bool = False):
    buttons = [
        [
            types.InlineKeyboardButton(text="Оставить отзыв", callback_data="review"),
            types.InlineKeyboardButton(text="Сбросить результаты", callback_data="quiz_reset"),
        ],
        [
            types.InlineKeyboardButton(text="Викторина", callback_data="quiz_start"),
        ],
        [
            types.InlineKeyboardButton(text="Связаться с сотрудником зоо", callback_data="contact_zoo"),
        ],
        # [
        #     types.InlineKeyboardButton(text="Дополнительное описание", callback_data="get_desc"),
        # ],
    ]
    if DEBUG:
        buttons.append([types.InlineKeyboardButton(text="DEBUG: get_data", callback_data="get_data")])
        buttons.append([types.InlineKeyboardButton(text="DEBUG: get_result", callback_data="get_result")])
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def quiz_finish():
    buttons = [
        [types.InlineKeyboardButton(text="К результатам!", callback_data="quiz_start")],
        [types.InlineKeyboardButton(text="В меню", callback_data="quiz_0_menu")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def main_menu():
    buttons = [
        [types.InlineKeyboardButton(text="В меню", callback_data="quiz_0_menu")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def quiz_reset():
    buttons = [
        [types.InlineKeyboardButton(text="Да", callback_data="quiz_0_delete")],
        [types.InlineKeyboardButton(text="Нет", callback_data="quiz_0_menu")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def quiz_keyboard(data, info_quest):
    answers = data['answers'].values()
    buttons = [[types.InlineKeyboardButton(text=f"{i['text']}", callback_data=f"quiz_{info_quest}_{i['result']}")] for i in answers]
    buttons.append([types.InlineKeyboardButton(text="Выход", callback_data="quiz_0_menu")])
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

