from aiogram import Bot
from aiogram.types import Message


async def save_voice_as_mp3(bot: Bot, message: Message):
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_name = f"files/audio{file_id}.mp3"
    voice_mp3_path = await bot.download_file(file_path, file_name)

    return voice_mp3_path
