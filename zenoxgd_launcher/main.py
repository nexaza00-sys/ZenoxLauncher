# ============================================================
#  ZENOX GD LAUNCHER  -  Created by SONI
#  Custom Desktop Launcher for Geometry Dash
#  Tech: Python 3 + CustomTkinter  |  Windows .exe ready
# ============================================================

import os
import sys
import subprocess
import webbrowser
import json
import tkinter as tk
from tkinter import messagebox, filedialog
from pathlib import Path

# ── PyInstaller _MEIPASS support for bundled assets ────────
APPLICATION_PATH = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk

# ═══════════════════════════════════════════════════════════════
#  COLOUR PALETTE  (Dark + Neon)
# ═══════════════════════════════════════════════════════════════
BG_DARK     = "#0a0a14"
BG_CARD     = "#12121f"
BG_HOVER    = "#1a1a2e"
NEON_PURPLE = "#b14aed"
NEON_RED    = "#ff2255"
NEON_GREEN  = "#00ff88"
NEON_CYAN   = "#00e5ff"
TEXT_WHITE  = "#e8e8f0"
TEXT_DIM    = "#6a6a8a"

APP_NAME    = "ZenoxGD Launcher"
APP_VERSION = "1.0.0"
APP_AUTHOR  = "SONI"

# ═══════════════════════════════════════════════════════════════
#  DEFAULT PATHS  (Windows)
# ═══════════════════════════════════════════════════════════════
GD_EXE_DEFAULT   = r"C:\Program Files (x86)\Steam\steamapps\common\Geometry Dash\GeometryDash.exe"
GD_DIR_DEFAULT   = r"C:\Program Files (x86)\Steam\steamapps\common\Geometry Dash"
TEXTURE_URL      = "https://www.youtube.com/@SolubleHD"
GD_ACCOUNT_URL   = "https://www.boomlings.com/dashboard/account"

# ═══════════════════════════════════════════════════════════════
#  CONFIG PERSISTENCE  (saves last used path)
# ═══════════════════════════════════════════════════════════════
CONFIG_FILE = Path(os.getenv("APPDATA", "")) / "ZenoxGD" / "config.json"


def load_config():
    """Load saved configuration (GD path, etc.)."""
    defaults = {"gd_exe": GD_EXE_DEFAULT, "gd_dir": GD_DIR_DEFAULT}
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                defaults.update(data)
    except Exception:
        pass
    return defaults


def save_config(gd_exe, gd_dir):
    """Save configuration to AppData."""
    try:
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump({"gd_exe": gd_exe, "gd_dir": gd_dir}, f, indent=2)
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════════
#  NEON BUTTON  - custom widget with glow on hover
# ═══════════════════════════════════════════════════════════════
class NeonButton(ctk.CTkButton):
    """Button with neon glow effect on hover."""

    def __init__(self, master, text="", command=None, icon="",
                 neon_color=NEON_PURPLE, font_size=18, height=52, **kw):
        label = f"{icon}  {text}" if icon else text
        super().__init__(
            master,
            text=label,
            command=command,
            font=ctk.CTkFont(family="Consolas", size=font_size, weight="bold"),
            fg_color="transparent",
            hover_color=BG_HOVER,
            border_width=2,
            border_color=neon_color,
            text_color=neon_color,
            corner_radius=12,
            height=height,
            **kw
        )
        self._neon = neon_color
        self._dim  = BG_CARD
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, _):
        self.configure(fg_color=self._dim, text_color=self._neon,
                       border_color=self._neon)

    def _on_leave(self, _):
        self.configure(fg_color="transparent", text_color=self._neon,
                       border_color=self._neon)


# ═══════════════════════════════════════════════════════════════
#  PLAY BUTTON  - huge primary launch button
# ═══════════════════════════════════════════════════════════════
class PlayButton(ctk.CTkButton):
    """Huge primary PLAY button."""

    def __init__(self, master, command=None, **kw):
        super().__init__(
            master,
            text="JUGAR  DASH",
            command=command,
            font=ctk.CTkFont(family="Consolas", size=24, weight="bold"),
            fg_color=NEON_RED,
            text_color="#ffffff",
            corner_radius=16,
            height=72,
            border_width=0,
            **kw
        )
        self.bind("<Enter>", self._pulse_on)
        self.bind("<Leave>", self._pulse_off)

    def _pulse_on(self, _):
        self.configure(fg_color=NEON_PURPLE, text_color="#ffffff")

    def _pulse_off(self, _):
        self.configure(fg_color=NEON_RED, text_color="#ffffff")


# ═══════════════════════════════════════════════════════════════
#  ZENOX REPAIR WINDOW
# ═══════════════════════════════════════════════════════════════
class ZenoxRepairWindow(ctk.CTkToplevel):
    """ZenoxRepair - Diagnostic & Repair tool for Geometry Dash."""

    def __init__(self, master, gd_dir=GD_DIR_DEFAULT):
        super().__init__(master)
        self.title("ZenoxRepair - Herramienta de Reparacion")
        self.geometry("580x680")
        self.configure(fg_color=BG_DARK)
        self.resizable(False, False)
        self.grab_set()

        self.gd_dir = gd_dir

        # ── Header ───────────────────────────────────────
        hdr = ctk.CTkLabel(
            self, text="ZENOXREPAIR",
            font=ctk.CTkFont("Consolas", 22, "bold"),
            text_color=NEON_CYAN
        )
        hdr.pack(pady=(18, 4))

        sub = ctk.CTkLabel(
            self, text="Herramienta de diagnostico y reparacion para GD",
            font=ctk.CTkFont("Consolas", 11), text_color=TEXT_DIM
        )
        sub.pack(pady=(0, 6))

        # ── GD dir path selector ─────────────────────────
        dir_frame = ctk.CTkFrame(self, fg_color="transparent")
        dir_frame.pack(fill="x", padx=24, pady=(0, 10))

        ctk.CTkLabel(
            dir_frame, text="Carpeta de GD:",
            font=ctk.CTkFont("Consolas", 10), text_color=TEXT_DIM
        ).pack(side="left")

        self.dir_var = tk.StringVar(value=self.gd_dir)
        ctk.CTkEntry(
            dir_frame, textvariable=self.dir_var,
            font=ctk.CTkFont("Consolas", 10),
            fg_color="#0d0d1a", border_color=NEON_CYAN,
            border_width=1, text_color=TEXT_WHITE,
            height=28, corner_radius=6, width=300
        ).pack(side="left", padx=6)

        ctk.CTkButton(
            dir_frame, text="...", width=36, height=28,
            font=ctk.CTkFont("Consolas", 10, "bold"),
            fg_color="transparent", hover_color=BG_HOVER,
            border_width=1, border_color=NEON_CYAN,
            text_color=NEON_CYAN, corner_radius=6,
            command=self._change_gd_dir
        ).pack(side="left")

        # ── Log area ─────────────────────────────────────
        self.log_box = ctk.CTkTextbox(
            self, height=220, width=530,
            font=ctk.CTkFont("Consolas", 11),
            fg_color="#0d0d18",
            border_color=NEON_CYAN, border_width=1,
            text_color=NEON_GREEN
        )
        self.log_box.pack(padx=20, pady=6)
        self.log_box.insert("end", "  ZenoxRepair v1.0 - Listo.\n")
        self.log_box.configure(state="disabled")

        # ── Repair Buttons ───────────────────────────────
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=8, padx=20, fill="x")

        repairs = [
            ("\u2003\u2003Verificar Archivos GD\u2003\u2003",   self._verify_files,  NEON_CYAN),
            ("\u2003\u2003Limpiar Cache\u2003\u2003",             self._clear_cache,   NEON_GREEN),
            ("\u2003\u2003Restablecer Preferencias\u2003\u2003", self._reset_prefs,   NEON_PURPLE),
            ("\u2003\u2003Abrir Carpeta de GD\u2003\u2003",     self._open_gd_dir,   NEON_RED),
            ("\u2003\u2003Estado de Integridad\u2003\u2003",     self._health_check,  NEON_CYAN),
        ]

        for idx, (label, cmd, color) in enumerate(repairs):
            b = NeonButton(btn_frame, text=label, command=cmd,
                           neon_color=color, font_size=13, height=42)
            b.grid(row=idx, column=0, pady=4, padx=10, sticky="ew")

        # ── Close ────────────────────────────────────────
        ctk.CTkButton(
            self, text="Cerrar", command=self.destroy,
            font=ctk.CTkFont("Consolas", 13, "bold"),
            fg_color="transparent", hover_color=BG_HOVER,
            border_width=1, border_color=NEON_RED,
            text_color=NEON_RED, corner_radius=10
        ).pack(pady=(8, 16))

    # ── helpers ───────────────────────────────────────────
    def _log(self, msg):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"  {msg}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def _gd_path(self, *parts):
        return Path(self.gd_dir).joinpath(*parts)

    def _change_gd_dir(self):
        folder = filedialog.askdirectory(
            title="Selecciona la carpeta de Geometry Dash",
            initialdir=self.gd_dir if Path(self.gd_dir).exists() else "C:/"
        )
        if folder:
            self.gd_dir = folder
            self.dir_var.set(folder)
            self._log(f"Carpeta actualizada: {folder}")

    # ── repair actions ───────────────────────────────────
    def _verify_files(self):
        self._log("")
        self._log("======= VERIFICACION DE ARCHIVOS =======")
        gd = Path(self.gd_dir)
        if not gd.exists():
            self._log("[CRITICO] La carpeta de GD no existe!")
            self._log("========================================")
            return

        checks = [
            ("GeometryDash.exe",       "Ejecutable principal"),
            ("ViewController.dll",     "Libreria de interfaz"),
            ("steam_api.dll",          "Integracion Steam"),
            ("Resources",              "Carpeta de recursos"),
            ("Shaders",                "Carpeta de shaders"),
        ]

        for name, desc in checks:
            p = gd / name
            if p.exists():
                size_info = ""
                if p.is_file():
                    mb = p.stat().st_size / (1024 * 1024)
                    size_info = f" ({mb:.1f} MB)"
                self._log(f"  [OK] {name} - {desc}{size_info}")
            else:
                self._log(f"  [!!] {name} AUSENTE - {desc}")

        self._log("========================================")

    def _clear_cache(self):
        self._log("")
        self._log("======= LIMPIEZA DE CACHE =======")
        cleared = 0
        errors = 0

        # Steam cloud / local app data caches
        cache_locations = [
            Path(os.getenv("LOCALAPPDATA", "")) / "GeometryDash",
            Path(os.getenv("APPDATA", "")) / "GeometryDash",
        ]

        for cache_dir in cache_locations:
            if not cache_dir.exists():
                self._log(f"  Carpeta no encontrada: {cache_dir}")
                continue
            self._log(f"  Escaneando: {cache_dir}")
            for pattern in ["*.dat", "*.tmp", "*.log"]:
                for f in cache_dir.rglob(pattern):
                    try:
                        f.unlink()
                        cleared += 1
                        self._log(f"    Eliminado: {f.name}")
                    except Exception as e:
                        errors += 1
                        self._log(f"    Error: {f.name} - {e}")

        self._log(f"  Resultado: {cleared} eliminados, {errors} errores")
        self._log("==================================")

    def _reset_prefs(self):
        self._log("")
        self._log("======= RESTABLECER PREFERENCIAS =======")
        reset = 0

        pref_locations = [
            Path(os.getenv("APPDATA", "")) / "GeometryDash",
            Path(self.gd_dir),
        ]

        for loc in pref_locations:
            if not loc.exists():
                continue
            for pref_name in ["prefs", "local_prefs", "GD_prefs"]:
                candidate = loc / pref_name
                if candidate.exists():
                    try:
                        bak = candidate.with_suffix(".zenox.bak")
                        # Remove old backup if exists
                        if bak.exists():
                            bak.unlink()
                        candidate.replace(bak)
                        self._log(f"  [OK] {pref_name} respaldado como {bak.name}")
                        reset += 1
                    except Exception as e:
                        self._log(f"  [!!] Error con {pref_name}: {e}")

        if reset == 0:
            self._log("  No se encontraron preferencias para restablecer.")
            self._log("  Sugerencia: Ejecuta GD una vez para generar las prefs.")
        else:
            self._log(f"  {reset} archivo(s) restablecidos correctamente.")
        self._log("========================================")

    def _open_gd_dir(self):
        self._log("")
        self._log(f"  Abriendo carpeta: {self.gd_dir}")
        gd = Path(self.gd_dir)
        if gd.exists():
            os.startfile(str(gd))
        else:
            self._log("  Carpeta no encontrada. Selecciona manualmente.")
            folder = filedialog.askdirectory(
                title="Selecciona la carpeta de Geometry Dash")
            if folder:
                self.gd_dir = folder
                self.dir_var.set(folder)
                os.startfile(folder)

    def _health_check(self):
        self._log("")
        self._log("======= ESTADO DE INTEGRIDAD =======")
        gd = Path(self.gd_dir)
        if not gd.exists():
            self._log("  [CRITICO] Carpeta de GD no encontrada")
            self._log("  Solucion: Configura la ruta manualmente")
            self._log("=====================================")
            return

        # Count total files in GD directory
        all_files = list(gd.rglob("*"))
        total_files = len([f for f in all_files if f.is_file()])

        # Check critical files
        critical = [
            "GeometryDash.exe", "ViewController.dll",
            "steam_api.dll", "Resources", "Shaders"
        ]
        total_c = len(critical)
        ok_c = sum(1 for name in critical if (gd / name).exists())

        # Check optional but important files
        optional = [
            "fmodex64.dll", "fmodL64.dll", "avcodec-59.dll",
            "avformat-59.dll", "avutil-57.dll", "swresample-4.dll"
        ]
        total_o = len(optional)
        ok_o = sum(1 for name in optional if (gd / name).exists())

        # Results
        self._log(f"  Archivos en carpeta: {total_files}")
        self._log(f"  Archivos criticos:  {ok_c}/{total_c}")
        self._log(f"  Archivos opcionales: {ok_o}/{total_o}")

        total_all = total_c + total_o
        ok_all = ok_c + ok_o
        pct = (ok_all / total_all * 100) if total_all else 0

        # Size check
        exe = gd / "GeometryDash.exe"
        if exe.exists():
            mb = exe.stat().st_size / (1024 * 1024)
            self._log(f"  Tamano del ejecutable: {mb:.1f} MB")

        # Status bar
        bar_len = 30
        filled = int(pct / 100 * bar_len)
        bar = "\u2588" * filled + "\u2591" * (bar_len - filled)
        self._log(f"  [{bar}] {pct:.0f}%")

        if pct >= 80:
            self._log("  Estado: SALUDABLE")
        elif pct >= 50:
            self._log("  Estado: PARCIAL - Requiere atencion")
        else:
            self._log("  Estado: CRITICO - Reinstalar recomendado")

        self._log("=====================================")


# ═══════════════════════════════════════════════════════════════
#  MAIN LAUNCHER WINDOW
# ═══════════════════════════════════════════════════════════════
class ZenoxGDLauncher(ctk.CTk):
    """Main Launcher Window."""

    def __init__(self):
        super().__init__()

        # ── Load saved config ────────────────────────────
        cfg = load_config()
        self.gd_exe = cfg.get("gd_exe", GD_EXE_DEFAULT)
        self.gd_dir = cfg.get("gd_dir", GD_DIR_DEFAULT)

        # ── Window config ────────────────────────────────
        self.title(f"{APP_NAME}")
        self.geometry("700x760")
        self.configure(fg_color=BG_DARK)
        self.resizable(False, False)

        # ── Center window on screen ──────────────────────
        self.update_idletasks()
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        x = (w - 700) // 2
        y = (h - 760) // 2
        self.geometry(f"700x760+{x}+{y}")

        # ── Set window icon (if bundled) ─────────────────
        ico_path = os.path.join(APPLICATION_PATH, "assets", "icon.ico")
        if os.path.exists(ico_path):
            self.iconbitmap(ico_path)

        self._build_ui()

    # ═══════════════════════════════════════════════════════
    #  UI BUILD
    # ═══════════════════════════════════════════════════════
    def _build_ui(self):

        # ── Background canvas for neon decorations ──────
        canvas = tk.Canvas(self, width=700, height=760,
                           bg=BG_DARK, highlightthickness=0)
        canvas.place(x=0, y=0)

        # Top / bottom neon lines
        canvas.create_line(0, 2, 700, 2, fill=NEON_PURPLE, width=2)
        canvas.create_line(0, 758, 700, 758, fill=NEON_PURPLE, width=2)
        # Side accents
        canvas.create_line(2, 0, 2, 760, fill=NEON_RED, width=1)
        canvas.create_line(698, 0, 698, 760, fill=NEON_RED, width=1)
        # Corner neon dots
        for cx, cy in [(10, 10), (690, 10), (10, 750), (690, 750)]:
            r = 5
            canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
                               fill=NEON_CYAN, outline=NEON_CYAN)
        # Decorative diagonal neon accents (subtle)
        canvas.create_line(0, 0, 60, 60, fill=NEON_PURPLE, width=1,
                           dash=(4, 8))
        canvas.create_line(700, 0, 640, 60, fill=NEON_PURPLE, width=1,
                           dash=(4, 8))

        # ── Main container (over canvas) ────────────────
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.place(relx=0.5, rely=0.5, anchor="center")

        # ── HEADER ───────────────────────────────────────
        title_label = ctk.CTkLabel(
            container,
            text="ZENOX GD LAUNCHER",
            font=ctk.CTkFont("Consolas", 34, "bold"),
            text_color=NEON_PURPLE
        )
        title_label.pack(pady=(8, 0))

        # Creator signature
        creator_label = ctk.CTkLabel(
            container,
            text="Created by SONI",
            font=ctk.CTkFont("Consolas", 13),
            text_color=NEON_CYAN
        )
        creator_label.pack(pady=(2, 2))

        # Neon separator
        sep = ctk.CTkFrame(container, height=2, fg_color=NEON_PURPLE)
        sep.pack(fill="x", padx=50, pady=(6, 14))

        # ── GD PATH CONFIG ROW ──────────────────────────
        path_frame = ctk.CTkFrame(container, fg_color="transparent")
        path_frame.pack(fill="x", padx=36, pady=(0, 6))

        ctk.CTkLabel(
            path_frame, text="Ruta de GeometryDash.exe:",
            font=ctk.CTkFont("Consolas", 11),
            text_color=TEXT_DIM
        ).pack(side="left")

        ctk.CTkButton(
            path_frame, text="Explorar", width=80, height=28,
            font=ctk.CTkFont("Consolas", 10, "bold"),
            fg_color="transparent", hover_color=BG_HOVER,
            border_width=1, border_color=NEON_CYAN,
            text_color=NEON_CYAN, corner_radius=8,
            command=self._browse_exe
        ).pack(side="right")

        self.path_var = tk.StringVar(value=self.gd_exe)
        path_entry = ctk.CTkEntry(
            container, textvariable=self.path_var,
            font=ctk.CTkFont("Consolas", 11),
            fg_color="#0d0d1a", border_color=NEON_CYAN,
            border_width=1, text_color=TEXT_WHITE,
            height=32, corner_radius=8
        )
        path_entry.pack(fill="x", padx=36, pady=(0, 14))

        # ── PLAY BUTTON ──────────────────────────────────
        play_btn = PlayButton(container, command=self._launch_gd)
        play_btn.pack(fill="x", padx=36, pady=(0, 18))

        # ── ACTION BUTTONS ───────────────────────────────
        actions = [
            ("\u2003Texture Packs (Soluble HD)\u2003\u2003\u2003\u2003\u2003\u2003\u2003",
             self._open_texture_packs, NEON_GREEN),
            ("\u2003Herramientas de Creador (ZenoxRepair)\u2003",
             self._open_zenox_repair, NEON_CYAN),
            ("\u2003Cuenta GD (Boomlings)\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003",
             self._open_account, NEON_PURPLE),
        ]

        for text, cmd, color in actions:
            btn = NeonButton(container, text=text, command=cmd,
                              neon_color=color, font_size=15, height=48)
            btn.pack(fill="x", padx=36, pady=5)

        # ── SEPARATOR ────────────────────────────────────
        sep2 = ctk.CTkFrame(container, height=1, fg_color=TEXT_DIM)
        sep2.pack(fill="x", padx=80, pady=(12, 8))

        # ── SECONDARY ACTIONS (smaller) ──────────────────
        sec_frame = ctk.CTkFrame(container, fg_color="transparent")
        sec_frame.pack(fill="x", padx=36, pady=(0, 4))

        sec_actions = [
            ("Configurar Ruta de GD",   self._browse_exe,    NEON_RED),
            ("Abrir Carpeta de GD",     self._open_gd_folder, NEON_RED),
        ]

        for idx, (text, cmd, color) in enumerate(sec_actions):
            btn = NeonButton(sec_frame, text=text, command=cmd,
                              neon_color=color, font_size=12, height=36)
            btn.grid(row=0, column=idx, padx=6, pady=2, sticky="ew")
        sec_frame.grid_columnconfigure((0, 1), weight=1)

        # ── STATUS BAR ──────────────────────────────────
        status_frame = ctk.CTkFrame(container, fg_color="transparent",
                                     height=30)
        status_frame.pack(fill="x", padx=36, pady=(14, 2))

        self.status_var = tk.StringVar(value="Listo.")
        ctk.CTkLabel(
            status_frame, textvariable=self.status_var,
            font=ctk.CTkFont("Consolas", 10),
            text_color=TEXT_DIM
        ).pack(side="left")

        ctk.CTkLabel(
            status_frame, text=f"v{APP_VERSION}  |  {APP_AUTHOR}",
            font=ctk.CTkFont("Consolas", 10),
            text_color=NEON_PURPLE
        ).pack(side="right")

        # ── Footer ───────────────────────────────────────
        ctk.CTkLabel(
            container,
            text="SONI  |  ZenoxGD  |  2025",
            font=ctk.CTkFont("Consolas", 9),
            text_color=TEXT_DIM
        ).pack(pady=(4, 8))

    # ═══════════════════════════════════════════════════════
    #  ACTIONS
    # ═══════════════════════════════════════════════════════
    def _launch_gd(self):
        exe = self.path_var.get().strip('"').strip()
        if not exe:
            self.status_var.set("Ruta no configurada. Selecciona GeometryDash.exe")
            messagebox.showinfo("Configurar ruta",
                "Primero selecciona la ruta de GeometryDash.exe\n"
                "usando el boton 'Explorar' o 'Configurar Ruta'.")
            return
        exe_path = Path(exe)
        if exe_path.exists():
            self.status_var.set("Lanzando Geometry Dash...")
            self.update()
            try:
                subprocess.Popen([str(exe_path)], cwd=str(exe_path.parent))
                self.status_var.set("Geometry Dash lanzado correctamente!")
            except Exception as e:
                self.status_var.set(f"Error al lanzar: {e}")
                messagebox.showerror("Error", f"No se pudo lanzar GD:\n{e}")
        else:
            self.status_var.set("Ejecutable no encontrado. Verifica la ruta.")
            messagebox.showwarning("No encontrado",
                f"No se encontro:\n{exe}\n\n"
                f"Verifica la ruta del ejecutable o busca manualmente.")

    def _browse_exe(self):
        exe = filedialog.askopenfilename(
            title="Selecciona GeometryDash.exe",
            filetypes=[("Ejecutable", "*.exe"), ("Todos", "*.*")],
            initialdir=self.gd_dir if Path(self.gd_dir).exists() else "C:/"
        )
        if exe:
            self.path_var.set(exe)
            self.gd_exe = exe
            self.gd_dir = str(Path(exe).parent)
            self.status_var.set(f"Ruta configurada: {exe}")
            save_config(self.gd_exe, self.gd_dir)

    def _open_texture_packs(self):
        self.status_var.set("Abriendo Texture Packs de Soluble HD...")
        # Open GD Resources folder (where textures live)
        resources = Path(self.gd_dir) / "Resources"
        if resources.exists():
            os.startfile(str(resources))
        else:
            # Try to open GD directory at least
            gd = Path(self.gd_dir)
            if gd.exists():
                os.startfile(str(gd))
        # Also open the Soluble HD channel for downloads
        webbrowser.open(TEXTURE_URL)
        self.status_var.set("Texture Packs - Carpeta y canal de Soluble HD abiertos")

    def _open_zenox_repair(self):
        self.status_var.set("Abriendo ZenoxRepair...")
        ZenoxRepairWindow(self, gd_dir=self.gd_dir)

    def _open_account(self):
        self.status_var.set("Abriendo gestion de cuenta Boomlings...")
        webbrowser.open(GD_ACCOUNT_URL)

    def _open_gd_folder(self):
        self.status_var.set("Abriendo carpeta de Geometry Dash...")
        gd = Path(self.gd_dir)
        if gd.exists():
            os.startfile(str(gd))
        else:
            folder = filedialog.askdirectory(
                title="Selecciona la carpeta de Geometry Dash")
            if folder:
                self.gd_dir = folder
                self.gd_exe = str(Path(folder) / "GeometryDash.exe")
                self.path_var.set(self.gd_exe)
                os.startfile(folder)
                save_config(self.gd_exe, self.gd_dir)


# ═══════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════
def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ZenoxGDLauncher()

    # Save config on close
    def on_closing():
        save_config(app.gd_exe, app.gd_dir)
        app.destroy()

    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()


if __name__ == "__main__":
    main()
