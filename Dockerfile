FROM  python:latest
ENV PYTHONUNBUFFERED=1 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.7.0 \
  PYTHONPATH=/voice_bot

WORKDIR /voice_bot

COPY requirements.txt requirements.txt

COPY . .

COPY start.sh /voice_bot/start.sh
RUN chmod +x /voice_bot/start.sh

CMD ["./start.sh"]
