import base64

import openai
from aiogram import Bot
from aiogram.types import Message
from dotenv import load_dotenv
from openai import AsyncOpenAI
import json
from config import settings
from bot.database.database import ValueOrm, new_session
from aiogram.fsm.context import FSMContext

load_dotenv()
client = AsyncOpenAI()


async def save_value(core_value: str, user_id: str):
    value = ValueOrm(core_value=core_value, user_id=user_id)
    async with new_session() as session:
        value_orm = value
        session.add(value_orm)
        await session.flush()
        await session.commit()


async def encode_image(image_path: str):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


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
    async def get_response_from_openai(cls, text: str, state: FSMContext) -> str:
        if settings.assistant_id != "no_id":
            assistant = await client.beta.assistants.retrieve(settings.assistant_id)
        else:
            assistant = await client.beta.assistants.create(
                name="Assistant",
                description="Ты дружелюбный ассистент имеющий данные о тревожности",
                model="gpt-4o",
                tools=[{"type": "file_search"}]
            )

            vector_store = await client.beta.vector_stores.create(
                name="Тревожность"
            )
            file_paths = ["bot/data_files/file_1.docx"]
            file_streams = [open(path, "rb") for path in file_paths]

            file_batch = await client.beta.vector_stores.file_batches.upload_and_poll(
                vector_store_id=vector_store.id, files=file_streams
            )

            assistant = await client.beta.assistants.update(
                assistant_id=assistant.id,
                tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
            )

            settings.assistant_id = assistant.id

        assistant_id = settings.assistant_id

        message_file = await client.files.create(
            file=open("bot/data_files/file_1.docx", "rb"), purpose="assistants"
        )

        thread = await client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": f""" Вопрос: {text}
                                    Найди ответ в приложенном файле, указав название файла в ответе.
                                    Если ответ не найден в файле, просто ответь на вопрос, не указывая названия файла.
                                """,
                    "attachments": [
                        {"file_id": message_file.id, "tools": [{"type": "file_search"}]}
                    ],
                }
            ]
        )
        thread_id = thread.id

        await state.update_data(thread_id=thread_id)

        run = await client.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=assistant_id)
        if run.status in ['requires_action', 'running', 'queued', 'failed', 'canceled', 'timed_out']:
            return str("Please, repeat the question.")
        if run.status == str("completed"):
            messages = await client.beta.threads.messages.list(thread_id=thread_id, run_id=run.id)
            message_content = messages.data[0].content[0].text
            annotations = message_content.annotations

            try:
                file_name = "Ответ взят из файла: " + annotations[0].text[5:16]
            except IndexError:
                file_name = ""

            for annotation in annotations:
                message_content.value = message_content.value.replace(annotation.text, '')

            response_message = message_content.value
            print(response_message + "\n" + file_name)
            return str(response_message)

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

    @staticmethod
    async def answer_validation(answer: str) -> bool:
        messages = [{"role": "user", "content": f"This correct words? {answer}"}]
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "answer_validation",
                    "description": "Understand are my values correct? If yes answer True, if no answer False.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "correct": {
                                "type": "boolean",
                                "description": "True or False",
                            },
                        },
                        "required": ["correct"],
                    },
                },
            }
        ]
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )

        arguments_json = response.choices[0].message.tool_calls[0].function.arguments
        arguments_dict = json.loads(arguments_json)
        correct = arguments_dict.get("correct")
        print(correct)
        if correct:
            return True
        else:
            return False

    @classmethod
    async def find_value(cls, user_id: str, text: str) -> str:
        if settings.value_assistant_id != "no_id":
            assistant = await client.beta.assistants.retrieve(settings.value_assistant_id)
        else:
            assistant = await client.beta.assistants.create(
                name="Assistant",
                description="From the messages you should understand my core values.",
                model="gpt-3.5-turbo",
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "save_value",
                            "description": "determine my core value",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "core_value": {
                                        "type": "string",
                                        "values": "person's core value"
                                    }
                                },
                                "required": ["core_value"]
                            }
                        }
                    }
                ]
            )
            settings.value_assistant_id = assistant.id
        assistant_id = settings.value_assistant_id

        thread = await client.beta.threads.create()
        thread_id = thread.id

        await client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=f"Помоги мне определить мои ключевые ценности из этого рассказа: {text}"
        )

        run = await client.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=assistant_id,
            poll_interval_ms=5000
        )
        if run.status in ['running', 'queued', 'failed', 'canceled', 'timed_out']:
            return "Please, repeat the question."

        if run.status == 'completed or ' or run.status == 'requires_action':

            messages = await client.beta.threads.messages.list(thread_id=thread_id)
            if not messages.data:
                return "Failed"

            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            core_value = ""
            for i in range(0, len(tool_calls)):
                arguments = tool_calls[i].function.arguments
                arguments_json = json.loads(arguments)
                core_value = core_value + " " + arguments_json.get("core_value")
            print(core_value)
            if await cls.answer_validation(str(core_value)):
                await save_value(core_value, user_id)
                return str(core_value)
            else:
                return "Failed"

        return "Failed"

    @classmethod
    async def save_photo(cls, message) -> str:
        file_id = message.from_user.id
        file_name = f"files/photo{file_id}.jpg"
        await message.bot.download(file=message.photo[-1].file_id, destination=file_name)
        return file_name

    @classmethod
    async def detect_mood(cls, file_name: str) -> str:
        base64_image = await encode_image(file_name)
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Определи настроение по фото."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        return response.choices[0].message.content
