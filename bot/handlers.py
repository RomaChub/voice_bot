from aiogram.types import Message, Voice, File
from aiogram import Router, F, Bot, types
from aiogram.filters import CommandStart

from bot.utils import save_voice_as_mp3, audio_to_text

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет, я бот для ответа на голосовые сообщения")


@router.message(F.content_type == "voice")
async def process_voice_message(message: Message, bot: Bot):
    voice_path = await save_voice_as_mp3(bot, message)
    #transcripted_voice_text = await audio_to_text(voice_path)

    await message.reply(text=voice_path)
