# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules

BASE_DIR = Path(".").resolve()   # <-- Fix: aktuelles Arbeitsverzeichnis

# Alle Templates & Static rekursiv einsammeln und Zielpfade beibehalten
datas = []
for folder in ["app/templates", "app/static", "instance"]:
    src = BASE_DIR / folder
    if src.exists():
        for p in src.rglob("*"):
            if p.is_file():
                rel = p.relative_to(BASE_DIR)  # z.B. app/static/...
                datas.append((str(p), str(rel.parent)))  # in selben Ordner entpacken

# Hidden Imports für Flask/Jinja2
hidden = []
for pkg in ["flask", "jinja2", "werkzeug", "markupsafe"]:
    hidden += collect_submodules(pkg)

block_cipher = None

a = Analysis(
    ['run.py'],                         # Einstiegspunkt
    pathex=[str(BASE_DIR)],
    binaries=[],
    datas=datas,
    hiddenimports=hidden,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='zufallsgenerator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,                                        # Konsole sichtbar lassen
    icon=str(BASE_DIR / 'app' / 'static' / 'BMWLogo.ico')
)
