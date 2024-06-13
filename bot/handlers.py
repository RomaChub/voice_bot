import os

from aiogram.types import Message, Voice, File, InputMediaAudio, InputFile, FSInputFile
from aiogram import Router, F, Bot, types, methods
from aiogram.filters import CommandStart, Command

from bot.utils import save_voice_as_mp3, audio_to_text, get_response_from_openai, text_to_speech

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет, я бот для ответа на голосовые сообщения")


@router.message(F.content_type == "voice")
async def process_voice_message(message: Message, bot: Bot):
    voice_path = await save_voice_as_mp3(bot, message)
    transcripted_voice_text = await audio_to_text(voice_path)
    answer = await get_response_from_openai(transcripted_voice_text)
    await text_to_speech(answer)
    voice_file = FSInputFile("speech.mp3")
    await bot.send_voice(chat_id=message.chat.id, voice=voice_file, caption="Вот ваш ответ!")
    os.remove(voice_path)
