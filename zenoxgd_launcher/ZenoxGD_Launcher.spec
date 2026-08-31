# -*- mode: python ; coding: utf-8 -*-
# ============================================================
#  ZENOX GD LAUNCHER  -  PyInstaller Spec File
#  Created by SONI
#  Use:  pyinstaller ZenoxGD_Launcher.spec
# ============================================================

import os
import sys

block_cipher = None

# ── Paths ─────────────────────────────────────────────────
PROJECT_DIR = os.path.abspath(SPECPATH)
ASSETS_DIR   = os.path.join(PROJECT_DIR, 'assets')
MAIN_SCRIPT  = os.path.join(PROJECT_DIR, 'main.py')
ICON_FILE    = os.path.join(ASSETS_DIR, 'icon.ico')  # Replace with your icon

# ── Datas (assets folder bundled into exe) ─────────────────
datas = []
if os.path.isdir(ASSETS_DIR):
    datas.append((ASSETS_DIR, 'assets'))

# ── Hidden imports (CTk needs these) ──────────────────────
hiddenimports = [
    'customtkinter',
    'PIL',
    'PIL._tkinter_finder',
]

# ═══════════════════════════════════════════════════════════
a = Analysis(
    [MAIN_SCRIPT],
    pathex=[PROJECT_DIR],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ZenoxGD Launcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,          # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=ICON_FILE if os.path.exists(ICON_FILE) else None,
    version_file=None,       # Add a version file if desired
)
