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

        self.routes= {}
        self.routes.update(Home.routes())
        self.routes.update(Privacy_security.routes())
        self.routes.update(Diagnostic.routes())

        self._build_layout()
        root.bind("<Alt-Left>", self.back_key)
        root.bind("<BackSpace>", self.backspace_key)
        self.open("home")

    def back_key(self, event):
        self.back()

    def backspace_key(self, event):
        if not isinstance(self.root.focus_get(), tk.Entry):
            self.back()

    def _build_layout(self):
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(1, weight=1)

        top= tk.Frame(self.root, bg=T.BG)
        top.grid(row=0, column=0, columnspan=2, sticky="ew", padx=T.px(8), pady=(T.px(6), T.px(4)))
        self.back_btn= tk.Label(top, text=T.glyph("back"), font=T.icon_font(10), bg=T.BG,
                                 fg=T.TEXT, width=4, pady=T.px(4))
        self.back_btn.pack(side="left")
        self.back_btn.bind("<Button-1>", self.back_key)
        self.back_btn.bind("<Enter>", self.back_hover)
        self.back_btn.bind("<Leave>", self.back_unhover)
        tk.Label(top, text="Settings", font=T.font(9), bg=T.BG, fg=T.TEXT).pack(side="left",
                                                                               padx=(T.px(4), 0))

        self.sidebar= Sidebar(self.root, NAV_ITEMS, on_select=self.nav_clicked, on_search=self.search)
        self.sidebar.grid(row=1, column=0, sticky="ns")

        content= tk.Frame(self.root, bg=T.BG)
        content.grid(row=1, column=1, sticky="nsew")
        self.header= tk.Frame(content, bg=T.BG)
        self.header.pack(fill="x", padx=(T.px(40), T.px(40)), pady=(T.px(10), T.px(14)))
        self.page_host= tk.Frame(content, bg=T.BG)
        self.page_host.pack(fill="both", expand=True)

    def nav_clicked(self, key):
        if key == "home" or key == "privacy":
            self.open(key)
            return
        for item_key, title, icon in NAV_ITEMS:
            if item_key == key:
                messagebox.showinfo(title, title+" is a placeholder.\n\n"
                                    "This project only focuses on Privacy & security.")

    def back_hover(self, event):
        if self.history:
            self.back_btn.configure(bg=T.NAV_HOVER)

    def back_unhover(self, event):
        self.back_btn.configure(bg=T.BG)

    def _render_header(self, page_id):
        for w in self.header.winfo_children():
            w.destroy()

        if "/" in page_id:
            parent_id= page_id.split("/")[0]
            parent_title= self.routes[parent_id][0]
            parent_label= tk.Label(self.header, text=parent_title, font=T.font(20, "semibold"),
                                   bg=T.BG, fg=T.SUBTEXT, cursor="hand2")
            parent_label.pack(side="left")
            parent_label.bind("<Button-1>", lambda e: self.open(parent_id))
            tk.Label(self.header, text=T.glyph("chevron_right"), font=T.icon_font(12), bg=T.BG,
                     fg=T.SUBTEXT).pack(side="left", padx=T.px(12))

        title= self.routes[page_id][0]
        tk.Label(self.header, text=title, font=T.font(20, "semibold"), bg=T.BG,
                 fg=T.TEXT).pack(side="left")

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
        title, build= self.routes[page_id]
        build(body, self)

        if self.history:
            self.back_btn.configure(fg=T.TEXT, cursor="hand2")
        else:
            self.back_btn.configure(fg=T.DISABLED, cursor="arrow")

    def back(self):
        if self.history:
            last_page= self.history.pop()
            self.open(last_page, push=False)

    def search(self, text):
        query= text.lower()
        found=None
        for page_id in self.routes:
            title= self.routes[page_id][0].lower()
            if title.startswith(query):
                found= page_id
                break
            if query in title and found is None:
                found= page_id

        if found is None:
            messagebox.showinfo("Settings", "No results for "+text)
        else:
            self.open(found)

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
