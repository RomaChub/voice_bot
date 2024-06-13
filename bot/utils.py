import time
from pathlib import Path

import openai
from aiogram import Bot, types
from aiogram.types import Message, FSInputFile
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI()


async def save_voice_as_mp3(bot: Bot, message: Message):
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_name = f"files/audio{file_id}.mp3"
    voice_mp3_path = await bot.download_file(file_path, file_name)

    return file_name


async def audio_to_text(file_path: str) -> str:
    with open(file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return str(transcript)


async def get_response_from_openai(text: str) -> str:
    assistant = client.beta.assistants.create(
        name="Assistant",
        description="You are a helpful assistant.You should to answer questions",
        model="gpt-3.5-turbo",
        tools=[]
    )

    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": text
            }
        ]
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )
    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread.id,
                                                       run_id=run.id)
        if run_status.status == "completed":
            break
        elif run_status.status == "failed":
            print("Run failed:", run_status.last_error)
            break
        time.sleep(5)

    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )

    number_of_messages = len(messages.data)
    print(f'Number of messages: {number_of_messages}')

    answer = []
    for message in reversed(messages.data):
        role = message.role
        for content in message.content:
            if content.type == 'text' and role == 'assistant':
                response = content.text.value
                print({response})
                answer.append(str(response))
    return answer[0]


async def text_to_speech(text):
    speech_file_path = "speech.mp3"
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    response.stream_to_file(speech_file_path)
    return speech_file_path
