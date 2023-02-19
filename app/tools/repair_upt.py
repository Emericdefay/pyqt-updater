import json

from updater.settings import DEF_STGS
from updater.paths import UPT_PATH


def repair_update_json() -> None: 
    with open(f'{UPT_PATH}', 'w') as f:
        json.dump(DEF_STGS, f)

if __name__ == "__main__":
    repair_update_json()