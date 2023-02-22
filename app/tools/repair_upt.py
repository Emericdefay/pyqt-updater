import json

from updater.settings import DEF_STGS
from updater.paths import UPT_PATH


def repair_update_json() -> None: 
    """
    Writes default settings to the update configuration file. This is used when
    the update configuration file is missing or corrupted, to ensure that the
    application can operate with default settings.

    Returns:
        None
    """
    with open(f'{UPT_PATH}', 'w') as f:
        json.dump(DEF_STGS, f)

if __name__ == "__main__":
    repair_update_json()
