import os

from aiogram.types import Message, FSInputFile
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart

from bot.utils import Utils

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет, я бот для ответа на голосовые сообщения")


@router.message(F.content_type == "voice")
async def process_voice_message(message: Message, bot: Bot):
    processing_message = await message.answer("Подождите, я обрабатываю ваше сообщение...")
    voice_path = await Utils.save_voice_as_mp3(bot, message)

    transcripted_voice_text = await Utils.audio_to_text(voice_path)

    answer = await Utils.get_response_from_openai(transcripted_voice_text)

    await Utils.text_to_speech(answer)

    voice_file = FSInputFile("speech.mp3")
    await bot.send_voice(chat_id=message.chat.id, voice=voice_file, caption="Вот ваш ответ!")
    os.remove(voice_path)
    await processing_message.delete()
