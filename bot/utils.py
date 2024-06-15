import openai
from aiogram import Bot
from aiogram.types import Message
from dotenv import load_dotenv
from openai import AsyncOpenAI
from config import settings

load_dotenv()
client = AsyncOpenAI()


class Utils:
    def __init__(self):
        openai.api_key = settings.openai_api_key

    @classmethod
    async def save_voice_as_mp3(cls, bot: Bot, message: Message):
        file_id = message.voice.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        file_name = f"files/audio{file_id}.mp3"
        voice_mp3_path = await bot.download_file(file_path, file_name)

        return file_name

    @classmethod
    async def audio_to_text(cls, file_path: str) -> str:
        with open(file_path, "rb") as audio_file:
            transcript = await client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return str(transcript)

    @classmethod
    async def get_response_from_openai(cls, text: str) -> str:
        if settings.assistant_id != "no_id":
            assistant = await client.beta.assistants.retrieve(settings.assistant_id)
        else:
            assistant = await client.beta.assistants.create(
                name="Assistant",
                description="You are a helpful assistant.You should to answer questions",
                model="gpt-3.5-turbo",
                tools=[]
            )
            settings.assistant_id = assistant.id

        thread_id = settings.thread_id
        assistant_id = settings.assistant_id

        if thread_id is None or thread_id == "no_id":
            thread = await client.beta.threads.create()
            thread_id = thread.id
            settings.thread_id = thread_id

        await client.beta.threads.messages.create(thread_id=thread_id,
                                                  role="user",
                                                  content=text)

        run = await client.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=assistant_id,
            poll_interval_ms=5000)

        if run.status == 'requires_action':
            return "Please, repeat the question."
        if run.status == "completed":
            messages = await client.beta.threads.messages.list(thread_id=thread_id)
            message_content = messages.data[0].content[0].text
            annotations = message_content.annotations

            for annotation in annotations:
                message_content.value = message_content.value.replace(annotation.text, '')

            response_message = message_content.value
            return response_message

    @classmethod
    async def text_to_speech(cls, text: str):
        speech_file_path = "speech.mp3"
        response = await client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )
        response.stream_to_file(speech_file_path)
        return speech_file_path
