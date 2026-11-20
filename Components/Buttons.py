import tkinter as tk
import webbrowser

from Components import Theme as T


def pointer_inside(widget):
    try:
        x, y= widget.winfo_pointerxy()
        w= widget.winfo_containing(x, y)
    except (KeyError, tk.TclError):
        return False
    while w is not None:
        if w is widget:
            return True
        w= getattr(w, "master", None)
    return False


class ToggleSwitch(tk.Canvas):
    _interactive=True

    def __init__(self, parent, value=False, command=None, bg=T.CARD, enabled=True):
        self.w, self.h= T.px(40), T.px(20)
        super().__init__(parent, width=self.w+2, height=self.h+2, bg=bg,
                         highlightthickness=0, bd=0, cursor="hand2")
        self.value= bool(value)
        self.command= command
        self.enabled= enabled
        self._hover=False
        self.bind("<Button-1>", self._click)
        self.bind("<Enter>", lambda e: self._set_hover(True))
        self.bind("<Leave>", lambda e: self._set_hover(False))
        self.bind("<space>", self._click)
        self._draw()

    def _set_hover(self, hover):
        self._hover= hover
        self._draw()

    def _click(self, _event=None):
        if not self.enabled:
            return
        self.set(not self.value, notify=True)

    def set(self, value, notify=False):
        self.value= bool(value)
        self._draw()
        if notify and self.command:
            self.command(self.value)

    def set_enabled(self, enabled):
        self.enabled= enabled
        self.configure(cursor="hand2" if enabled else "arrow")
        self._draw()

    def configure(self, cnf=None, **kw):
        result= super().configure(cnf, **kw)
        if "bg" in kw or "background" in kw:
            self._draw()
        return result

    config= configure

    def _draw(self):
        self.delete("all")
        r= self.h/2
        x0, x1, y=1+r, 1+self.w-r, 1+r
        if self.value:
            fill= (T.ACCENT_HOVER if self._hover else T.ACCENT) if self.enabled else T.DISABLED
            border, knob= fill, T.WHITE
        else:
            fill= ("#ededed" if self._hover else T.WHITE) if self.enabled else T.WHITE
            border= knob= T.SUBTEXT if self.enabled else T.DISABLED
        self.create_line(x0, y, x1, y, width=self.h, capstyle="round", fill=border)
        self.create_line(x0, y, x1, y, width=self.h-2, capstyle="round", fill=fill)
        kr= T.px(6) if (self._hover and self.enabled) else T.px(5)
        kx= x1 if self.value else x0
        self.create_oval(kx-kr, y-kr, kx+kr, y+kr, fill=knob, outline=knob)


class Button(tk.Label):
    _interactive=True
    _keep_bg=True

    def __init__(self, parent, text, command=None, accent=False, enabled=True):
        super().__init__(parent, text=text, font=T.font(10), padx=T.px(14), pady=T.px(4),
                         bd=0, highlightthickness=1)
        self.command= command
        self.accent= accent
        self.enabled= enabled
        self._hover=False
        self.bind("<Enter>", lambda e: self._set_hover(True))
        self.bind("<Leave>", lambda e: self._set_hover(False))
        self.bind("<ButtonRelease-1>", self._click)
        self._apply()

    def _set_hover(self, hover):
        self._hover= hover
        self._apply()

    def _click(self, _event=None):
        if self.enabled and self.command and pointer_inside(self):
            self.command()

    def set_enabled(self, enabled):
        self.enabled= enabled
        self._apply()

    def _apply(self):
        if not self.enabled:
            bg, fg, border= ("#c8c8c8", T.WHITE, "#c8c8c8") if self.accent else ("#f5f5f5", T.DISABLED, T.CARD_BORDER)
        elif self.accent:
            bg= T.ACCENT_HOVER if self._hover else T.ACCENT
            fg, border= T.WHITE, bg
        else:
            bg="#f6f6f6" if self._hover else T.WHITE
            fg, border= T.TEXT, T.CARD_BORDER
        tk.Label.configure(self, bg=bg, fg=fg, highlightbackground=border, highlightcolor=border,
                           cursor="hand2" if self.enabled else "arrow")


class Link(tk.Label):
    _interactive=True
    _keep_fg=True

    def __init__(self, parent, text, target, bg=T.BG):
        super().__init__(parent, text=text, font=T.font(10), fg=T.ACCENT, bg=bg, cursor="hand2")
        self.target= target
        self.bind("<Enter>", lambda e: self.configure(font=T.font(10)+("underline",)))
        self.bind("<Leave>", lambda e: self.configure(font=T.font(10)))
        self.bind("<Button-1>", self._open)

    def _open(self, _event=None):
        if callable(self.target):
            self.target()
        else:
            webbrowser.open(self.target)
