# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = ['core', 'transcript']
hiddenimports += collect_submodules('django')
hiddenimports += collect_submodules('rest_framework')


a = Analysis(
    ['iniciar_app.py'],
    pathex=[],
    binaries=[],
    datas=[('db.sqlite3', '.'), ('core', 'core'), ('transcript', 'transcript'), ('FrontTranscript', 'FrontTranscript'), ('planilhasfontes', 'planilhasfontes')],
    hiddenimports=hiddenimports,
    hookspath=['pyinstaller_hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='TranscriptDemo',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TranscriptDemo',
)
