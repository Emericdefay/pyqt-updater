# -*- mode: python ; coding: utf-8 -*-
import os, sys
from pathlib import Path

sys.path.append(
    os.path.join(os.path.dirname(os.path.realpath("")), os.pardir)
)

try:
    from app.updater.settings import APP_NAME
except ModuleNotFoundError:
    APP_NAME = 'main'

LAUNCHER_NAME = 'launcher'


# Get the path of the folder containing the .spec file
base_path = Path('').parent.absolute()
lib_dir = os.path.join(base_path, 'dist', f'{APP_NAME}', 'lib')
dist_dir = os.path.join(base_path, 'dist', f'{APP_NAME}')



block_cipher = None

# launcher

launcher_a = Analysis(
    [f'.\\..\\app\\{LAUNCHER_NAME}.py'],
    pathex=[base_path],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[f'{os.path.join(base_path, "specs", "add_lib.py")}'],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

launcher_pyz = PYZ(launcher_a.pure, launcher_a.zipped_data, cipher=block_cipher)

launcher_exe = EXE(
    launcher_pyz,
    launcher_a.scripts,
    [],
    exclude_binaries=True,
    name=f'{LAUNCHER_NAME}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# app
app_a = Analysis(
    [f'.\\..\\app\\{APP_NAME}.py'],
    pathex=[base_path],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[f'{os.path.join(base_path, "specs", "add_lib.py")}'],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
app_pyz = PYZ(app_a.pure, app_a.zipped_data, cipher=block_cipher)

app_exe = EXE(
    app_pyz,
    app_a.scripts,
    [],
    exclude_binaries=True,
    name=f'{APP_NAME}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)


coll = COLLECT(
    launcher_exe,
    launcher_a.binaries,
    launcher_a.zipfiles,
    launcher_a.datas,
    app_exe,
    app_a.binaries,
    app_a.zipfiles,
    app_a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=f'{APP_NAME}',
)

for (dirpath, dirnames, filenames) in os.walk(dist_dir):
    if dirpath is not dist_dir:
        continue
    for filename in filenames:
        if filename.endswith('.dll') or filename.endswith('.pyd'):
            if 'python' in filename:
                continue
            if 'VCRUNTIME' in filename:
                continue
            filepath = os.path.join(dirpath, filename)
            os.makedirs(lib_dir, exist_ok=True)
            os.rename(filepath, os.path.join(lib_dir, filename))
