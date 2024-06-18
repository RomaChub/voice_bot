#!/bin/sh

pip install --no-cache-dir -r requirements.txt

alembic upgrade head

python main.py