import tkinter as tk
import webbrowser

from Components import Theme as T


def mouse_is_over(widget):
    x, y= widget.winfo_pointerxy()
    try:
        w= widget.winfo_containing(x, y)
    except KeyError:
        return False
    while w is not None:
        if w == widget:
            return True
        w= w.master
    return False


class ToggleSwitch(tk.Canvas):
    def __init__(self, parent, value=False, command=None):
        self.w= T.px(40)
        self.h= T.px(20)
        super().__init__(parent, width=self.w+2, height=self.h+2, bg=T.CARD,
                         highlightthickness=0, bd=0, cursor="hand2")
        self.value= value
        self.command= command
        self.enabled=True
        self.hover=False
        self.bind("<Button-1>", self.click)
        self.bind("<Enter>", self.mouse_enter)
        self.bind("<Leave>", self.mouse_leave)
        self.draw()

    def mouse_enter(self, event):
        self.hover=True
        self.draw()

    def mouse_leave(self, event):
        self.hover=False
        self.draw()

    def click(self, event):
        if not self.enabled:
            return
        self.value= not self.value
        self.draw()
        if self.command:
            self.command(self.value)

    def set(self, value):
        self.value= value
        self.draw()

    def set_enabled(self, enabled):
        self.enabled= enabled
        if enabled:
            self.configure(cursor="hand2")
        else:
            self.configure(cursor="arrow")
        self.draw()

    def draw(self):
        self.delete("all")

        if self.value and self.enabled:
            if self.hover:
                fill= T.ACCENT_HOVER
            else:
                fill= T.ACCENT
            border= fill
            knob= T.WHITE
        elif self.value:
            fill= T.DISABLED
            border= T.DISABLED
            knob= T.WHITE
        elif self.enabled:
            if self.hover:
                fill="#ededed"
            else:
                fill= T.WHITE
            border= T.SUBTEXT
            knob= T.SUBTEXT
        else:
            fill= T.WHITE
            border= T.DISABLED
            knob= T.DISABLED

        radius= self.h/2
        left= 1+radius
        right= 1+self.w-radius
        middle= 1+radius
        self.create_line(left, middle, right, middle, width=self.h, capstyle="round", fill=border)
        self.create_line(left, middle, right, middle, width=self.h-2, capstyle="round", fill=fill)

        if self.hover and self.enabled:
            knob_size= T.px(6)
        else:
            knob_size= T.px(5)
        if self.value:
            knob_x= right
        else:
            knob_x= left
        self.create_oval(knob_x-knob_size, middle-knob_size, knob_x+knob_size, middle+knob_size,
                         fill=knob, outline=knob)


class Button(tk.Label):
    def __init__(self, parent, text, command=None, accent=False, enabled=True):
        super().__init__(parent, text=text, font=T.font(10), padx=T.px(14), pady=T.px(4),
                         bd=0, highlightthickness=1)
        self.command= command
        self.accent= accent
        self.enabled= enabled
        self.hover=False
        self.bind("<Enter>", self.mouse_enter)
        self.bind("<Leave>", self.mouse_leave)
        self.bind("<ButtonRelease-1>", self.click)
        self.update_colors()

    def mouse_enter(self, event):
        self.hover=True
        self.update_colors()

    def mouse_leave(self, event):
        self.hover=False
        self.update_colors()

    def click(self, event):
        if self.enabled and self.command and mouse_is_over(self):
            self.command()

    def set_enabled(self, enabled):
        self.enabled= enabled
        self.update_colors()

    def update_colors(self):
        if not self.enabled:
            if self.accent:
                bg="#c8c8c8"
                fg= T.WHITE
                border="#c8c8c8"
            else:
                bg="#f5f5f5"
                fg= T.DISABLED
                border= T.CARD_BORDER
        elif self.accent:
            if self.hover:
                bg= T.ACCENT_HOVER
            else:
                bg= T.ACCENT
            fg= T.WHITE
            border= bg
        else:
            if self.hover:
                bg="#f6f6f6"
            else:
                bg= T.WHITE
            fg= T.TEXT
            border= T.CARD_BORDER

        if self.enabled:
            cursor="hand2"
        else:
            cursor="arrow"
        self.configure(bg=bg, fg=fg, highlightbackground=border, highlightcolor=border, cursor=cursor)


class Link(tk.Label):
    def __init__(self, parent, text, url, bg=T.BG):
        super().__init__(parent, text=text, font=T.font(11), fg=T.ACCENT, bg=bg, cursor="hand2",
                         pady=T.px(2))
        self.url= url
        self.bind("<Enter>", self.mouse_enter)
        self.bind("<Leave>", self.mouse_leave)
        self.bind("<Button-1>", self.open_link)

    def mouse_enter(self, event):
        family= T.font(11)[0]
        self.configure(font=(family, 11, "underline"))

    def mouse_leave(self, event):
        self.configure(font=T.font(11))

    def open_link(self, event):
        webbrowser.open(self.url)
