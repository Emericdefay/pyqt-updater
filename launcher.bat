@echo off

rem Récupération du chemin courant
set current_path=%~dp0
cd %current_path%
echo %current_path%

rem Activer l'environnement virtuel
if not exist "%current_path%env" (
    echo no env
    python -m venv "%current_path%env"
    call "%current_path%env\Scripts\activate.bat pip install -r %current_path%requirements.txt"
) else (
    call "%current_path%env\Scripts\activate.bat"
)

rem Lancer le script Python
python "%current_path%launcher.py" %current_path%
