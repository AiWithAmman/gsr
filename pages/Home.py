import platform
import tkinter as tk

from Components import Theme as T
from Components.Buttons import Button
from Components.Cards import SettingRow, paragraph, section_header, stack


def build(parent, app):
    hero= tk.Frame(parent, bg=T.CARD, highlightthickness=1, highlightbackground=T.CARD_BORDER,
                    highlightcolor=T.CARD_BORDER)
    stack(hero)
    inner= tk.Frame(hero, bg=T.CARD)
    inner.pack(fill="x", padx=T.px(20), pady=T.px(20))
    screen= tk.Canvas(inner, width=T.px(160), height=T.px(100), bg=T.CARD, highlightthickness=0)
    screen.create_rectangle(4, 4, T.px(156), T.px(90), fill="#2b6cb0", outline="#1b1b1b", width=3)
    screen.create_line(T.px(60), T.px(96), T.px(100), T.px(96), width=3, fill="#1b1b1b")
    screen.pack(side="left")
    info= tk.Frame(inner, bg=T.CARD)
    info.pack(side="left", padx=T.px(20), fill="x", expand=True)
    tk.Label(info, text=platform.node() or "DESKTOP-PC", font=T.font(14, "semibold"), bg=T.CARD,
             fg=T.TEXT, anchor="w").pack(fill="x")
    tk.Label(info, text=f"{platform.system()} {platform.release()}", font=T.font(10), bg=T.CARD,
             fg=T.SUBTEXT, anchor="w").pack(fill="x")

    section_header(parent, "Recommended settings")
    store= app.store
    links= [
        ("privacy", "Privacy & security", "Review security and the permissions apps have", "privacy"),
        ("privacy/diagnostics", "Diagnostics & feedback", "Choose what diagnostic data is sent", "diagnostic"),
        ("privacy/location", "Location",
         "On" if store.get("perm.location.access", True) else "Off", "location"),
        ("privacy/camera", "Camera", "On" if store.get("perm.camera.access", True) else "Off", "camera"),
        ("privacy/microphone", "Microphone",
         "On" if store.get("perm.microphone.access", True) else "Off", "microphone"),
        ("privacy/windows-security", "Windows Security", "No actions needed.", "shield"),
    ]
    for route, title, desc, icon in links:
        stack(SettingRow(parent, title, desc, icon, on_click=lambda r=route: app.open(r)))


def make_placeholder(title):
    def build_placeholder(parent, app):
        card= tk.Frame(parent, bg=T.CARD, highlightthickness=1, highlightbackground=T.CARD_BORDER,
                        highlightcolor=T.CARD_BORDER)
        stack(card)
        inner= tk.Frame(card, bg=T.CARD)
        inner.pack(fill="x", padx=T.px(20), pady=T.px(20))
        paragraph(inner, f"{title} hasn't been built in this clone yet.", bg=T.CARD, fg=T.TEXT)
        paragraph(inner, "Privacy & security is fully implemented — head there to try it out.",
                  bg=T.CARD)
        Button(inner, "Go to Privacy & security", accent=True,
               command=lambda: app.open("privacy")).pack(anchor="w", pady=(T.px(6), 0))
    return build_placeholder
