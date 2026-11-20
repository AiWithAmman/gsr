import tkinter as tk
from tkinter import ttk

from Components import Theme as T
from Components.Buttons import Link, ToggleSwitch, pointer_inside


class ScrollFrame(tk.Frame):
    def __init__(self, parent, bg=T.BG):
        super().__init__(parent, bg=bg)
        self.canvas= tk.Canvas(self, bg=bg, highlightthickness=0, bd=0,
                                yscrollincrement=T.px(20))
        self.vsb= ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner= tk.Frame(self.canvas, bg=bg)
        self._win= self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.vsb.pack(side="right", fill="y")
        self.inner.bind("<Configure>", self._update_region)
        self.canvas.bind("<Configure>", self._fit_width)
        self.canvas.bind_all("<MouseWheel>", self._wheel)
        self.canvas.bind_all("<Button-4>", lambda e: self._scroll(-1))
        self.canvas.bind_all("<Button-5>", lambda e: self._scroll(1))

    def _update_region(self, _event=None):
        self.canvas.configure(scrollregion=(0, 0, self.inner.winfo_reqwidth(),
                                            max(self.inner.winfo_reqheight(), self.canvas.winfo_height())))

    def _fit_width(self, event):
        self.canvas.itemconfigure(self._win, width=event.width)
        self._update_region()

    def _wheel(self, event):
        steps= max(1, abs(event.delta)//120)
        self._scroll(-steps if event.delta > 0 else steps)

    def _scroll(self, units):
        try:
            if not self.canvas.winfo_exists():
                return
            if self.inner.winfo_reqheight() <= self.canvas.winfo_height():
                return
            self.canvas.yview_scroll(units*2, "units")
        except tk.TclError:
            pass


def _walk(widget):
    yield widget
    for child in widget.winfo_children():
        yield from _walk(child)


class SettingRow(tk.Frame):
    def __init__(self, parent, title, description=None, icon=None, on_click=None,
                 toggle=None, on_toggle=None, right=None, chevron=None, nested=False):
        super().__init__(parent, bg=T.CARD, highlightthickness=0 if nested else 1,
                         highlightbackground=T.CARD_BORDER, highlightcolor=T.CARD_BORDER)
        self.on_click= on_click
        self.on_toggle= on_toggle
        self.enabled=True
        self.toggle=None
        self.state_label=None
        self.chevron_label=None
        self.desc_label=None
        hoverable= on_click is not None

        body= tk.Frame(self, bg=T.CARD)
        body.pack(fill="x", padx=(T.px(56) if nested else T.px(16), T.px(16)),
                  pady=T.px(13) if description else T.px(15))

        if icon and not nested:
            box= tk.Frame(body, bg=T.CARD, width=T.px(24), height=T.px(24))
            box.pack_propagate(False)
            box.pack(side="left", padx=(0, T.px(16)))
            tk.Label(box, text=T.glyph(icon), font=T.icon_font(14), bg=T.CARD, fg=T.TEXT).pack(expand=True)

        self.right_frame= tk.Frame(body, bg=T.CARD)
        self.right_frame.pack(side="right")
        if chevron is None and on_click is not None:
            chevron="chevron_right"
        if chevron:
            self.chevron_label= tk.Label(self.right_frame, text=T.glyph(chevron), font=T.icon_font(10),
                                          bg=T.CARD, fg=T.TEXT)
            self.chevron_label.pack(side="right", padx=(T.px(12), 0))
        if right is not None:
            right(self.right_frame).pack(side="right", padx=(T.px(12), 0))
        if toggle is not None:
            self.toggle= ToggleSwitch(self.right_frame, value=toggle, command=self._toggled)
            self.toggle.pack(side="right")
            self.state_label= tk.Label(self.right_frame, text="On" if toggle else "Off",
                                        font=T.font(10), bg=T.CARD, fg=T.TEXT)
            self.state_label.pack(side="right", padx=(0, T.px(10)))

        text= tk.Frame(body, bg=T.CARD)
        text.pack(side="left", fill="x", expand=True)
        self.title_label= tk.Label(text, text=title, font=T.font(10), bg=T.CARD, fg=T.TEXT,
                                    anchor="w", justify="left")
        self.title_label.pack(fill="x")
        if description:
            self.desc_label= tk.Label(text, text=description, font=T.font(9), bg=T.CARD,
                                       fg=T.SUBTEXT, anchor="w", justify="left")
            self.desc_label.pack(fill="x")
            self.bind("<Configure>", self._rewrap)

        if hoverable:
            self.bind("<Enter>", lambda e: self._set_bg(T.CARD_HOVER))
            self.bind("<Leave>", self._leave)
            for w in _walk(self):
                if not getattr(w, "_interactive", False) and not isinstance(w, ttk.Widget):
                    w.bind("<Button-1>", self._clicked, add="+")
                    w.configure(cursor="hand2")

    def _rewrap(self, event):
        reserved= self.right_frame.winfo_reqwidth()+T.px(110)
        self.desc_label.configure(wraplength=max(T.px(160), event.width-reserved))

    def _leave(self, _event):
        if not pointer_inside(self):
            self._set_bg(T.CARD)

    def _clicked(self, _event):
        if self.enabled and self.on_click:
            self.on_click()

    def _toggled(self, value):
        self.state_label.configure(text="On" if value else "Off")
        if self.on_toggle:
            self.on_toggle(value)

    def _set_bg(self, color):
        for w in _walk(self):
            if getattr(w, "_keep_bg", False):
                continue
            try:
                w.configure(bg=color)
            except tk.TclError:
                pass

    def set_value(self, value):
        if self.toggle:
            self.toggle.set(value)
            self.state_label.configure(text="On" if value else "Off")

    def set_enabled(self, enabled):
        self.enabled= enabled
        color= T.TEXT if enabled else T.DISABLED
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


class Expander(tk.Frame):
    def __init__(self, parent, title, description=None, icon=None, expanded=False):
        super().__init__(parent, bg=T.BG)
        self.header= SettingRow(self, title, description, icon, on_click=self.toggle,
                                 chevron="chevron_down")
        self.header.pack(fill="x")
        self.body= tk.Frame(self, bg=T.CARD, highlightthickness=1,
                             highlightbackground=T.CARD_BORDER, highlightcolor=T.CARD_BORDER)
        self._count=0
        self.expanded=False
        if expanded:
            self.toggle()

    def toggle(self):
        self.expanded= not self.expanded
        if self.expanded:
            self.body.pack(fill="x")
        else:
            self.body.pack_forget()
        self.header.set_chevron("chevron_up" if self.expanded else "chevron_down")

    def _separator(self):
        if self._count:
            tk.Frame(self.body, bg=T.DIVIDER, height=1).pack(fill="x")
        self._count += 1

    def row(self, *args, **kwargs):
        self._separator()
        r= SettingRow(self.body, *args, nested=True, **kwargs)
        r.pack(fill="x")
        return r

    def frame(self):
        self._separator()
        f= tk.Frame(self.body, bg=T.CARD)
        f.pack(fill="x", padx=(T.px(56), T.px(16)), pady=T.px(12))
        return f


def stack(widget):
    widget.pack(fill="x", pady=(0, T.px(4)))
    return widget


def section_header(parent, text):
    lbl= tk.Label(parent, text=text, font=T.font(10, "semibold"), bg=T.BG, fg=T.TEXT, anchor="w")
    lbl.pack(fill="x", pady=(T.px(22), T.px(8)))
    return lbl


def paragraph(parent, text, bg=T.BG, fg=T.SUBTEXT, size=10):
    lbl= tk.Label(parent, text=text, font=T.font(size), bg=bg, fg=fg, anchor="w",
                   justify="left", wraplength=T.px(720))
    lbl.pack(fill="x", pady=(0, T.px(8)))
    return lbl


def toggle_row(parent, store, key, title, description=None, icon=None, default=True,
               on_change=None, nested=False):
    def handler(value):
        store.set(key, value)
        if on_change:
            on_change(value)

    row= SettingRow(parent, title, description, icon, toggle=store.get(key, default),
                     on_toggle=handler, nested=nested)
    if not nested:
        stack(row)
    return row


def radio_group(parent, store, key, options, default, on_change=None):
    var= tk.StringVar(value=store.get(key, default))

    def changed():
        store.set(key, var.get())
        if on_change:
            on_change(var.get())

    for value, label, hint in options:
        rb= tk.Radiobutton(parent, text=label, value=value, variable=var, command=changed,
                            font=T.font(10), bg=T.CARD, fg=T.TEXT, activebackground=T.CARD,
                            selectcolor=T.WHITE, anchor="w", bd=0, highlightthickness=0,
                            cursor="hand2")
        rb.pack(fill="x", pady=(T.px(2), 0))
        if hint:
            tk.Label(parent, text=hint, font=T.font(9), bg=T.CARD, fg=T.SUBTEXT, anchor="w",
                     justify="left", wraplength=T.px(620)).pack(fill="x", padx=(T.px(24), 0),
                                                                  pady=(0, T.px(6)))
    return var


PRIVACY_LINKS= [
    ("About these settings and your privacy", "https://privacy.microsoft.com/"),
    ("Privacy dashboard", "https://account.microsoft.com/privacy"),
    ("Privacy Statement", "https://privacy.microsoft.com/privacystatement"),
]


def privacy_resources(parent, links=None):
    section_header(parent, "Related")
    card= tk.Frame(parent, bg=T.CARD, highlightthickness=1, highlightbackground=T.CARD_BORDER,
                    highlightcolor=T.CARD_BORDER)
    stack(card)
    inner= tk.Frame(card, bg=T.CARD)
    inner.pack(fill="x", padx=T.px(16), pady=T.px(13))
    box= tk.Frame(inner, bg=T.CARD, width=T.px(24), height=T.px(24))
    box.pack_propagate(False)
    box.pack(side="left", padx=(0, T.px(16)), anchor="n")
    tk.Label(box, text=T.glyph("shield"), font=T.icon_font(14), bg=T.CARD, fg=T.TEXT).pack(expand=True)
    col= tk.Frame(inner, bg=T.CARD)
    col.pack(side="left", fill="x", expand=True)
    tk.Label(col, text="Privacy resources", font=T.font(10), bg=T.CARD, fg=T.TEXT,
             anchor="w").pack(fill="x")
    row= tk.Frame(col, bg=T.CARD)
    row.pack(fill="x", pady=(T.px(2), 0))
    for i, (text, url) in enumerate(links or PRIVACY_LINKS):
        if i:
            tk.Label(row, text="|", font=T.font(9), bg=T.CARD, fg=T.DISABLED).pack(side="left", padx=T.px(6))
        Link(row, text, url, bg=T.CARD).pack(side="left")
    return card
