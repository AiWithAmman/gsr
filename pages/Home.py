import platform
import tkinter as tk

from Components import Theme as T
from Components.Cards import SettingRow, on_off, section_header, stack


def windows_name():
    if platform.system() != "Windows":
        return platform.system()+" "+platform.release()
    parts= platform.version().split(".")
    if len(parts) >= 3 and parts[2].isdigit() and int(parts[2]) >= 22000:
        return "Windows 11"
    return "Windows "+platform.release()


def build(parent, app):
    store= app.store

    pc_card= tk.Frame(parent, bg=T.CARD, highlightthickness=1, highlightbackground=T.CARD_BORDER,
                      highlightcolor=T.CARD_BORDER)
    stack(pc_card)
    inner= tk.Frame(pc_card, bg=T.CARD)
    inner.pack(fill="x", padx=T.px(20), pady=T.px(20))

    screen= tk.Canvas(inner, width=T.px(160), height=T.px(100), bg=T.CARD, highlightthickness=0)
    screen.create_rectangle(4, 4, T.px(156), T.px(90), fill="#2b6cb0", outline="#1b1b1b", width=3)
    screen.create_line(T.px(60), T.px(96), T.px(100), T.px(96), width=3, fill="#1b1b1b")
    screen.pack(side="left")

    pc_name= platform.node()
    if pc_name == "":
        pc_name="DESKTOP-PC"
    info= tk.Frame(inner, bg=T.CARD)
    info.pack(side="left", padx=T.px(20), fill="x", expand=True)
    tk.Label(info, text=pc_name, font=T.font(14, "semibold"), bg=T.CARD, fg=T.TEXT,
             anchor="w").pack(fill="x")
    tk.Label(info, text=windows_name(), font=T.font(10), bg=T.CARD,
             fg=T.SUBTEXT, anchor="w").pack(fill="x")

    section_header(parent, "Your privacy")

    def go_privacy():
        app.open("privacy")

    def go_camera():
        app.open("privacy/camera")

    def go_microphone():
        app.open("privacy/microphone")

    def go_location():
        app.open("privacy/location")

    def go_history():
        app.open("privacy/history")

    stack(SettingRow(parent, "Privacy & security", "See and change what Windows and apps can access",
                     "privacy", on_click=go_privacy))
    stack(SettingRow(parent, "Camera", "Camera access: "+on_off(store.get("perm.camera.access", True)),
                     "camera", on_click=go_camera))
    stack(SettingRow(parent, "Microphone",
                     "Microphone access: "+on_off(store.get("perm.microphone.access", True)),
                     "microphone", on_click=go_microphone))
    stack(SettingRow(parent, "Location", "Location access: "+on_off(store.get("perm.location.access", True)),
                     "location", on_click=go_location))
    stack(SettingRow(parent, "Recent privacy changes", "Review and restore settings you changed",
                     "history", on_click=go_history))


def routes():
    return {"home": ("Home", build)}
