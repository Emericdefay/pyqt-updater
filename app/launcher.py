from typing import Any
import os
import re
import json
import subprocess
import queue
import tkinter as tk
import requests

from updater.settings import USER, REPO, APP_NAME, DEBUG, WIDTH, HEIGHT, TAG_FRONT, TAG_BACK, UPD_HEX_C
from updater.paths import APP_PATH, UPT_PATH
from updater.spinner import DownloadProgressBar

my_queue = queue.Queue()

def load_json() -> Any:
    with open(f"{UPT_PATH}") as f_json:
        data = json.load(f_json)
    return data

def update_json(data) -> None: 
    with open(f'{UPT_PATH}', 'w') as f:
        json.dump(data, f)

def update(url: str) -> None:
    """Update the REPO project release

    Args:
        url (str): _description_
    """
    # Create Tk window
    root = tk.Tk()
    # Masquer la barre de titre
    root.overrideredirect(True)
    

    # Créer le canvas et définir sa couleur
    canvas = tk.Canvas(root, bg=UPD_HEX_C)
    canvas.pack(fill="both", expand=True)
    # Définir les dimensions et la position de la fenêtre
    x = root.winfo_screenwidth() // 2 - WIDTH // 2
    y = root.winfo_screenheight() // 2 - HEIGHT // 2
    root.geometry(f'{WIDTH}x{HEIGHT}+{x}+{y}')
    root.configure(background='black')
    # Update
    download_url = url
    download_frame = DownloadProgressBar(canvas, download_url)
    download_frame.pack()

    canvas.tag_lower('canvas')
    # Tkinter window
    root.mainloop()

    root.quit()

def main() -> None:
    # Récupère les paramètres JSON
    data = load_json()
    BRANCH = data['BRANCH']
    APP_VER = data['APP_VER']

    # Récupérer la dernière version disponible sur GitHub
    url = f"https://github.com/{USER}/{REPO}/releases/latest"
    response = requests.get(url)
    latest_version = response.url.split("/")[-1]
    if not DEBUG:
        latest_version = re.sub('[a-zA-Z]', '', latest_version)\
                           .replace(' ', '')

    file_exist = os.path.exists(APP_PATH)

    if latest_version != APP_VER or not file_exist or DEBUG:
        # Vérifier si une mise à jour est disponible
        version_url = f"https://raw.githubusercontent.com/{USER}/{REPO}/{BRANCH}/version.txt"
        version = requests.get(version_url).text
        # Update depuis GitHub
        update_url = f"https://github.com/{USER}/{REPO}/releases/download/{TAG_FRONT}{version}{TAG_BACK}/{APP_NAME}.exe"
        try:
            my_queue.put(update(update_url))
            
            # Mettre à jour le fichier json
            data['APP_VER'] = latest_version
            update_json(data)
        except Exception as e:
            raise

    # Lancer l'application une fois les mises à jour terminées
    my_queue.put(subprocess.Popen(f"{APP_PATH}"))


if __name__ == '__main__':
    main()
    os._exit(0)
