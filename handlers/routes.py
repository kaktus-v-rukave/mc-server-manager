from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from os import getenv
from dotenv import load_dotenv
from functools import wraps
from server_panel.rcon_service import RconService
import subprocess

router = Router()

load_dotenv()

rcon = RconService('172.0.0.1', getenv('RCON_PASSWD'))


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
            [KeyboardButton(text='Перезапуск')],
            [KeyboardButton(text='Пуск'), KeyboardButton(text='Стоп')]
        ],
        resize_keyboard=True
    )
    return keyboard


@router.message(Command('get_id'))
async def get_id(message: Message):
    await message.answer(str(message.from_user.id))


@router.message(Command('menu'))
@admin_only
async def mc_console(message: Message):
    await message.answer('Выберите действие.', reply_markup=admin_panel())


@router.message(F.text == 'Стоп')
@admin_only
async def stop_server(message: Message):
    await message.answer('Остановка...')
    rcon.stop_server()


@router.message(F.text == 'Пуск')
@admin_only
async def start_server(message: Message):
    await message.answer('Запуск...')
    subprocess.run(["screen", "-S", "mc", "-X", "stuff", "./run.sh\n"])