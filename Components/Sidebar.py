import tkinter as tk

from Components import Theme as T
from Components.Buttons import mouse_is_over

PLACEHOLDER="Find a setting"


class NavItem(tk.Frame):
    def __init__(self, parent, key, text, icon, command, placeholder):
        if placeholder:
            cursor="arrow"
            color= T.SUBTEXT
        else:
            cursor="hand2"
            color= T.TEXT
        super().__init__(parent, bg=T.BG, height=T.px(36), cursor=cursor)
        self.pack_propagate(False)
        self.key= key
        self.command= command
        self.placeholder= placeholder
        self.selected=False

        self.icon= tk.Label(self, text=T.glyph(icon), font=T.icon_font(12), bg=T.BG, fg=color,
                            width=2, cursor=cursor)
        self.icon.pack(side="left", padx=(T.px(14), T.px(10)))
        self.label= tk.Label(self, text=text, font=T.font(10), bg=T.BG, fg=color, anchor="w",
                             cursor=cursor)
        self.label.pack(side="left", fill="x", expand=True)
        self.indicator= tk.Frame(self, bg=T.BG, width=T.px(3))
        self.indicator.place(x=0, rely=0.5, anchor="w", height=T.px(16))

        for w in [self, self.icon, self.label, self.indicator]:
            w.bind("<Button-1>", self.clicked)
            w.bind("<Enter>", self.mouse_enter)
            w.bind("<Leave>", self.mouse_leave)

    def clicked(self, event):
        self.command(self.key)

    def mouse_enter(self, event):
        if not self.placeholder:
            self._paint(True)

    def mouse_leave(self, event):
        self._paint(mouse_is_over(self))

    def set_selected(self, selected):
        self.selected= selected
        self._paint(False)

    def _paint(self, hover):
        if self.selected:
            bg= T.NAV_SELECTED
        elif hover:
            bg= T.NAV_HOVER
        else:
            bg= T.BG
        self.configure(bg=bg)
        self.icon.configure(bg=bg)
        self.label.configure(bg=bg)
        if self.selected:
            self.indicator.configure(bg=T.ACCENT)
        else:
            self.indicator.configure(bg=bg)


class Sidebar(tk.Frame):
    def __init__(self, parent, items, on_select, on_search):
        super().__init__(parent, bg=T.BG, width=T.px(300))
        self.pack_propagate(False)
        self.on_select= on_select
        self.on_search= on_search
        self.items={}

        self._build_profile()
        self._build_search()

        nav= tk.Frame(self, bg=T.BG)
        nav.pack(fill="x", padx=(T.px(8), T.px(12)), pady=(T.px(4), 0))
        for key, text, icon in items:
            if key == "home" or key == "privacy":
                placeholder=False
            else:
                placeholder=True
            item= NavItem(nav, key, text, icon, on_select, placeholder)
            item.pack(fill="x", pady=(0, T.px(2)))
            self.items[key]= item

    def _build_profile(self):
        box= tk.Frame(self, bg=T.BG)
        box.pack(fill="x", padx=T.px(20), pady=(T.px(8), T.px(16)))
        size= T.px(64)
        avatar= tk.Canvas(box, width=size, height=size, bg=T.BG, highlightthickness=0)
        avatar.create_oval(1, 1, size-1, size-1, fill="#d6d6d6", outline="#d6d6d6")
        avatar.create_text(size/2, size/2, text=T.glyph("person") or "☺",
                           font=T.icon_font(22), fill=T.WHITE)
        avatar.pack(side="left")
        info= tk.Frame(box, bg=T.BG)
        info.pack(side="left", padx=(T.px(14), 0))
        tk.Label(info, text="Local user", font=T.font(11, "semibold"), bg=T.BG, fg=T.TEXT,
                 anchor="w").pack(fill="x")
        tk.Label(info, text="Local Account", font=T.font(9), bg=T.BG, fg=T.SUBTEXT,
                 anchor="w").pack(fill="x")

    def _build_search(self):
        self.search_box= tk.Frame(self, bg=T.WHITE, highlightthickness=1,
                                   highlightbackground=T.CARD_BORDER, highlightcolor=T.CARD_BORDER)
        self.search_box.pack(fill="x", padx=(T.px(16), T.px(16)), pady=(0, T.px(10)))
        self.entry= tk.Entry(self.search_box, bd=0, relief="flat", font=T.font(10), bg=T.WHITE,
                              fg=T.SUBTEXT, insertbackground=T.TEXT, highlightthickness=0)
        self.entry.pack(side="left", fill="x", expand=True, padx=(T.px(10), 0), pady=T.px(6))
        tk.Label(self.search_box, text=T.glyph("search"), font=T.icon_font(10), bg=T.WHITE,
                 fg=T.SUBTEXT).pack(side="right", padx=T.px(10))
        self.entry.insert(0, PLACEHOLDER)
        self.entry.bind("<FocusIn>", self._focus_in)
        self.entry.bind("<FocusOut>", self._focus_out)
        self.entry.bind("<Return>", self._submit)
        self.entry.bind("<Escape>", self._clear)

    def _clear(self, event):
        self.entry.delete(0, "end")
        self.focus_set()

    def _focus_in(self, _event):
        if self.entry.get() == PLACEHOLDER:
            self.entry.delete(0, "end")
            self.entry.configure(fg=T.TEXT)
        self.search_box.configure(highlightbackground=T.ACCENT, highlightcolor=T.ACCENT)

    def _focus_out(self, _event):
        if not self.entry.get():
            self.entry.insert(0, PLACEHOLDER)
            self.entry.configure(fg=T.SUBTEXT)
        self.search_box.configure(highlightbackground=T.CARD_BORDER, highlightcolor=T.CARD_BORDER)

    def _submit(self, _event):
        text= self.entry.get().strip()
        if text and text != PLACEHOLDER:
            self.on_search(text)

    def select(self, key):
        for item_key in self.items:
            if item_key == key:
                self.items[item_key].set_selected(True)
            else:
                self.items[item_key].set_selected(False)
