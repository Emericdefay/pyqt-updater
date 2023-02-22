import os

from updater.settings import APP_NAME, UPT_NAME

file_dirname = os.path.dirname(__file__)

UPT_PATH = os.path.join(os.path.dirname(file_dirname), f"{UPT_NAME}.json")
APP_PATH = os.path.join(os.path.dirname(file_dirname), f"{APP_NAME}.exe")
