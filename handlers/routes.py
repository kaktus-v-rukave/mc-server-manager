from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from os import getenv
from dotenv import load_dotenv

load_dotenv()


def is_admin(uid):
    admins_id = set(getenv('ADMINS_ID').split(';'))
    return str(uid) in admins_id


def is_owner(uid):
    owner_id = getenv('OWNER_ID')
    return str(uid) == owner_id

def admin_panel():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Перезапустить')],
            [KeyboardButton(text='Запустить'), KeyboardButton(text='Остановить')]
        ],
        resize_keyboard=True
    )
    return keyboard


router = Router()


@router.message(Command('start'))
async def start(message: Message):
    await message.answer('Привет')


@router.message(Command('get_id'))
async def get_id(message: Message):
    await message.answer(str(message.from_user.id))


@router.message(Command('mc_server_op'))
async def mc_server_op(message: Message):
    if is_admin(message.from_user.id):
        await message.answer(
            'Доступ разрешен.\nДобро пожаловать.',
            reply_markup=admin_panel()
        )
    else:
        await message.answer('В доступе отказано.')