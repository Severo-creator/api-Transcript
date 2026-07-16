import os
import sys
import threading
import time
import webbrowser
from pathlib import Path


def caminho_base():
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent


BASE_DIR = caminho_base()
os.chdir(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "transcript.settings")


def iniciar_servidor():
    import django
    from django.core.management import call_command

    django.setup()
    call_command("runserver", "127.0.0.1:8000", "--noreload")


threading.Thread(target=iniciar_servidor, daemon=True).start()

time.sleep(2)
webbrowser.open("http://127.0.0.1:8000/")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
