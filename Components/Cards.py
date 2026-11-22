import tkinter as tk
from tkinter import ttk

from Components import Theme as T
from Components.Buttons import Button, Link, ToggleSwitch, mouse_is_over


def get_all_widgets(widget):
    widgets= [widget]
    for child in widget.winfo_children():
        widgets= widgets+get_all_widgets(child)
    return widgets


class ScrollFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=T.BG)
        self.canvas= tk.Canvas(self, bg=T.BG, highlightthickness=0, bd=0, yscrollincrement=T.px(20))
        self.scrollbar= ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner= tk.Frame(self.canvas, bg=T.BG)
        self.window= self.canvas.create_window(0, 0, window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.inner.bind("<Configure>", self.update_scroll_area)
        self.canvas.bind("<Configure>", self.canvas_resized)
        self.canvas.bind_all("<MouseWheel>", self.mouse_wheel)

    def update_scroll_area(self, event=None):
        height= self.inner.winfo_reqheight()
        if height < self.canvas.winfo_height():
            height= self.canvas.winfo_height()
        self.canvas.configure(scrollregion=(0, 0, self.inner.winfo_reqwidth(), height))

    def canvas_resized(self, event):
        self.canvas.itemconfigure(self.window, width=event.width)
        self.update_scroll_area()

    def mouse_wheel(self, event):
        if not self.canvas.winfo_exists():
            return
        if self.inner.winfo_reqheight() <= self.canvas.winfo_height():
            return
        if event.delta > 0:
            self.canvas.yview_scroll(-2, "units")
        else:
            self.canvas.yview_scroll(2, "units")


class SettingRow(tk.Frame):
    def __init__(self, parent, title, description=None, icon=None, on_click=None,
                 toggle=None, on_toggle=None, chevron=None, nested=False):
        if nested:
            border=0
        else:
            border=1
        super().__init__(parent, bg=T.CARD, highlightthickness=border,
                         highlightbackground=T.CARD_BORDER, highlightcolor=T.CARD_BORDER)
        self.on_click= on_click
        self.on_toggle= on_toggle
        self.enabled=True
        self.toggle=None
        self.state_label=None
        self.chevron_label=None
        self.desc_label=None

        if nested:
            left_space= T.px(56)
        else:
            left_space= T.px(16)
        if description:
            top_space= T.px(13)
        else:
            top_space= T.px(15)
        body= tk.Frame(self, bg=T.CARD)
        body.pack(fill="x", padx=(left_space, T.px(16)), pady=top_space)

        if icon and not nested:
            icon_box= tk.Frame(body, bg=T.CARD, width=T.px(24), height=T.px(24))
            icon_box.pack_propagate(False)
            icon_box.pack(side="left", padx=(0, T.px(16)))
            tk.Label(icon_box, text=T.glyph(icon), font=T.icon_font(14), bg=T.CARD, fg=T.TEXT).pack(expand=True)

        self.right_frame= tk.Frame(body, bg=T.CARD)
        self.right_frame.pack(side="right")

        if chevron is None and on_click is not None:
            chevron="chevron_right"
        if chevron:
            self.chevron_label= tk.Label(self.right_frame, text=T.glyph(chevron), font=T.icon_font(10),
                                         bg=T.CARD, fg=T.TEXT)
            self.chevron_label.pack(side="right", padx=(T.px(12), 0))

        if toggle is not None:
            self.toggle= ToggleSwitch(self.right_frame, value=toggle, command=self.toggle_changed)
            self.toggle.pack(side="right")
            self.state_label= tk.Label(self.right_frame, text=on_off(toggle), font=T.font(10),
                                       bg=T.CARD, fg=T.TEXT)
            self.state_label.pack(side="right", padx=(0, T.px(10)))

        text_area= tk.Frame(body, bg=T.CARD)
        text_area.pack(side="left", fill="x", expand=True)
        self.title_label= tk.Label(text_area, text=title, font=T.font(10), bg=T.CARD, fg=T.TEXT,
                                   anchor="w", justify="left")
        self.title_label.pack(fill="x")
        if description:
            self.desc_label= tk.Label(text_area, text=description, font=T.font(9), bg=T.CARD,
                                      fg=T.SUBTEXT, anchor="w", justify="left")
            self.desc_label.pack(fill="x")
            self.bind("<Configure>", self.wrap_text)

        if on_click is not None:
            self.bind("<Enter>", self.mouse_enter)
            self.bind("<Leave>", self.mouse_leave)
            for w in get_all_widgets(self):
                if isinstance(w, ToggleSwitch) or isinstance(w, Button) or isinstance(w, ttk.Widget):
                    continue
                w.bind("<Button-1>", self.clicked, add="+")
                w.configure(cursor="hand2")

    def wrap_text(self, event):
        width= event.width-self.right_frame.winfo_reqwidth()-T.px(110)
        if width < T.px(160):
            width= T.px(160)
        self.desc_label.configure(wraplength=width)

    def mouse_enter(self, event):
        self.change_color(T.CARD_HOVER)

    def mouse_leave(self, event):
        if not mouse_is_over(self):
            self.change_color(T.CARD)

    def clicked(self, event):
        if self.enabled and self.on_click:
            self.on_click()

    def toggle_changed(self, value):
        self.state_label.configure(text=on_off(value))
        if self.on_toggle:
            self.on_toggle(value)

    def change_color(self, color):
        for w in get_all_widgets(self):
            if isinstance(w, Button) or isinstance(w, ttk.Widget):
                continue
            w.configure(bg=color)

    def set_value(self, value):
        if self.toggle:
            self.toggle.set(value)
            self.state_label.configure(text=on_off(value))

    def set_enabled(self, enabled):
        self.enabled= enabled
        if enabled:
            color= T.TEXT
        else:
            color= T.DISABLED
        self.title_label.configure(fg=color)
        if self.state_label:
            self.state_label.configure(fg=color)
        if self.toggle:
            self.toggle.set_enabled(enabled)

    def set_description(self, text):
        if self.desc_label:
            self.desc_label.configure(text=text)

    def set_chevron(self, name):
        if self.chevron_label:
            self.chevron_label.configure(text=T.glyph(name))


class DashboardCard(tk.Frame):
    def __init__(self, parent, title, description, icon, on_click):
        super().__init__(parent, bg=T.CARD, highlightthickness=1, highlightbackground=T.CARD_BORDER,
                         highlightcolor=T.CARD_BORDER)
        self.on_click= on_click
        self.pad= T.px(20)

        top= tk.Frame(self, bg=T.CARD)
        top.pack(fill="x", padx=self.pad, pady=(self.pad, T.px(14)))
        tk.Label(top, text=T.glyph(icon), font=T.icon_font(20), bg=T.CARD, fg=T.ACCENT).pack(side="left")
        tk.Label(top, text=T.glyph("chevron_right"), font=T.icon_font(11), bg=T.CARD,
                 fg=T.SUBTEXT).pack(side="right")

        self.title_label= tk.Label(self, text=title, font=T.font(12, "semibold"), bg=T.CARD, fg=T.TEXT,
                                   anchor="w", justify="left", wraplength=T.px(160))
        self.title_label.pack(fill="x", padx=self.pad)
        self.desc_label= tk.Label(self, text=description, font=T.font(10), bg=T.CARD, fg=T.SUBTEXT,
                                  anchor="nw", justify="left", wraplength=T.px(160))
        self.desc_label.pack(fill="both", expand=True, padx=self.pad, pady=(T.px(4), self.pad))

        self.bind("<Configure>", self.wrap_text)
        self.bind("<Enter>", self.mouse_enter)
        self.bind("<Leave>", self.mouse_leave)
        for w in get_all_widgets(self):
            w.bind("<Button-1>", self.clicked, add="+")
            w.configure(cursor="hand2")

    def wrap_text(self, event):
        width= event.width-2*self.pad-2
        if width < T.px(80):
            width= T.px(80)
        self.title_label.configure(wraplength=width)
        self.desc_label.configure(wraplength=width)

    def mouse_enter(self, event):
        self.change_color(T.CARD_HOVER)

    def mouse_leave(self, event):
        if not mouse_is_over(self):
            self.change_color(T.CARD)

    def clicked(self, event):
        self.on_click()

    def change_color(self, color):
        for w in get_all_widgets(self):
            w.configure(bg=color)


def card_grid(parent, cards):
    grid= tk.Frame(parent, bg=T.BG)
    grid.pack(fill="x", pady=(0, T.px(8)))
    grid.grid_columnconfigure(0, weight=1, uniform="cards")
    grid.grid_columnconfigure(1, weight=1, uniform="cards")

    index=0
    for title, description, icon, on_click in cards:
        card= DashboardCard(grid, title, description, icon, on_click)
        row= index//2
        column= index%2
        if column == 0:
            space= (0, T.px(4))
        else:
            space= (T.px(4), 0)
        card.grid(row=row, column=column, sticky="nsew", padx=space, pady=(0, T.px(8)))
        index= index+1


class Expander(tk.Frame):
    def __init__(self, parent, title, description=None, icon=None, expanded=False):
        super().__init__(parent, bg=T.BG)
        self.header= SettingRow(self, title, description, icon, on_click=self.open_close,
                                chevron="chevron_down")
        self.header.pack(fill="x")
        self.body= tk.Frame(self, bg=T.CARD, highlightthickness=1,
                            highlightbackground=T.CARD_BORDER, highlightcolor=T.CARD_BORDER)
        self.count=0
        self.expanded=False
        if expanded:
            self.open_close()

    def open_close(self):
        if self.expanded:
            self.body.pack_forget()
            self.header.set_chevron("chevron_down")
            self.expanded=False
        else:
            self.body.pack(fill="x")
            self.header.set_chevron("chevron_up")
            self.expanded=True

    def add_line(self):
        if self.count > 0:
            tk.Frame(self.body, bg=T.DIVIDER, height=1).pack(fill="x")
        self.count= self.count+1

    def row(self, title, description=None, toggle=None, on_toggle=None):
        self.add_line()
        new_row= SettingRow(self.body, title, description, toggle=toggle, on_toggle=on_toggle, nested=True)
        new_row.pack(fill="x")
        return new_row

    def frame(self):
        self.add_line()
        f= tk.Frame(self.body, bg=T.CARD)
        f.pack(fill="x", padx=(T.px(56), T.px(16)), pady=T.px(12))
        return f


def on_off(value):
    if value:
        return "On"
    return "Off"


def stack(widget):
    widget.pack(fill="x", pady=(0, T.px(4)))
    return widget


def section_header(parent, text):
    label= tk.Label(parent, text=text, font=T.font(18, "bold"), bg=T.BG, fg=T.TEXT, anchor="w")
    label.pack(fill="x", pady=(T.px(26), T.px(10)))
    return label


def paragraph(parent, text, bg=T.BG, fg=T.SUBTEXT, size=10):
    label= tk.Label(parent, text=text, font=T.font(size), bg=bg, fg=fg, anchor="w",
                    justify="left", wraplength=T.px(720))
    label.pack(fill="x", pady=(0, T.px(8)))
    return label


def toggle_row(parent, store, key, title, description=None, icon=None, default=True,
               on_change=None):
    def save_value(value):
        store.set(key, value)
        if on_change:
            on_change(value)

    row= SettingRow(parent, title, description, icon, toggle=store.get(key, default),
                    on_toggle=save_value)
    stack(row)
    return row


def radio_group(parent, store, key, options, default, on_change=None):
    choice= tk.StringVar(value=store.get(key, default))

    def save_choice():
        store.set(key, choice.get())
        if on_change:
            on_change(choice.get())

    for value, label, hint in options:
        button= tk.Radiobutton(parent, text=label, value=value, variable=choice, command=save_choice,
                               font=T.font(10), bg=T.CARD, fg=T.TEXT, activebackground=T.CARD,
                               selectcolor=T.WHITE, anchor="w", bd=0, highlightthickness=0,
                               cursor="hand2")
        button.pack(fill="x", pady=(T.px(2), 0))
        tk.Label(parent, text=hint, font=T.font(9), bg=T.CARD, fg=T.SUBTEXT, anchor="w",
                 justify="left", wraplength=T.px(620)).pack(fill="x", padx=(T.px(24), 0), pady=(0, T.px(6)))


def option_label(options, value):
    for option_value, label, hint in options:
        if option_value == value:
            return label
    return value


PRIVACY_LINKS= [
    ("About these settings and your privacy", "https://privacy.microsoft.com/"),
    ("Privacy dashboard", "https://account.microsoft.com/privacy"),
    ("Privacy Statement", "https://privacy.microsoft.com/privacystatement"),
]


def privacy_resources(parent, links=None):
    if links is None:
        links= PRIVACY_LINKS

    section_header(parent, "Related")
    card= tk.Frame(parent, bg=T.CARD, highlightthickness=1, highlightbackground=T.CARD_BORDER,
                   highlightcolor=T.CARD_BORDER)
    stack(card)
    inner= tk.Frame(card, bg=T.CARD)
    inner.pack(fill="x", padx=T.px(16), pady=T.px(13))

    icon_box= tk.Frame(inner, bg=T.CARD, width=T.px(24), height=T.px(24))
    icon_box.pack_propagate(False)
    icon_box.pack(side="left", padx=(0, T.px(16)), anchor="n")
    tk.Label(icon_box, text=T.glyph("shield"), font=T.icon_font(14), bg=T.CARD, fg=T.TEXT).pack(expand=True)

    column= tk.Frame(inner, bg=T.CARD)
    column.pack(side="left", fill="x", expand=True)
    tk.Label(column, text="Privacy resources", font=T.font(10), bg=T.CARD, fg=T.TEXT,
             anchor="w").pack(fill="x")
    row= tk.Frame(column, bg=T.CARD)
    row.pack(fill="x", pady=(T.px(2), 0))

    first=True
    for text, url in links:
        if not first:
            tk.Label(row, text="|", font=T.font(10), bg=T.CARD, fg=T.DISABLED).pack(side="left", padx=T.px(8))
        Link(row, text, url, bg=T.CARD).pack(side="left")
        first=False
