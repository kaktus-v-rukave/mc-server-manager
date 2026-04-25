from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from os import getenv
from dotenv import load_dotenv
from functools import wraps
from server_panel.rcon_service import RconService
import subprocess
from keyboards.reply_keyboards import server_menu, main_menu
import asyncio


load_dotenv()
router = Router()
rcon = RconService('127.0.0.1', getenv('RCON_PASSWD'))


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


@router.message(Command('start'))
async def start(message: Message):
    if str(message.from_user.id) == getenv('OWNER_ID'):
        user_status = '[Owner]'
    elif str(message.from_user.id) in getenv('ADMINS_ID').split(';'):
        user_status = '[Admin]'
    else:
        user_status = ''

    await message.answer(
        f'Приветствую, {message.from_user.first_name}{user_status}.\n'
        'Выберите действие в появившемся меню.',
        reply_markup=main_menu()
    )


@router.message(F.text == 'Мой ID')
async def get_id(message: Message):
    await message.answer(f'Ваш ID: {str(message.from_user.id)}')


@router.message(F.text == 'Меню сервера')
@admin_only
async def mc_console(message: Message):
    await message.answer('Выберите действие.', reply_markup=server_menu())


@router.message(F.text == 'Стоп')
@admin_only
async def stop_server(message: Message):
    await message.answer('<b>Сервер остановлен</b> 🛑', parse_mode='HTML')
    rcon.stop_server()


@router.message(F.text == 'Пуск')
@admin_only
async def start_server(message: Message):
    sent = await message.answer('<b>Запускаю</b> 🚀', parse_mode='HTML')
    subprocess.run(["screen", "-S", "mc", "-X", "stuff", "./run.sh\n"])
    await asyncio.sleep(15)
    await sent.edit_text('<b>Сервер запущен</b> ✅', parse_mode='HTML')