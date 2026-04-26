from functools import wraps
from os import getenv
from dotenv import load_dotenv
from aiogram.types import Message


load_dotenv()


def admin_only(handler):
    @wraps(handler)
    async def wrapper(message: Message, *args, **kwargs):
        admins_id = set(getenv('ADMINS_ID').split(';'))
        owner_id = getenv('OWNER_ID')
        uid = str(message.from_user.id)

        if uid in admins_id or uid == owner_id:
            return await handler(message, *args, **kwargs)
        return await message.answer('Не достаточно прав.')

    return wrapper