from amplitude import Amplitude, BaseEvent
from config import settings
from concurrent.futures import ThreadPoolExecutor

client = Amplitude(settings.amplitude_api_key)
pool = ThreadPoolExecutor(max_workers=1)


class Events:  # содержит все возможные ивенты
    @staticmethod
    def process_photo_event(user_id: str):
        event = BaseEvent(event_type="Sent photo to determine mood", user_id=user_id)
        pool.submit(client.track(event))  # кидаю ивент в поток

    @staticmethod
    def process_voice_message_event(user_id: str):
        event = BaseEvent(event_type="Sent a voice message with a question", user_id=user_id)
        pool.submit(client.track(event))

    @staticmethod
    def my_value_event(user_id: str):
        event = BaseEvent(event_type="Switched the bot to value finding mode", user_id=user_id)
        pool.submit(client.track(event))

    @staticmethod
    def process_voice_for_value(user_id: str):
        event = BaseEvent(event_type="Sent a voice to find value", user_id=user_id)
        pool.submit(client.track(event))

    @staticmethod
    def help_event(user_id: str):
        event = BaseEvent(event_type="Get help", user_id=user_id)
        pool.submit(client.track(event))

    @staticmethod
    def start_event(user_id: str):
        event = BaseEvent(event_type="Start bot", user_id=user_id)
        pool.submit(client.track(event))

