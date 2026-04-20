from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from os import getenv
from dotenv import load_dotenv
from functools import wraps

router = Router()
load_dotenv()


def admin_only(handler):
    @wraps(handler)
    async def wrapper(message: Message, *args, **kwargs):
        admins_id = set(getenv('ADMINS_ID').split(';'))
        owner_id = getenv('OWNER_ID')
        uid = str(message.from_user.id)

        if uid in admins_id or uid == owner_id:
            return await handler(message, *args, **kwargs)
        return await message.answer('В доступе отказано.')

    return wrapper

def admin_panel():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Перезапустить')],
            [KeyboardButton(text='Запустить'), KeyboardButton(text='Остановить')]
        ],
        resize_keyboard=True
    )
    return keyboard


@router.message(Command('start'))
async def start(message: Message):
    await message.answer('Привет')


@router.message(Command('get_id'))
async def get_id(message: Message):
    await message.answer(str(message.from_user.id))


@router.message(Command('mc_console'))
@admin_only
async def mc_console(message: Message):
    await message.answer(
        '<b>Панель управления майнкрафт сервера</b>\nДоступ разрешен.',
        parse_mode='HTML',
        reply_markup=admin_panel()
    )