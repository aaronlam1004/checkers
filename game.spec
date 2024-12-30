# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['game.py'],
    pathex=[],
    binaries=[],
    datas=[
        ("resources/audio/move.wav", "./resources/audio"),
        ("resources/audio/speed.mp3", "./resources/audio"),
        ("resources/fonts/Black Bird.otf", "./resources/fonts"),
        ("resources/fonts/Starborn.otf", "./resources/fonts"),
        ("resources/imgs/background.png", "./resources/imgs"),
        ("resources/imgs/flag.png", "./resources/imgs"),
        ("resources/imgs/home.png", "./resources/imgs"),
        ("resources/imgs/icon.png", "./resources/imgs"),
        ("resources/imgs/king.png", "./resources/imgs"),
        ("resources/imgs/refresh.png", "./resources/imgs"),
        ("resources/music/lofi-song-backyard-by-lofium-242713.mp3", "./resources/music"),
        ("resources/music/once-in-paris-168895.mp3", "./resources/music"),
        ("resources/music/relaxed-day-futuristic-chill-250712.mp3", "./resources/music"),
        ("resources/music/relaxed-vlog-night-street-131746.mp3", "./resources/music"),
    ],
    hiddenimports=["pillow", "pygame"],
    hookspath=[],
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
    exclude_binaries=False,
    name='Checkers Blitz',
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
    icon="resources/imgs/icon.ico"
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Checkers Blitz',
)
