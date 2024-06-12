import openai
from aiogram import Bot
from aiogram.types import Message
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


async def save_voice_as_mp3(bot: Bot, message: Message):
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_name = f"files/audio{file_id}.mp3"
    voice_mp3_path = await bot.download_file(file_path, file_name)

    return file_name


async def audio_to_text(file_path: str) -> str:
    with open(file_path, "rb") as audio_file:
        transcript = await openai.Audio.atranscribe(
            "whisper-1", audio_file
        )
    return transcript["text"]
