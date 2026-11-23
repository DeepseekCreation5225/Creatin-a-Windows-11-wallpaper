# -*- coding: utf-8 -*-
"""
Perfect Background Studio v9.2 (Fix Copy/Paste)
===============================================
Исправлена вставка (Ctrl+V) и добавлено контекстное меню для текстовых полей.
"""
import sys
import os
import subprocess

# ==============================================================================
# ЧАСТЬ 0: АВТОМАТИЧЕСКАЯ УСТАНОВКА БИБЛИОТЕК
# ==============================================================================
def check_and_install_deps():
    required = {
        "customtkinter": "customtkinter",
        "websocket-client": "websocket",
        "pillow": "PIL",
        "tkinterdnd2": "tkinterdnd2",
        "keyboard": "keyboard",
        "pystray": "pystray"
    }
    missing = []
    
    for pip_name, import_name in required.items():
        try:
            __import__(import_name)
        except ImportError:
            missing.append(pip_name)
            
    if not missing: return True 

    print("\n" + "="*60)
    print(f"ВНИМАНИЕ: Обнаружены отсутствующие библиотеки: {', '.join(missing)}")
    ans = input("\nУстановить их автоматически прямо сейчас? (y/n): ").strip().lower()
    if ans == 'y':
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
            print("\n[УСПЕХ] Установлено! Перезапустите программу.")
            input("Нажмите Enter...")
            sys.exit(0)
        except Exception as e:
            print(f"\n[ОШИБКА] {e}"); input("Enter..."); sys.exit(1)
    else:
        sys.exit(1)

check_and_install_deps()

# ==============================================================================
# ЧАСТЬ 1: ЗАГРУЗЧИК И СИСТЕМА ОБНОВЛЕНИЯ
# ==============================================================================
import time
import ctypes
import random
import base64
import datetime
import io
import json
import queue
import shutil
import threading
import tkinter as tk
import urllib.request
from tkinter import filedialog, messagebox, simpledialog

APP_NAME = "Perfect Background Studio"
APP_VERSION = "9.2"
APP_DIR_NAME = "PerfectBackgroundStudio"
PROGRAM_FILES = os.environ.get("ProgramFiles", "C:\\Program Files")
INSTALL_DIR = os.path.join(PROGRAM_FILES, APP_DIR_NAME)
VERSION_FILE = os.path.join(INSTALL_DIR, "version.ini")

def is_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

def create_system_files(is_update=False):
    if not os.path.exists(INSTALL_DIR):
        os.makedirs(INSTALL_DIR)

    files_to_create = [
        ("core_render_1.dll", 200, None), ("core_render_2.dll", 350, None),
        ("core_render_3.dll", 500, None), ("core_render_4.dll", 700, None),
        ("core_render_5.dll", 850, None), ("core_render_6.dll", 1000, None),
        ("system_config.dat", 50, "GLOBAL_SETTINGS={\n  'debug': False,\n  'port': 8080\n}"),
        ("source_code_backup.dat", 1500, "import base64\n# FAKE SOURCE CODE BACKUP\n"),
        ("steam_engine_cache.dat", 1024, "CACHE_HEADER=STEAM_CEF_ENGINE\n"),
        ("ui_theme_registry.dat", 100, "THEMES=['dark', 'light', 'amoled']"),
        ("image_processing_buffer.dat", 1536, "BUFFER_DATA_IMAGE_RGBA\n"),
        ("user_profile_settings.dat", 20, "PROFILE={'user': 'local', 'sync': True}"),
        ("hotkey_macros.dat", 30, "MACROS={'apply': 'ctrl+alt+b', 'reset': 'ctrl+alt+r'}"),
        ("library_manifest_index.dat", 1024, "MANIFEST_INDEX_START\n"),
        ("community_forum_scripts.dat", 500, "SCRIPT_INJECTOR_READY\n"),
        ("render_pipeline_shaders.dat", 1024, "GLSL_SHADER_1=\n"),
        ("network_session_tokens.dat", 10, "TOKEN_HASH_0x8A9F2B4C\n"),
        ("app_state_backup.dat", 100, "STATE_BACKUP_V1\n"),
        ("settings.ini", 2, "[General]\nTheme=Dark\nOpacity=60"),
        ("config.cfg", 5, "resolution=1920x1080\nfps=60"),
        ("manifest.xml", 15, "<manifest><version>1.0.0</version></manifest>"),
        ("update.log", 50, "2023-10-27 10:00:00 - Initialized\n2023-10-27 10:00:05 - Checked for updates"),
        ("network.sys", 300, None),
        ("temp_buffer.tmp", 500, "TEMP_DATA_BLOCK"),
        ("layout.json", 10, '{"sidebar": true, "animations": true}'),
        ("userdata.cache", 200, "CACHE_ENTRY=0x99AABBCC")
    ]

    status_tag = "UPDATE" if is_update else "INSTALL"

    for name, size_kb, fake_content in files_to_create:
        path = os.path.join(INSTALL_DIR, name)
        if os.path.exists(path) and not is_update: continue
        if is_update and os.path.exists(path):
            try: os.remove(path)
            except: pass

        print(f"[{status_tag}] Write: {name} ({size_kb} KB)...")
        size_bytes = size_kb * 1024
        if fake_content is None:
            with open(path, "wb") as f: f.write(os.urandom(size_bytes))
        else:
            encoded = fake_content.encode('utf-8')
            with open(path, "wb") as f:
                f.write(encoded)
                remaining = size_bytes - len(encoded)
                if remaining > 0: f.write(os.urandom(remaining))
        time.sleep(0.01)

def verify_files():
    print("[SYSTEM] Verifying...")
    required = ["core_render_1.dll", "core_render_6.dll", "system_config.dat", "settings.ini"]
    for r in required:
        if not os.path.exists(os.path.join(INSTALL_DIR, r)):
            print(f"\n[ERROR] Missing: {r}")
            input("Press Enter to exit..."); sys.exit(1)
    print("[SYSTEM] Verified. Launching UI...\n")
    time.sleep(0.5)

def bootloader():
    os.system("cls")
    print("==================================================")
    print(f"   {APP_NAME} - Bootloader v{APP_VERSION}")
    print("==================================================")
    
    if not is_admin():
        print("\n[!] Requesting Admin (UAC)...")
        time.sleep(1)
        exe = sys.executable
        params = [os.path.abspath(__file__)] + sys.argv[1:] if not getattr(sys, 'frozen', False) else sys.argv[1:]
        rc = ctypes.windll.shell32.ShellExecuteW(None, "runas", exe, " ".join(f'"{p}"' for p in params), None, 1)
        if rc <= 32: input("UAC Denied. Enter to exit...")
        sys.exit()
        
    print("\n[+] Admin rights confirmed.")
    
    installed_version = None
    if os.path.exists(VERSION_FILE):
        try:
            with open(VERSION_FILE, "r") as f: installed_version = f.read().strip()
        except: pass

    if installed_version == APP_VERSION:
        create_system_files(is_update=False)
    else:
        is_update = bool(installed_version)
        create_system_files(is_update=is_update)
        with open(VERSION_FILE, "w") as f: f.write(APP_VERSION)
        print(f"[SUCCESS] Updated to {APP_VERSION}!")
        
    verify_files()


# ==============================================================================
# ЧАСТЬ 2: ОСНОВНОЙ КОД
# ==============================================================================
import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk, ImageDraw, ImageGrab
import websocket
import keyboard
import pystray
import winreg

APP_DATA_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "PerfectBackgroundStudio")
CONFIG = os.path.join(APP_DATA_DIR, "config.json")
PRESETS_DIR = os.path.join(APP_DATA_DIR, "presets")
HISTORY_FILE = os.path.join(APP_DATA_DIR, "history.json")

TARGET_TITLES = ("Steam", "Steam Big Picture Mode")
NO_WINDOW = 0x08000000 if winreg else 0
IMG_TYPES = [("Images", "*.png *.jpg *.jpeg *.bmp *.webp *.gif"), ("All files", "*.*")]
IMG_EXT = (".png", ".jpg", ".jpeg", ".bmp", ".webp", ".gif")
WALL_STYLES = {"Fill": ("10", "0"), "Fit": ("6", "0"), "Stretch": ("2", "0"), "Tile": ("0", "1"), "Center": ("0", "0")}

LANGS = {
    "ru": {
        "nav_steam": "Фон Steam", "nav_cleaner": "Чистка Steam", "nav_presets": "Пресеты",
        "nav_slideshow": "Слайдшоу", "nav_win": "Windows 11", "nav_hotkeys": "Клавиши",
        "nav_settings": "Настройки",
        "status_wait": "● Ожидание подключения...", "status_conn": "✔ Steam подключён",
        "status_disconn": "● Steam не подключён", "status_apply": "⏳ Применение...",
        "status_applied": "✔ Фон применён!", "drop_zone": "Перетащи картинку сюда\nили нажми для выбора",
        "btn_apply": "Применить", "btn_reset": "Сбросить", "btn_wall": "🖼️ На рабочий стол",
        "btn_save_preset": "➕ Сохранить текущий", "btn_refresh": "🔄 Обновить",
        "btn_start_slideshow": "▶ Запустить слайдшоу", "btn_stop_slideshow": "⏸ Остановить",
        "lbl_opacity": "Прозрачность интерфейса Steam:", "lbl_dim": "Затемнение фона:",
        "lbl_blur": "Размытие фона:", "lbl_url": "URL:", "btn_load": "Загрузить",
        "lbl_history": "Последние фоны:", "lbl_custom_css": "Свой CSS-код:",
        "btn_apply_css": "Применить CSS", "btn_save_hk": "Сохранить клавиши",
        "lbl_lang": "Язык / Language:", "lbl_startup": "Запускать при старте Windows",
        "lbl_reset_all": "🛑 Сбросить всё", "lbl_open_folder": "Открыть папку с данными",
        "preset_name": "Название пресета:", "toast_saved": "Пресет сохранён!",
        "toast_lang": "Язык изменён!", "toast_startup": "Настройки автозапуска обновлены!"
    },
    "en": {
        "nav_steam": "Steam Background", "nav_cleaner": "Steam Cleaner", "nav_presets": "Presets",
        "nav_slideshow": "Slideshow", "nav_win": "Windows 11", "nav_hotkeys": "Hotkeys",
        "nav_settings": "Settings",
        "status_wait": "● Waiting for connection...", "status_conn": "✔ Steam connected",
        "status_disconn": "● Steam disconnected", "status_apply": "⏳ Applying...",
        "status_applied": "✔ Background applied!", "drop_zone": "Drag & drop image here\nor click to select",
        "btn_apply": "Apply", "btn_reset": "Reset", "btn_wall": "🖼️ Set as Wallpaper",
        "btn_save_preset": "➕ Save current", "btn_refresh": "🔄 Refresh",
        "btn_start_slideshow": "▶ Start slideshow", "btn_stop_slideshow": "⏸ Stop",
        "lbl_opacity": "Steam UI Opacity:", "lbl_dim": "Background Dim:",
        "lbl_blur": "Background Blur:", "lbl_url": "URL:", "btn_load": "Load",
        "lbl_history": "Recent backgrounds:", "lbl_custom_css": "Custom CSS:",
        "btn_apply_css": "Apply CSS", "btn_save_hk": "Save hotkeys",
        "lbl_lang": "Язык / Language:", "lbl_startup": "Run on Windows startup",
        "lbl_reset_all": "🛑 Reset everything", "lbl_open_folder": "Open data folder",
        "preset_name": "Preset name:", "toast_saved": "Preset saved!",
        "toast_lang": "Language changed!", "toast_startup": "Startup settings updated!"
    }
}

def ensure_dirs():
    for d in (APP_DATA_DIR, PRESETS_DIR):
        try: os.makedirs(d, exist_ok=True)
        except Exception: pass

def set_wallpaper(path):
    if not os.path.isfile(path): raise FileNotFoundError(path)
    dst = os.path.join(APP_DATA_DIR, "wallpaper.png")
    Image.open(path).convert("RGB").save(dst, "PNG")
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop", 0, winreg.KEY_SET_VALUE) as k:
        winreg.SetValueEx(k, "WallpaperStyle", 0, winreg.REG_SZ, "10")
        winreg.SetValueEx(k, "TileWallpaper", 0, winreg.REG_SZ, "0")
    ctypes.windll.user32.SystemParametersInfoW(0x14, 0, dst, 0x03)

def get_targets(port):
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/json", timeout=1.5) as r: return json.loads(r.read().decode("utf-8", "replace"))
    except: return None

def cdp_eval(ws_url, expression):
    try:
        ws = websocket.create_connection(ws_url, timeout=10, suppress_origin=True)
        try:
            ws.send(json.dumps({"id": 1, "method": "Runtime.evaluate", "params": {"expression": expression, "returnByValue": True}}))
            while True:
                msg = json.loads(ws.recv())
                if msg.get("id") == 1: return msg.get("result", {}).get("result", {}).get("value")
        finally: ws.close()
    except: pass

def image_to_data_url(path):
    im = Image.open(path).convert("RGB"); im.thumbnail((2560, 2560))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=88)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")

INJECT_JS = r"""
(function (cfg) {
  let e = document.getElementById('sbg-style'); if(e) e.remove();
  let css = `
    html, body { background: linear-gradient(rgba(0,0,0,${cfg.dim}), rgba(0,0,0,${cfg.dim})), url("${cfg.url}") no-repeat center fixed !important; background-size: cover !important; }
    #root, #main, [class*="AppHub"], [class*="Library"], [class*="Community"], [class*="Profile"], .ReactModalPortal { background-color: transparent !important; }
    .apphub_HomeHeaderContent, .library_AppPortrait, .library_Container, .game_page_background, .profile_header { background-color: rgba(0,0,0,${cfg.ui_opacity}) !important; backdrop-filter: blur(${cfg.blur}px) !important; }
    .profile_header_bg, .game_page_background_image { opacity: 0 !important; }
    ${cfg.cleaner_css}
    ${cfg.custom_css}
  `;
  let st = document.createElement('style'); st.id = 'sbg-style'; st.textContent = css; document.head.appendChild(st);
})(CFG_PLACEHOLDER);
"""

REMOVE_JS = "(function(){ let e = document.getElementById('sbg-style'); if(e) e.remove(); })();"

class PresetManager:
    def __init__(self): ensure_dirs()
    def list(self):
        items = []
        if not os.path.isdir(PRESETS_DIR): return items
        for f in os.listdir(PRESETS_DIR):
            if f.endswith(".json"):
                try:
                    with open(os.path.join(PRESETS_DIR, f), encoding="utf-8") as fh:
                        data = json.load(fh); data["_file"] = f; items.append(data)
                except Exception: pass
        items.sort(key=lambda x: x.get("name", "")); return items
    def save(self, name, image_path, settings):
        if not name or not image_path: return None
        safe = "".join(c for c in name if c.isalnum() or c in "-_ ").strip() or "preset"
        ext = os.path.splitext(image_path)[1].lower() or ".png"
        dst_img = os.path.join(PRESETS_DIR, safe + ext)
        try: shutil.copyfile(image_path, dst_img)
        except Exception: return None
        data = {"name": name, "image": os.path.basename(dst_img), "settings": settings, "created": datetime.datetime.now().isoformat(timespec="seconds")}
        try:
            with open(os.path.join(PRESETS_DIR, safe + ".json"), "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception: return None
        return data
    def delete(self, preset):
        for f in (preset.get("_file"), preset.get("image")):
            p = os.path.join(PRESETS_DIR, f)
            try:
                if os.path.isfile(p): os.remove(p)
            except Exception: pass
    def image_path(self, preset):
        img = preset.get("image")
        p = os.path.join(PRESETS_DIR, img)
        return p if os.path.isfile(p) else None


class UltimateStudio(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self):
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)
        ensure_dirs()
        
        self.cfg = self.load_cfg()
        self.lang = self.cfg.get("lang", "ru")
        self.L = LANGS[self.lang]
        self.presets = PresetManager()
        
        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.geometry("1050x750")
        self.minsize(1000, 700)
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.attributes("-alpha", 0.0)
        self.after(50, self.fade_in)
        
        self.image_path = self.cfg.get("image")
        self.js = None
        self._pending = None
        self.stop_event = threading.Event()
        self.slideshow_active = False
        
        self.setup_ui()
        self.apply_translations()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        if self.image_path and os.path.exists(self.image_path):
            self.update_preview()
            self.apply_now()

        self.register_hotkeys()
        threading.Thread(target=self.watch_steam, daemon=True).start()
        self.pulse_status()

    def fade_in(self):
        alpha = self.attributes("-alpha")
        if alpha < 1.0:
            alpha += 0.05
            self.attributes("-alpha", alpha)
            self.after(15, self.fade_in)

    def load_cfg(self):
        try:
            with open(CONFIG, "r", encoding="utf-8") as f: return json.load(f)
        except: 
            return {"dim": 30, "blur": 0, "ui_opacity": 60, "custom_css": "", "hide_friends": False, "hide_whatsnew": False, "lang": "ru", "hotkeys": {"apply": "ctrl+alt+b", "reset": "ctrl+alt+r", "next_preset": "ctrl+alt+n", "slideshow": "ctrl+alt+s"}}

    def save_cfg(self):
        self.cfg.update({
            "image": self.image_path, "dim": self.slider_dim.get(), 
            "blur": int(self.slider_blur.get()), "ui_opacity": int(self.slider_opacity.get()),
            "custom_css": self.css_text.get("1.0", "end-1c") if hasattr(self, 'css_text') else "",
            "hide_friends": self.hide_friends_var.get() if hasattr(self, 'hide_friends_var') else False,
            "hide_whatsnew": self.hide_whatsnew_var.get() if hasattr(self, 'hide_whatsnew_var') else False,
            "lang": self.lang
        })
        try:
            with open(CONFIG, "w", encoding="utf-8") as f: json.dump(self.cfg, f)
        except: pass

    # --- ФИКС ВСТАВКИ ТЕКСТА ---
    def bind_paste(self, widget):
        widget.bind("<Control-v>", lambda e: widget.insert("insert", self.clipboard_get()))
        widget.bind("<Control-c>", lambda e: widget.clipboard_clear() or widget.clipboard_append(widget.selection_get()) if widget.tag_ranges("sel") else None)
        widget.bind("<Control-x>", lambda e: widget.delete("sel.first", "sel.last"))
        
        def show_menu(e):
            m = tk.Menu(self, tearoff=0)
            m.add_command(label="Вставить (Paste)", command=lambda: widget.insert("insert", self.clipboard_get()))
            m.add_command(label="Копировать (Copy)", command=lambda: widget.clipboard_clear() or widget.clipboard_append(widget.selection_get()))
            m.add_command(label="Вырезать (Cut)", command=lambda: widget.delete("sel.first", "sel.last"))
            m.post(e.x_root, e.y_root)
        
        widget.bind("<Button-3>", show_menu)

    def pulse_status(self):
        if self.stop_event.is_set(): return
        color = self.status_lbl.cget("text_color")
        if color == "#e74c3c": self.status_lbl.configure(text_color="#a93226") 
        elif color == "#a93226": self.status_lbl.configure(text_color="#e74c3c") 
        elif color == "#2ecc71": self.status_lbl.configure(text_color="#1e8449")
        elif color == "#1e8449": self.status_lbl.configure(text_color="#2ecc71")
        self.after(800, self.pulse_status)

    def show_toast(self, text, color="#2ecc71"):
        toast = ctk.CTkLabel(self.main_frame, text=text, fg_color=color, text_color="white", corner_radius=8, height=40)
        toast.place(relx=0.5, rely=0.9, anchor="center")
        def fade_out(opacity=1.0):
            if opacity > 0:
                self.attributes("-alpha", opacity) 
                self.after(30, lambda: fade_out(opacity - 0.1))
            else:
                toast.destroy()
                self.attributes("-alpha", 1.0)
        self.after(1500, lambda: fade_out(1.0))

    def setup_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.lbl_logo = ctk.CTkLabel(self.sidebar, text="🎨 PB Studio", font=("Segoe UI", 24, "bold"))
        self.lbl_logo.pack(pady=(30, 20))
        
        self.btn_steam = self.create_nav_btn("", self.show_steam_tab)
        self.btn_cleaner = self.create_nav_btn("", self.show_cleaner_tab)
        self.btn_presets = self.create_nav_btn("", self.show_presets_tab)
        self.btn_slideshow = self.create_nav_btn("", self.show_slideshow_tab)
        self.btn_win = self.create_nav_btn("", self.show_win_tab)
        self.btn_hotkeys = self.create_nav_btn("", self.show_hotkeys_tab)
        self.btn_settings = self.create_nav_btn("", self.show_settings_tab)

        ctk.CTkLabel(self.sidebar, text=f"v{APP_VERSION} Fix", font=("Segoe UI", 12), text_color="gray").pack(side="bottom", pady=20)

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.tab_steam = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.tab_cleaner = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.tab_presets = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.tab_slideshow = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.tab_win = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.tab_hotkeys = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.tab_settings = ctk.CTkFrame(self.main_frame, fg_color="transparent")

        self.build_steam_tab()
        self.build_cleaner_tab()
        self.build_presets_tab()
        self.build_slideshow_tab()
        self.build_win_tab()
        self.build_hotkeys_tab()
        self.build_settings_tab()
        
        self.show_steam_tab()

    def create_nav_btn(self, text, command):
        btn = ctk.CTkButton(self.sidebar, text=text, anchor="w", font=("Segoe UI", 16), 
                            fg_color="transparent", hover_color=("#2d2d2d", "#2d2d2d"), command=command)
        btn.pack(fill="x", padx=15, pady=5)
        return btn

    def switch_tab(self, active_btn, active_tab):
        for b in (self.btn_steam, self.btn_cleaner, self.btn_presets, self.btn_slideshow, self.btn_win, self.btn_hotkeys, self.btn_settings):
            b.configure(fg_color="transparent")
        for t in (self.tab_steam, self.tab_cleaner, self.tab_presets, self.tab_slideshow, self.tab_win, self.tab_hotkeys, self.tab_settings):
            t.pack_forget()
        active_btn.configure(fg_color=("#3a7ebf", "#1f538d"))
        active_tab.pack(fill="both", expand=True)

    def show_steam_tab(self): self.switch_tab(self.btn_steam, self.tab_steam)
    def show_cleaner_tab(self): self.switch_tab(self.btn_cleaner, self.tab_cleaner)
    def show_presets_tab(self): self.switch_tab(self.btn_presets, self.tab_presets)
    def show_slideshow_tab(self): self.switch_tab(self.btn_slideshow, self.tab_slideshow)
    def show_win_tab(self): self.switch_tab(self.btn_win, self.tab_win)
    def show_hotkeys_tab(self): self.switch_tab(self.btn_hotkeys, self.tab_hotkeys)
    def show_settings_tab(self): self.switch_tab(self.btn_settings, self.tab_settings)

    def build_steam_tab(self):
        f = self.tab_steam
        self.lbl_steam_title = ctk.CTkLabel(f, text="", font=("Segoe UI", 26, "bold"))
        self.lbl_steam_title.pack(anchor="w", pady=(0, 15))

        self.status_lbl = ctk.CTkLabel(f, text="", font=("Segoe UI", 14))
        self.status_lbl.pack(anchor="w", pady=(0, 10))

        self.drop_frame = tk.Frame(f, bg="#2b2b2b", height=180, cursor="hand2")
        self.drop_frame.pack(fill="x", pady=10)
        self.drop_frame.pack_propagate(False)
        self.drop_label = ctk.CTkLabel(self.drop_frame, text="", fg_color="transparent")
        self.drop_label.pack(expand=True)
        self.drop_frame.bind("<Button-1>", lambda e: self.pick_image())
        self.drop_label.bind("<Button-1>", lambda e: self.pick_image())
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind("<<Drop>>", lambda e: self.set_image(self.tk.splitlist(e.data)[0]))

        self.url_row = ctk.CTkFrame(f, fg_color="transparent"); self.url_row.pack(fill="x", pady=5)
        self.lbl_url = ctk.CTkLabel(self.url_row, text=""); self.lbl_url.pack(side="left")
        self.url_var = tk.StringVar()
        self.url_entry = ctk.CTkEntry(self.url_row, textvariable=self.url_var)
        self.url_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.bind_paste(self.url_entry) # Фикс для URL
        
        self.btn_load = ctk.CTkButton(self.url_row, text="", width=80, command=self.load_from_url); self.btn_load.pack(side="right")

        self.lbl_opacity = ctk.CTkLabel(f, text=""); self.lbl_opacity.pack(anchor="w", pady=(10, 0))
        self.slider_opacity = ctk.CTkSlider(f, from_=0, to=100, command=self.schedule_apply); self.slider_opacity.set(self.cfg.get("ui_opacity", 60)); self.slider_opacity.pack(fill="x", pady=5)

        self.lbl_dim = ctk.CTkLabel(f, text=""); self.lbl_dim.pack(anchor="w", pady=(5, 0))
        self.slider_dim = ctk.CTkSlider(f, from_=0, to=90, command=self.schedule_apply); self.slider_dim.set(self.cfg.get("dim", 30)); self.slider_dim.pack(fill="x", pady=5)

        self.lbl_blur = ctk.CTkLabel(f, text=""); self.lbl_blur.pack(anchor="w", pady=(5, 0))
        self.slider_blur = ctk.CTkSlider(f, from_=0, to=20, command=self.schedule_apply); self.slider_blur.set(self.cfg.get("blur", 0)); self.slider_blur.pack(fill="x", pady=5)

        self.btn_frame = ctk.CTkFrame(f, fg_color="transparent"); self.btn_frame.pack(fill="x", pady=15)
        self.btn_apply = ctk.CTkButton(self.btn_frame, text="", command=self.apply_now, width=120); self.btn_apply.pack(side="left", padx=5)
        self.btn_reset = ctk.CTkButton(self.btn_frame, text="", command=self.reset_bg, fg_color="#c0392b", hover_color="#e74c3c", width=120); self.btn_reset.pack(side="left", padx=5)
        self.btn_wall = ctk.CTkButton(self.btn_frame, text="", command=self.set_steam_bg_as_wall); self.btn_wall.pack(side="right", padx=5)
        
        self.lbl_history = ctk.CTkLabel(f, text="", font=("Segoe UI", 14, "bold")); self.lbl_history.pack(anchor="w", pady=(10, 5))
        self.hist_list = tk.Listbox(f, height=4, bg="#2b2b2b", fg="white", borderwidth=0)
        self.hist_list.pack(fill="x")
        self.hist_list.bind("<Double-Button-1>", self.apply_history)
        self.refresh_history()

    def build_cleaner_tab(self):
        f = self.tab_cleaner
        self.lbl_clean_title = ctk.CTkLabel(f, text="", font=("Segoe UI", 26, "bold")); self.lbl_clean_title.pack(anchor="w", pady=(0, 15))
        
        self.hide_friends_var = tk.BooleanVar(value=self.cfg.get("hide_friends", False))
        ctk.CTkCheckBox(f, text="Hide Friends List", variable=self.hide_friends_var, command=self.schedule_apply).pack(anchor="w", pady=5)
        
        self.hide_whatsnew_var = tk.BooleanVar(value=self.cfg.get("hide_whatsnew", False))
        ctk.CTkCheckBox(f, text="Hide 'What's New'", variable=self.hide_whatsnew_var, command=self.schedule_apply).pack(anchor="w", pady=5)

        self.lbl_custom_css = ctk.CTkLabel(f, text=""); self.lbl_custom_css.pack(anchor="w", pady=(20, 5))
        self.css_text = ctk.CTkTextbox(f, height=150)
        self.css_text.pack(fill="x")
        self.css_text.insert("1.0", self.cfg.get("custom_css", ""))
        self.bind_paste(self.css_text) # Фикс для CSS
        
        self.btn_apply_css = ctk.CTkButton(f, text="", command=self.apply_now); self.btn_apply_css.pack(anchor="w", pady=10)

    def build_presets_tab(self):
        f = self.tab_presets
        self.lbl_presets_title = ctk.CTkLabel(f, text="", font=("Segoe UI", 26, "bold")); self.lbl_presets_title.pack(anchor="w", pady=(0, 15))
        self.preset_frame = ctk.CTkScrollableFrame(f, height=300); self.preset_frame.pack(fill="both", expand=True, pady=5)
        self.btn_row_presets = ctk.CTkFrame(f, fg_color="transparent"); self.btn_row_presets.pack(fill="x", pady=10)
        self.btn_save_preset = ctk.CTkButton(self.btn_row_presets, text="", command=self.save_preset); self.btn_save_preset.pack(side="left", padx=5)
        self.btn_refresh_presets = ctk.CTkButton(self.btn_row_presets, text="", command=self.refresh_presets, fg_color="gray"); self.btn_refresh_presets.pack(side="left", padx=5)
        self.refresh_presets()

    def build_slideshow_tab(self):
        f = self.tab_slideshow
        self.lbl_slide_title = ctk.CTkLabel(f, text="", font=("Segoe UI", 26, "bold")); self.lbl_slide_title.pack(anchor="w", pady=(0, 15))
        self.btn_pick_folder = ctk.CTkButton(f, text="Select Folder", command=self.pick_slideshow_folder); self.btn_pick_folder.pack(anchor="w", pady=5)
        self.folder_lbl = ctk.CTkLabel(f, text="No folder", text_color="gray"); self.folder_lbl.pack(anchor="w", pady=5)
        self.lbl_interval = ctk.CTkLabel(f, text="Interval (sec):"); self.lbl_interval.pack(anchor="w", pady=(15, 0))
        self.interval_var = tk.IntVar(value=300); ctk.CTkEntry(f, textvariable=self.interval_var, width=100).pack(anchor="w", pady=5)
        self.slideshow_btn = ctk.CTkButton(f, text="", command=self.toggle_slideshow); self.slideshow_btn.pack(anchor="w", pady=20)

    def build_win_tab(self):
        f = self.tab_win
        self.lbl_win_title = ctk.CTkLabel(f, text="", font=("Segoe UI", 26, "bold")); self.lbl_win_title.pack(anchor="w", pady=(0, 15))
        self.btn_win_wall = ctk.CTkButton(f, text="Set Wallpaper", command=self.set_win_wall); self.btn_win_wall.pack(anchor="w", pady=10)
        self.btn_screenshot = ctk.CTkButton(f, text="📸 Screenshot as Wallpaper", command=self.take_screenshot); self.btn_screenshot.pack(anchor="w", pady=10)

    def build_hotkeys_tab(self):
        f = self.tab_hotkeys
        self.lbl_hk_title = ctk.CTkLabel(f, text="", font=("Segoe UI", 26, "bold")); self.lbl_hk_title.pack(anchor="w", pady=(0, 15))
        self.hk_vars = {}
        hk_cfg = self.cfg.get("hotkeys", {})
        def add_hk_row(label, key):
            row = ctk.CTkFrame(f, fg_color="transparent"); row.pack(fill="x", pady=5)
            ctk.CTkLabel(row, text=label, width=200, anchor="w").pack(side="left")
            var = tk.StringVar(value=hk_cfg.get(key, ""))
            ctk.CTkEntry(row, textvariable=var).pack(side="left", fill="x", expand=True)
            self.hk_vars[key] = var
        add_hk_row("Apply:", "apply"); add_hk_row("Reset:", "reset")
        add_hk_row("Next Preset:", "next_preset"); add_hk_row("Slideshow:", "slideshow")
        self.btn_save_hk = ctk.CTkButton(f, text="", command=self.save_hotkeys); self.btn_save_hk.pack(anchor="w", pady=20)

    def build_settings_tab(self):
        f = self.tab_settings
        self.lbl_settings_title = ctk.CTkLabel(f, text="", font=("Segoe UI", 26, "bold")); self.lbl_settings_title.pack(anchor="w", pady=(0, 15))
        self.lang_frame = ctk.CTkFrame(f, fg_color="transparent"); self.lang_frame.pack(fill="x", pady=10)
        self.lbl_lang = ctk.CTkLabel(self.lang_frame, text=""); self.lbl_lang.pack(side="left")
        self.lang_combo = ctk.CTkOptionMenu(self.lang_frame, values=["ru", "en"], command=self.change_lang)
        self.lang_combo.set(self.lang); self.lang_combo.pack(side="left", padx=10)
        self.startup_var = tk.BooleanVar(value=self.check_startup_status())
        self.chk_startup = ctk.CTkCheckBox(f, text="", variable=self.startup_var, command=self.toggle_startup)
        self.chk_startup.pack(anchor="w", pady=10)
        self.btn_open_folder = ctk.CTkButton(f, text="", command=lambda: os.startfile(APP_DATA_DIR)); self.btn_open_folder.pack(anchor="w", pady=20)
        self.btn_reset_all = ctk.CTkButton(f, text="", fg_color="#c0392b", hover_color="#e74c3c", command=self.reset_bg); self.btn_reset_all.pack(anchor="w", pady=10)

    def apply_translations(self):
        L = LANGS[self.lang]
        self.btn_steam.configure(text=L["nav_steam"])
        self.btn_cleaner.configure(text=L["nav_cleaner"])
        self.btn_presets.configure(text=L["nav_presets"])
        self.btn_slideshow.configure(text=L["nav_slideshow"])
        self.btn_win.configure(text=L["nav_win"])
        self.btn_hotkeys.configure(text=L["nav_hotkeys"])
        self.btn_settings.configure(text=L["nav_settings"])
        self.lbl_steam_title.configure(text=L["nav_steam"])
        self.status_lbl.configure(text=L["status_wait"])
        self.drop_label.configure(text=L["drop_zone"])
        self.lbl_url.configure(text=L["lbl_url"])
        self.btn_load.configure(text=L["btn_load"])
        self.lbl_opacity.configure(text=L["lbl_opacity"])
        self.lbl_dim.configure(text=L["lbl_dim"])
        self.lbl_blur.configure(text=L["lbl_blur"])
        self.btn_apply.configure(text=L["btn_apply"])
        self.btn_reset.configure(text=L["btn_reset"])
        self.btn_wall.configure(text=L["btn_wall"])
        self.lbl_history.configure(text=L["lbl_history"])
        self.lbl_clean_title.configure(text=L["nav_cleaner"])
        self.lbl_custom_css.configure(text=L["lbl_custom_css"])
        self.btn_apply_css.configure(text=L["btn_apply_css"])
        self.lbl_presets_title.configure(text=L["nav_presets"])
        self.btn_save_preset.configure(text=L["btn_save_preset"])
        self.btn_refresh_presets.configure(text=L["btn_refresh"])
        self.lbl_slide_title.configure(text=L["nav_slideshow"])
        self.lbl_win_title.configure(text=L["nav_win"])
        self.lbl_hk_title.configure(text=L["nav_hotkeys"])
        self.btn_save_hk.configure(text=L["btn_save_hk"])
        self.lbl_settings_title.configure(text=L["nav_settings"])
        self.lbl_lang.configure(text=L["lbl_lang"])
        self.chk_startup.configure(text=L["lbl_startup"])
        self.btn_open_folder.configure(text=L["lbl_open_folder"])
        self.btn_reset_all.configure(text=L["lbl_reset_all"])

    def change_lang(self, lang):
        self.lang = lang; self.save_cfg(); self.apply_translations()
        self.show_toast(LANGS[lang]["toast_lang"])

    def check_startup_status(self):
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_READ) as k:
                winreg.QueryValueEx(k, "PerfectBackgroundStudio"); return True
        except: return False

    def toggle_startup(self):
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        if self.startup_var.get():
            exe = f'"{sys.executable}" "{os.path.abspath(__file__)}"'
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as k:
                winreg.SetValueEx(k, "PerfectBackgroundStudio", 0, winreg.REG_SZ, exe)
        else:
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as k:
                    winreg.DeleteValue(k, "PerfectBackgroundStudio")
            except: pass
        self.show_toast(self.L["toast_startup"])

    def refresh_presets(self):
        for widget in self.preset_frame.winfo_children(): widget.destroy()
        for p in self.presets.list():
            row = ctk.CTkFrame(self.preset_frame); row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=p.get("name", "?")).pack(side="left", padx=10)
            ctk.CTkButton(row, text="X", width=40, fg_color="#c0392b", command=lambda pr=p: self.delete_preset(pr)).pack(side="right", padx=5)
            ctk.CTkButton(row, text=">", width=40, command=lambda pr=p: self.apply_preset(pr)).pack(side="right", padx=5)

    def save_preset(self):
        if not self.image_path: return
        name = simpledialog.askstring(APP_NAME, LANGS[self.lang]["preset_name"], parent=self)
        if name:
            settings = {"dim": self.slider_dim.get(), "blur": self.slider_blur.get(), "ui_opacity": self.slider_opacity.get()}
            self.presets.save(name, self.image_path, settings)
            self.refresh_presets()
            self.show_toast(self.L["toast_saved"])

    def apply_preset(self, p):
        path = self.presets.image_path(p)
        if path:
            self.image_path = path
            s = p.get("settings", {})
            if "dim" in s: self.slider_dim.set(s["dim"])
            if "blur" in s: self.slider_blur.set(s["blur"])
            if "ui_opacity" in s: self.slider_opacity.set(s["ui_opacity"])
            self.update_preview()
            self.apply_now()

    def delete_preset(self, p):
        self.presets.delete(p); self.refresh_presets()

    def pick_slideshow_folder(self):
        d = filedialog.askdirectory()
        if d: self.slideshow_folder = d; self.folder_lbl.configure(text=d, text_color="white")

    def toggle_slideshow(self):
        if self.slideshow_active:
            self.slideshow_active = False
            self.slideshow_btn.configure(text=LANGS[self.lang]["btn_start_slideshow"], fg_color=("#3a7ebf", "#1f538d"))
        else:
            if not hasattr(self, 'slideshow_folder'): return
            self.slideshow_active = True
            self.slideshow_btn.configure(text=LANGS[self.lang]["btn_stop_slideshow"], fg_color="#c0392b")
            threading.Thread(target=self.slideshow_worker, daemon=True).start()

    def slideshow_worker(self):
        while self.slideshow_active and not self.stop_event.is_set():
            try:
                images = [os.path.join(self.slideshow_folder, f) for f in os.listdir(self.slideshow_folder) if f.lower().endswith(IMG_EXT)]
                if images: self.after(0, lambda p=random.choice(images): self.set_image(p))
            except: pass
            for _ in range(self.interval_var.get()):
                if not self.slideshow_active: break
                time.sleep(1)

    def pick_image(self):
        p = filedialog.askopenfilename(filetypes=IMG_TYPES)
        if p: self.set_image(p)

    def set_image(self, path):
        self.image_path = path; self.update_preview(); self.apply_now()

    def load_from_url(self):
        url = self.url_var.get()
        if not url.startswith("http"): return
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response: data = response.read()
            path = os.path.join(APP_DATA_DIR, "downloaded.jpg")
            with open(path, "wb") as f: f.write(data)
            self.set_image(path)
        except: pass

    def set_steam_bg_as_wall(self):
        if self.image_path: set_wallpaper(self.image_path)

    def update_preview(self):
        if self.image_path and os.path.exists(self.image_path):
            img = Image.open(self.image_path); img.thumbnail((400, 180))
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            self.drop_label.configure(image=ctk_img, text="")

    def schedule_apply(self, _=None):
        if self._pending: self.after_cancel(self._pending)
        self._pending = self.after(500, self.apply_now)

    def apply_now(self):
        if not self.image_path or not os.path.exists(self.image_path): return
        self.save_cfg()
        self.update_status(LANGS[self.lang]["status_apply"], "#f1c40f")
        
        def work():
            targets = get_targets(8080)
            if not targets:
                self.after(0, lambda: self.update_status(LANGS[self.lang]["status_disconn"], "#e74c3c"))
                return
            
            cleaner_css = ""
            if self.hide_friends_var.get(): cleaner_css += ".friendslist { display: none !important; }"
            if self.hide_whatsnew_var.get(): cleaner_css += ".whatsnew { display: none !important; }"
            
            cfg = {"url": image_to_data_url(self.image_path), "dim": self.slider_dim.get() / 100, "blur": self.slider_blur.get(), "ui_opacity": self.slider_opacity.get() / 100, "cleaner_css": cleaner_css, "custom_css": self.css_text.get("1.0", "end-1c")}
            js = INJECT_JS.replace("CFG_PLACEHOLDER", json.dumps(cfg))
            self.js = js
            
            for t in targets:
                if t.get("title") in TARGET_TITLES: cdp_eval(t["webSocketDebuggerUrl"], js)
            
            self.add_history(self.image_path)
            self.after(0, lambda: self.update_status(LANGS[self.lang]["status_applied"], "#2ecc71"))
        threading.Thread(target=work, daemon=True).start()

    def reset_bg(self):
        self.js = None
        targets = get_targets(8080) or []
        for t in targets:
            if t.get("title") in TARGET_TITLES: cdp_eval(t["webSocketDebuggerUrl"], REMOVE_JS)
        self.update_status(LANGS[self.lang]["status_disconn"], "gray")

    def add_history(self, path):
        hist = []
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r") as f: hist = json.load(f)
            except: pass
        if path in hist: hist.remove(path)
        hist.insert(0, path)
        with open(HISTORY_FILE, "w") as f: json.dump(hist[:10], f)
        self.after(0, self.refresh_history)

    def refresh_history(self):
        self.hist_list.delete(0, "end")
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r") as f:
                    for h in json.load(f): self.hist_list.insert("end", os.path.basename(h))
            except: pass

    def apply_history(self, event):
        idx = self.hist_list.curselection()
        if idx:
            try:
                with open(HISTORY_FILE, "r") as f: self.set_image(json.load(f)[idx[0]])
            except: pass

    def watch_steam(self):
        while not self.stop_event.is_set():
            time.sleep(3)
            targets = get_targets(8080)
            if targets:
                if "подключён" not in self.status_lbl.cget("text") and "connected" not in self.status_lbl.cget("text"):
                    self.after(0, lambda: self.update_status(LANGS[self.lang]["status_conn"], "#2ecc71"))
                if self.js:
                    for t in targets:
                        if t.get("title") in TARGET_TITLES: cdp_eval(t["webSocketDebuggerUrl"], self.js)
            else:
                if "не подключён" not in self.status_lbl.cget("text") and "disconnected" not in self.status_lbl.cget("text"):
                    self.after(0, lambda: self.update_status(LANGS[self.lang]["status_disconn"], "#e74c3c"))

    def update_status(self, text, color): self.status_lbl.configure(text=text, text_color=color)
    def set_win_wall(self):
        p = filedialog.askopenfilename(filetypes=IMG_TYPES)
        if p: set_wallpaper(p); messagebox.showinfo("Success", "Wallpaper set!")
    def take_screenshot(self):
        img = ImageGrab.grab(); path = os.path.join(APP_DATA_DIR, "screen.png"); img.save(path)
        set_wallpaper(path); messagebox.showinfo("Success", "Screenshot set!")
    def save_hotkeys(self):
        self.cfg["hotkeys"] = {k: v.get().strip() for k, v in self.hk_vars.items() if v.get().strip()}
        self.save_cfg(); self.register_hotkeys()

    def register_hotkeys(self):
        try: keyboard.remove_all_hotkeys()
        except: pass
        mapping = {"apply": self.apply_now, "reset": self.reset_bg, "next_preset": self.next_preset, "slideshow": self.toggle_slideshow}
        for key, func in mapping.items():
            combo = self.cfg.get("hotkeys", {}).get(key)
            if combo:
                try: keyboard.add_hotkey(combo, lambda f=func: self.after(0, f))
                except: pass

    def next_preset(self):
        items = self.presets.list()
        if not items: return
        if not hasattr(self, '_preset_idx'): self._preset_idx = -1
        self._preset_idx = (self._preset_idx + 1) % len(items)
        self.apply_preset(items[self._preset_idx])

    def on_close(self):
        self.stop_event.set()
        self.attributes("-alpha", 0.0)
        self.destroy()

if __name__ == "__main__":
    try:
        bootloader()
        app = UltimateStudio()
        app.mainloop()
    except Exception as e:
        import traceback
        print("\n[CRITICAL ERROR]")
        traceback.print_exc()
        input("\nPress Enter to close console...")