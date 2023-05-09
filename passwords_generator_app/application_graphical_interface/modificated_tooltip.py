import time
import tkinter as tk
import customtkinter as ctk
from typing import Callable, Union


class ToolTip(ctk.CTkToplevel):
    def __init__(
            self,
            widget: tk.Widget,
            msg: Union[str, Callable] = None,
            delay: float = 0.0,
            follow: bool = True,
            refresh: float = 1.0,
            x_offset: int = +10,
            y_offset: int = +10,
            label_height: int = 75,
            label_wrap_length: int = 300,
            **message_kwargs,
    ):
        self.widget = widget
        ctk.CTkToplevel.__init__(self)
        self.withdraw()
        self.overrideredirect(True)

        self.config(highlightthickness=5, highlightbackground='#808080')

        self.msg_var = ctk.StringVar()
        self.msg = msg
        self.delay = delay
        self.follow = follow
        self.refresh = refresh
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.status = 'outside'
        self.last_moved = 0
        ctk.CTkLabel(
            self,
            textvariable=self.msg_var,
            height=label_height,
            wraplength=label_wrap_length,
            corner_radius=50, **message_kwargs
        ).pack()
        self.widget.bind('<Enter>', self.on_enter, add='+')
        self.widget.bind('<Leave>', self.on_leave, add='+')
        self.widget.bind('<Motion>', self.on_enter, add='+')
        self.widget.bind('<ButtonPress>', self.on_leave, add='+')

    def on_enter(self, event) -> None:
        self.last_moved = time.time()

        if self.status == 'outside':
            self.status = 'inside'

        if not self.follow:
            self.status = 'inside'
            self.withdraw()

        self.geometry(f'+{event.x_root + self.x_offset}+{event.y_root + self.y_offset}')

        self.after(int(self.delay * 1000), self._show)

    def on_leave(self, event=None) -> None:
        self.status = 'outside'
        self.withdraw()

    def configure(self, text) -> None:
        self.msg = text

    def check_message_type(self, msg) -> None:
        if not isinstance(msg, str):
            raise TypeError(
                'ToolTip `msg` must be a string or string returning '
                f'function instead `msg` of type {type(self.msg)} was input'
            )

    def _show(self) -> None:
        if self.status == 'inside' and time.time() - self.last_moved > self.delay:
            self.status = 'visible'

        if self.status == 'visible':
            try:
                msg = self.msg()
            except TypeError:
                msg = self.msg

            self.check_message_type(msg)

            self.msg_var.set(msg)
            self.deiconify()

            self.after(int(self.refresh * 1000), self._show)
