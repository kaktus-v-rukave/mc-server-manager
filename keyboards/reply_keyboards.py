from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def server_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Перезапуск')],
            [KeyboardButton(text='Пуск'), KeyboardButton(text='Стоп')]
        ],
        resize_keyboard=True
    )
    return keyboard


def main_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Мой ID'),
                KeyboardButton(text='Управление сервером')
            ]
        ]
    )