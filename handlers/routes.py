from aiogram import Router, F
from aiogram.filters import Command, or_f
from aiogram.types import Message
from os import getenv
from dotenv import load_dotenv
from server_panel.rcon_service import RconService
import subprocess
from keyboards.reply_keyboards import server_menu, main_menu
import asyncio
from decorators.wraps import admin_only

load_dotenv()
router = Router()
rcon = RconService('127.0.0.1', getenv('RCON_PASSWD'))


@router.message(or_f(Command('start'), F.text == 'Назад'))
async def start(message: Message):
    if str(message.from_user.id) == getenv('OWNER_ID'):
        user_status = '[Owner]'
    elif str(message.from_user.id) in getenv('ADMINS_ID').split(';'):
        user_status = '[Admin]'
    else:
        user_status = ''

    await message.answer(
        f'Приветствую, {message.from_user.first_name} {user_status}.\n'
        'Выберите действие в появившемся меню.',
        reply_markup=main_menu()
    )


@router.message(F.text == 'Мой ID')
async def get_id(message: Message):
    await message.answer(
        f'Ваш ID: <code>{str(message.from_user.id)}</code>',
        parse_mode='HTML'
    )


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
    await asyncio.sleep(34)
    await sent.edit_text('<b>Сервер запущен</b> ✅', parse_mode='HTML')


@router.message(F.text == 'Перезапуск')
@admin_only
async def restart_server(message: Message):
    sent = await message.answer('<b>Перезапускаю</b> 🔃', parse_mode='HTML')
    rcon.stop_server()
    subprocess.run(["screen", "-S", "mc", "-X", "stuff", "./run.sh\n"])
    await asyncio.sleep(36)
    await sent.edit_text('<b>Сервер перезапущен</b> ✅', parse_mode='HTML')