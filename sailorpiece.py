import pyautogui
import pydirectinput
import threading
import time
import customtkinter as ctk
import keyboard
import base64
import io
from PIL import Image
import pygetwindow as gw
import sys
import os

# ----------------------------
# CONFIG
# ----------------------------
# Image Haki en base64 (image.png encodé)
image_base64 = """
"""
interval = 10
running = False
shortcut_key = "F6"
drag_start_x = 0
drag_start_y = 0
waiting_for_key = False

# Charger l'image depuis le fichier au démarrage
haki_image = None
def get_image_path():
    """Récupère le chemin de l'image (dev ou exe)"""
    if getattr(sys, 'frozen', False):
        # Exécution en tant qu'exe PyInstaller
        base_path = sys._MEIPASS
    else:
        # Exécution en tant que script Python
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, "image.png")

try:
    haki_image = Image.open(get_image_path())
except:
    pass

# ----------------------------
# VERIF FENETRE ROBOX
# ----------------------------
def is_roblox_active():
    try:
        active_window = gw.getActiveWindow()
        if active_window:
            title = active_window.title
            # Vérifier si c'est Roblox (le titre contient généralement "Roblox" ou est vide/quatre chiffres)
            return "Roblox" in title or (title.isdigit() and len(title) == 4) or title == "ROBLOX"
        return False
    except:
        return True  # En cas d'erreur, on autorise quand même

# ----------------------------
# BOT LOOP
# ----------------------------
def bot_loop():
    global running
    while running:
        try:
            # Vérifier si Roblox est la fenêtre active
            if not is_roblox_active():
                status_label.configure(text="⏳ En attente de Roblox...")
                time.sleep(interval)
                continue
                
            if haki_image:
                result = pyautogui.locateOnScreen(haki_image, confidence=0.6)
                if result:
                    status_label.configure(text="✅ Image détectée")
                else:
                    status_label.configure(text="❌ Pas d'image → H")
                    pydirectinput.press('h')
            else:
                status_label.configure(text="⚠️ Image non chargée")
        except Exception as e:
            status_label.configure(text="❌ Pas d'image → H")
            pydirectinput.press('h')
        time.sleep(interval)

# ----------------------------
# TOGGLE BOT
# ----------------------------
def toggle_bot():
    global running
    if running:
        running = False
        status_label.configure(text="⛔ Bot arrêté")
        toggle_button.configure(text="▶ Démarrer")
    else:
        running = True
        status_label.configure(text="🚀 Bot lancé")
        toggle_button.configure(text="⏸ Stop")
        threading.Thread(target=bot_loop, daemon=True).start()

# ----------------------------
# DRAG WINDOW
# ----------------------------
def start_drag(event):
    global drag_start_x, drag_start_y
    drag_start_x = event.x
    drag_start_y = event.y

def do_drag(event):
    x = app.winfo_x() + event.x - drag_start_x
    y = app.winfo_y() + event.y - drag_start_y
    app.geometry(f"+{x}+{y}")

# ----------------------------
# SET HOTKEY BY CLICK
# ----------------------------
def wait_for_key(event):
    global waiting_for_key
    waiting_for_key = True
    status_label.configure(text="⏳ Appuie sur une touche...")

def key_pressed(event):
    global shortcut_key, waiting_for_key
    if waiting_for_key:
        key = event.name.upper()
        shortcut_key = key
        shortcut_label.configure(text=f"Raccourci actuel: {shortcut_key}")
        status_label.configure(text=f"✅ Raccourci changé: {shortcut_key}")
        waiting_for_key = False

# ----------------------------
# INTERFACE
# ----------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Auto Haki Observation")
app.geometry("300x200")
app.attributes("-alpha", 0.85)
app.attributes("-topmost", True)
app.overrideredirect(True)

frame = ctk.CTkFrame(app, corner_radius=15)
frame.pack(fill="both", expand=True, padx=10, pady=10)

# TITRE (drag)
title = ctk.CTkLabel(frame, text="Auto Haki Observation", font=("Arial", 14, "bold"))
title.pack(pady=5)
title.bind("<Button-1>", start_drag)
title.bind("<B1-Motion>", do_drag)

# STATUS
status_label = ctk.CTkLabel(frame, text="⛔ Bot arrêté", font=("Arial", 12))
status_label.pack(pady=5)

# TOGGLE BUTTON
toggle_button = ctk.CTkButton(frame, text="▶ Démarrer", command=toggle_bot)
toggle_button.pack(pady=5)

# HOTKEY LABEL (click to set)
shortcut_label = ctk.CTkLabel(frame, text=f"Raccourci actuel: {shortcut_key}", font=("Arial", 12))
shortcut_label.pack(pady=5)
shortcut_label.bind("<Button-1>", wait_for_key)

# ----------------------------
# GLOBAL HOTKEY LISTENER (non bloquant)
# ----------------------------
def global_listener():
    while True:
        if keyboard.is_pressed(shortcut_key):
            toggle_bot()
            time.sleep(0.3)
        time.sleep(0.05)

threading.Thread(target=global_listener, daemon=True).start()

# ----------------------------
# KEYBIND DETECTION
# ----------------------------
keyboard.on_press(key_pressed)

# ----------------------------
# START
# ----------------------------
app.mainloop()
