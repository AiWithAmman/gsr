import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk

from Components import Theme as T
from Components.Cards import ScrollFrame
from Components.Sidebar import Sidebar
from Components.State import SettingsStore
from pages import Diagnostic, Home, Privacy_security

BASE_DIR= os.path.dirname(os.path.abspath(__file__))
STATE_FILE= os.path.join(BASE_DIR, "settings_state.json")

NAV_ITEMS= [
    ("home", "Home", "home"),
    ("system", "System", "system"),
    ("bluetooth", "Bluetooth & devices", "bluetooth"),
    ("network", "Network & internet", "network"),
    ("personalization", "Personalization", "personalization"),
    ("apps", "Apps", "apps"),
    ("accounts", "Accounts", "accounts"),
    ("time", "Time & language", "time"),
    ("gaming", "Gaming", "gaming"),
    ("accessibility", "Accessibility", "accessibility"),
    ("privacy", "Privacy & security", "privacy"),
    ("update", "Windows Update", "update"),
]


class WindowsSettings:
    def __init__(self, root):
        self.root= root
        T.init(root)
        root.title("Settings")
        root.geometry(f"{T.px(1120)}x{T.px(760)}")
        root.minsize(T.px(820), T.px(540))
        root.configure(bg=T.BG)
        ttk.Style(root).configure("TCombobox", padding=T.px(4))

        self.store= SettingsStore(STATE_FILE)
        self.history=[]
        self.current=None
        self.notification_frame = None
        self.notification_timer = None
        self.store.add_listener(self._on_privacy_setting_changed)

        self.routes= {"home": ("Home", Home.build)}
        for key, title, _icon in NAV_ITEMS:
            self.routes.setdefault(key, (title, Home.make_placeholder(title)))
        self.routes.update(Privacy_security.routes())
        self.routes.update(Diagnostic.routes())

        self._build_layout()
        root.bind("<Alt-Left>", lambda e: self.back())
        root.bind("<BackSpace>", lambda e: self.back() if not isinstance(root.focus_get(), tk.Entry) else None)
        self.open("privacy")

    def _build_layout(self):
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(1, weight=1)

        top= tk.Frame(self.root, bg=T.BG)
        top.grid(row=0, column=0, columnspan=2, sticky="ew", padx=T.px(8), pady=(T.px(6), T.px(4)))
        self.back_btn= tk.Label(top, text=T.glyph("back"), font=T.icon_font(10), bg=T.BG,
                                 fg=T.TEXT, width=4, pady=T.px(4))
        self.back_btn.pack(side="left")
        self.back_btn.bind("<Button-1>", lambda e: self.back())
        self.back_btn.bind("<Enter>", lambda e: self.history and self.back_btn.configure(bg=T.NAV_HOVER))
        self.back_btn.bind("<Leave>", lambda e: self.back_btn.configure(bg=T.BG))
        tk.Label(top, text="Settings", font=T.font(9), bg=T.BG, fg=T.TEXT).pack(side="left",
                                                                               padx=(T.px(4), 0))

        self.sidebar= Sidebar(self.root, NAV_ITEMS, on_select=self.open, on_search=self.search)
        self.sidebar.grid(row=1, column=0, sticky="ns")

        content= tk.Frame(self.root, bg=T.BG)
        content.grid(row=1, column=1, sticky="nsew")
        self.header= tk.Frame(content, bg=T.BG)
        self.header.pack(fill="x", padx=(T.px(40), T.px(40)), pady=(T.px(10), T.px(14)))
        self.page_host= tk.Frame(content, bg=T.BG)
        self.page_host.pack(fill="both", expand=True)

    def _render_header(self, page_id):
        for w in self.header.winfo_children():
            w.destroy()
        parts= page_id.split("/")
        crumbs= ["/".join(parts[:i+1]) for i in range(len(parts))]
        for i, crumb in enumerate(crumbs):
            title= self.routes[crumb][0]
            last= i == len(crumbs)-1
            lbl= tk.Label(self.header, text=title, font=T.font(20, "semibold"), bg=T.BG,
                           fg=T.TEXT if last else T.SUBTEXT, cursor="arrow" if last else "hand2")
            lbl.pack(side="left")
            if not last:
                lbl.bind("<Button-1>", lambda e, c=crumb: self.open(c))
                lbl.bind("<Enter>", lambda e, l=lbl: l.configure(fg=T.TEXT))
                lbl.bind("<Leave>", lambda e, l=lbl: l.configure(fg=T.SUBTEXT))
                tk.Label(self.header, text=T.glyph("chevron_right"), font=T.icon_font(12), bg=T.BG,
                         fg=T.SUBTEXT).pack(side="left", padx=T.px(12))

    def open(self, page_id, push=True):
        if page_id not in self.routes:
            return
        if push and self.current and self.current != page_id:
            self.history.append(self.current)
        self.current= page_id
        self.sidebar.select(page_id.split("/")[0])
        self._render_header(page_id)

        for w in self.page_host.winfo_children():
            w.destroy()
        scroller= ScrollFrame(self.page_host)
        scroller.pack(fill="both", expand=True)
        body= tk.Frame(scroller.inner, bg=T.BG)
        body.pack(fill="x", padx=(T.px(40), T.px(28)), pady=(0, T.px(36)))
        self.routes[page_id][1](body, self)

        self.back_btn.configure(fg=T.TEXT if self.history else T.DISABLED,
                                cursor="hand2" if self.history else "arrow")

    def back(self):
        if self.history:
            self.open(self.history.pop(), push=False)

    def search(self, text):
        query= text.lower()
        matches= [rid for rid, (title, _b) in self.routes.items() if query in title.lower()]
        if not matches:
            messagebox.showinfo("Settings", f"No results for “{text}”.")
            return
        matches.sort(key=lambda rid: (not self.routes[rid][0].lower().startswith(query), len(rid)))
        self.open(matches[0])

    def _on_privacy_setting_changed(self, event):
        key = event["key"]
        old_value = event["old_value"]
        new_value = event["new_value"]

        setting_name = key.replace(".", " ").replace("_", " ").title()

        if(isinstance(old_value, bool)):
            old_value = "On" if old_value else "Off"

        if(isinstance(new_value, bool)):
            new_value = "On" if new_value else "Off"
        
        if self.notification_timer is not None:
            self.root.after_cancel(self.notification_timer)
            self.notification_timer = None

        if self.notification_frame is not None:
            if self.notification_frame.winfo_exists():
                self.notification_frame.destroy()
            self.notification_frame = None

        self.notification_frame = tk.Frame(self.root, bg = T.CARD, highlightbackground = T.SUBTEXT, highlightthickness = 1)

        self.notification_frame.place(relx = 1.0, rely = 1.0, anchor = "se", x =- T.px(20), y =- T.px(20), width = T.px(320), height = T.px(85))

        tk.Label(self.notification_frame, text = "Privacy setting changed", font = T.font(10, "semibold"), bg = T.CARD,
            fg = T.TEXT).pack(anchor = "w", padx = T.px(12), pady = (T.px(8), 0))

        tk.Label(self.notification_frame, text = f"{setting_name}: {old_value} -> {new_value}", 
            font = T.font(9), bg = T.CARD, fg = T.SUBTEXT, wraplength = T.px(290)).pack(anchor = "w", padx = T.px(12), pady = T.px(5))

        self.notification_timer = self.root.after(4000, self._remove_notification)


    def _remove_notification(self):
        if self.notification_frame is not None:
            if self.notification_frame.winfo_exists():
                self.notification_frame.destroy()
        self.notification_frame = None
        self.notification_timer = None


def _enable_dpi_awareness():
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass


if __name__ == "__main__":
    _enable_dpi_awareness()
    root= tk.Tk()
    WindowsSettings(root)
    root.mainloop()
