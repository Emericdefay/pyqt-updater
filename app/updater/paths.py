import os

from updater.settings import APP_NAME, UPT_NAME

UPT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), f"{UPT_NAME}.json")
APP_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), f"{APP_NAME}.exe")
