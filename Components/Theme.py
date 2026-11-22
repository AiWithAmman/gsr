import tkinter.font as tkfont

BG="#f3f3f3"
CARD="#fbfbfb"
CARD_HOVER="#f6f6f6"
CARD_BORDER="#e5e5e5"
DIVIDER="#ebebeb"
NAV_HOVER="#eaeaea"
NAV_SELECTED="#e6e6e6"
TEXT="#1b1b1b"
SUBTEXT="#5d5d5d"
DISABLED="#a3a3a3"
ACCENT="#005fb8"
ACCENT_HOVER="#1a6fc0"
WHITE="#ffffff"
SUCCESS="#0f7b0f"

SCALE=1.0
_icon_family=""
_text_family="Segoe UI"

ICONS= {
    "home": "", "system": "", "bluetooth": "", "network": "",
    "personalization": "", "apps": "", "accounts": "", "time": "",
    "gaming": "", "accessibility": "", "privacy": "", "update": "",
    "back": "", "search": "", "chevron_right": "", "chevron_down": "",
    "chevron_up": "", "open": "", "person": "", "info": "",
    "settings": "",
    "shield": "", "find_device": "", "encryption": "", "developer": "",
    "lock": "", "speech": "", "keyboard": "", "diagnostic": "",
    "history": "", "searching": "", "feedback": "", "delete": "",
    "view": "", "health": "", "firewall": "", "app_window": "",
    "family": "", "check": "",
    "location": "", "camera": "", "microphone": "", "voice": "",
    "notifications": "", "account_info": "", "contacts": "",
    "calendar": "", "phone": "", "email": "", "tasks": "",
    "messaging": "", "radios": "", "devices": "", "download": "",
    "document": "", "folder": "", "music": "", "pictures": "",
    "videos": "", "file_system": "", "screenshot": "",
}

FALLBACK= {
    "back": "←", "chevron_right": "›", "chevron_down": "⌄",
    "chevron_up": "⌃", "open": "↗", "search": "⌕", "check": "✓",
}


def init(root):
    global SCALE, _icon_family, _text_family
    try:
        SCALE= max(1.0, root.winfo_fpixels("1i")/96.0)
    except Exception:
        SCALE=1.0
    families= set(tkfont.families(root))
    for name in ("Segoe Fluent Icons", "Segoe MDL2 Assets"):
        if name in families:
            _icon_family= name
            break
    for name in ("Segoe UI Variable Text", "Segoe UI"):
        if name in families:
            _text_family= name
            break


def px(value):
    return int(round(value*SCALE))


def font(size=10, weight="normal"):
    if weight == "semibold" or weight == "bold":
        if _text_family.startswith("Segoe"):
            return ("Segoe UI Semibold", size)
        return (_text_family, size, "bold")
    return (_text_family, size)


def icon_font(size=12):
    return (_icon_family or _text_family, size)


def glyph(name):
    if _icon_family:
        return ICONS.get(name, "")
    return FALLBACK.get(name, "")
