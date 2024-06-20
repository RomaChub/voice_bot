import os

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, FSInputFile
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command

from bot.utils import Utils
from bot.event_tracker import Events
router = Router()


class VoiceState(StatesGroup):
    AWAITING_QUESTION = State()
    AWAITING_VOICE_FOR_VALUE = State()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    Events.start_event(str(message.from_user.id))
    await state.set_state(VoiceState.AWAITING_QUESTION)
    await message.answer("Привет, я бот для ответа на голосовые сообщения")


@router.message(Command("help"))
async def help(message: Message, state: FSMContext):
    Events.start_event(str(message.from_user.id))
    await state.set_state(VoiceState.AWAITING_QUESTION)
    help_text = (
        "Вот команды, которые я поддерживаю:\n"
        "/start - начать работу с ботом\n"
        "/my_value - помогу найти твою ценность\n"
    )
    await message.answer(help_text)


@router.message(F.content_type == "voice", VoiceState.AWAITING_QUESTION)
async def process_voice_message(message: Message, state: FSMContext, bot: Bot):
    Events.start_event(str(message.from_user.id))
    processing_message = await message.answer("Подождите, я обрабатываю ваше сообщение...")
    voice_path = await Utils.save_voice_as_mp3(bot, message)

    transcripted_voice_text = await Utils.audio_to_text(voice_path)

    answer = await Utils.get_response_from_openai(transcripted_voice_text)

    await Utils.text_to_speech(answer)

    voice_file = FSInputFile("speech.mp3")
    await bot.send_voice(chat_id=message.chat.id, voice=voice_file, caption="Вот ваш ответ!")
    os.remove(voice_path)
    await processing_message.delete()


@router.message(Command("my_value"))
async def my_value(message: Message, state: FSMContext):
    Events.start_event(str(message.from_user.id))
    await message.answer("Я помогу найти твою ключевую ценность")
    await message.answer("Давай пообщаемся. Отправь мне голосовое сообщение.")
    await state.set_state(VoiceState.AWAITING_VOICE_FOR_VALUE)


@router.message(F.content_type == "voice", VoiceState.AWAITING_VOICE_FOR_VALUE)
async def process_voice_for_value(message: Message, state: FSMContext, bot: Bot):
    Events.start_event(str(message.from_user.id))
    processing_message = await message.answer("Подождите, я обрабатываю ваше сообщение.....")
    voice_path = await Utils.save_voice_as_mp3(bot, message)
    transcripted_voice_text = await Utils.audio_to_text(voice_path)
    user_id = message.from_user.id

    answer = await Utils.find_value(str(user_id), transcripted_voice_text)
    if answer == "Failed":
        await message.answer("Расскажи чуть больше о себе")
        os.remove(voice_path)
        await state.set_state(VoiceState.AWAITING_VOICE_FOR_VALUE)
    else:
        await Utils.text_to_speech(answer)
        voice_file = FSInputFile("speech.mp3")
        await bot.send_voice(chat_id=message.chat.id, voice=voice_file, caption="Вот ваш ответ!")
        os.remove(voice_path)
        await state.set_state(VoiceState.AWAITING_QUESTION)
    await processing_message.delete()


@router.message(F.content_type == "photo")
async def process_photo(message: Message, state: FSMContext, bot: Bot):
    Events.start_event(str(message.from_user.id))
    await state.set_state(VoiceState.AWAITING_QUESTION)
    processing_message = await message.answer("Подождите, я обрабатываю вашу фотографию...")
    file_name = await Utils.save_photo(message)
    answer = await Utils.detect_mood(file_name)
    await processing_message.delete()
    os.remove(file_name)
    await message.answer(answer)









