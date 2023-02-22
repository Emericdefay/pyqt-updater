from typing import Any
import os
import sys
import re
import json
import subprocess
import queue
import tkinter as tk
import requests
import logging
import unittest

try:
    from updater.settings import (
        USER,
        REPO,
        APP_NAME,
        DEBUG,
        WIDTH,
        HEIGHT,
        TAG_FRONT,
        TAG_BACK,
        UPD_HEX_C
    )
    from updater.paths import APP_PATH, UPT_PATH
    from updater.spinner import DownloadProgressBar
    from updater.dialog import dialog_error
    from updater.tests.test_integrity import TestUpdateJson

    from tools.repair_upt import repair_update_json

    from dbg.logs import setup_logs, log_exceptions
except ModuleNotFoundError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    from app.updater.settings import (USER,
    REPO,
    APP_NAME,
    DEBUG,
    WIDTH,
    HEIGHT,
    TAG_FRONT,
    TAG_BACK,
    UPD_HEX_C
    )
    from app.updater.paths import APP_PATH, UPT_PATH
    from app.updater.spinner import DownloadProgressBar
    from app.updater.dialog import dialog_error
    from app.updater.tests.test_integrity import TestUpdateJson

    from app.tools.repair_upt import repair_update_json

    from app.dbg.logs import setup_logs, log_exceptions


setup_logs()
my_queue = queue.Queue()


def get_app_name():
    """
    Returns the name of the application.

    Returns:
        A string representing the name of the application.
    """
    return APP_NAME


@log_exceptions
def load_json() -> Any:
    """
    This is a function that loads a JSON file from disk and returns its
    content. The function is decorated with the @log_exceptions decorator,
    which will log any exceptions that occur while the function is running.

    The function first attempts to open the JSON file using a context manager
    (with open(...) as f_json:) and load its content using the json.load()
    method. If this operation fails with a FileNotFoundError, the function
    calls the repair_update_json() function to create a new JSON file with
    default settings, and then recursively calls itself to attempt to load the
    newly created file.

    Note that this recursion could potentially cause an infinite loop if the
    repair_update_json() function is unable to create a valid JSON file for
    some reason. A better approach might be to have a loop that tries to load
    the file a certain number of times before giving up, and possibly showing
    an error message to the user.
    """
    try:
        with open(f"{UPT_PATH}") as f_json:
            data = json.load(f_json)
        return data
    except FileNotFoundError:
        repair_update_json()
        load_json()


@log_exceptions
def update_json(data: dict) -> None: 
    """
    The update_json function takes a dictionary as input and writes it to a
    JSON file located at UPT_PATH with the contents of the input dictionary.
    If there is an exception while writing the file, it will be logged using
    the log_exceptions decorator.
    """
    with open(f'{UPT_PATH}', 'w') as f:
        json.dump(data, f)


@log_exceptions
def update(url: str) -> None:
    """
    The update function is using tkinter library to create a progress bar and
    download a file from a given url. During the download, it will display the
    amount of bytes downloaded and the download speed. After the download is
    completed, the tkinter window is destroyed.
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


@log_exceptions
def version_check() -> None:
    """
    The version_check function checks if a new version of the application is
    available on GitHub, and if so, downloads and installs it.

    Here is a breakdown of what the function does:

        - It loads the JSON parameters (branch and application version) using
          the load_json function.
        - It retrieves the latest version number available on GitHub by sending
          a request to the corresponding page and parsing the URL. It also 
          checks if the current version is outdated or if the application file 
          is missing (in the latter case, it assumes that an update is 
          required).
        - It retrieves the version number (which is different from the 
          application version number) by sending a request to a text file on 
          GitHub.
        - It constructs the update URL by combining the repository and version 
          information obtained earlier.
        - It enqueues an update task using the update function.
        - It updates the JSON parameters to reflect the latest application 
          version using the update_json function.

    Overall, this function automates the update process by fetching the latest
    version information and downloading the update from GitHub, and it uses the
    update function to perform the actual download and installation.
    """
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

    # Does it need an update?
    if latest_version != APP_VER or not file_exist or DEBUG:
        # Log feed
        if latest_version != APP_VER:
            logging.info(f"Update required : {APP_VER} -> {latest_version}")
        elif not file_exist:
            logging.info(f"Update required : File {APP_NAME} doesn't exist")
        else:
            logging.info(f"Update required : DEBUG MODE")

        # Vérifier si une mise à jour est disponible
        version_url = f"https://raw.githubusercontent.com/\
                        {USER}/{REPO}/{BRANCH}/version.txt"
        version = requests.get(version_url).text

        # Update depuis GitHub
        update_url = f"https://github.com/\
                       {USER}/{REPO}/releases/download/\
                       {TAG_FRONT}{version}{TAG_BACK}/{APP_NAME}.exe"

        try:
            my_queue.put(update(update_url))           
            # Mettre à jour le fichier json
            data['APP_VER'] = latest_version
            update_json(data)
        except Exception as e:
            dialog_error(e)
            logging.error(f"Errors in version_check : {e}", exc_info=True)
            raise


@log_exceptions
def main() -> None:
    """
    The main function seems to be the entry point of the application.
    
    Here's what it does:

        - It checks the JSON configuration file using load_json.
        - It runs integrity tests on the updater using unittest. It raises an 
          exception if the tests fail.
        - It checks for an available update using version_check.
        - It launches the updated application using subprocess.Popen.
    """
    # check json
    load_json()
    # check updater integrity
    try:
        suite = unittest.TestLoader().loadTestsFromTestCase(TestUpdateJson)
        test_integrity_result = unittest.TextTestRunner(verbosity=2).run(suite)
        assert test_integrity_result.wasSuccessful(), "Integrity tests failed"
    except AssertionError as e:
        dialog_error(e)
        logging.error(f"Tests failed : {e}", exc_info=True)
    # launch 
    version_check()
    # Lancer l'application une fois les mises à jour terminées
    my_queue.put(subprocess.Popen(f"{APP_PATH}"))


if __name__ == '__main__':
    main()
    os._exit(0)
