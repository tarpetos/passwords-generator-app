from typing import Tuple

from customtkinter import CTkLabel, CTkEntry, CTkButton, CTkInputDialog


class ExpandedCTkInputDialog(CTkInputDialog):
    def __init__(self, title: str = 'Title', text: str = 'Text', button_options: Tuple[str, str] = ('Ok', 'Cancel')):
        super().__init__(title=title, text=text)
        self._ok_button_text = button_options[0]
        self._cancel_button_text = button_options[1]

    def _create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self._label = CTkLabel(
            master=self,
            width=300,
            wraplength=300,
            fg_color='transparent',
            text_color=self._text_color,
            text=self._text,
        )
        self._label.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky='ew')

        self._entry = CTkEntry(
            master=self,
            width=230,
            fg_color=self._entry_fg_color,
            border_color=self._entry_border_color,
            text_color=self._entry_text_color
        )
        self._entry.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky='ew')

        self._ok_button = CTkButton(
            master=self,
            width=100,
            border_width=0,
            fg_color=self._button_fg_color,
            hover_color=self._button_hover_color,
            text_color=self._button_text_color,
            text=self._ok_button_text,
            command=self._ok_event
        )
        self._ok_button.grid(row=2, column=0, columnspan=1, padx=(20, 10), pady=(0, 20), sticky='ew')

        self._cancel_button = CTkButton(
            master=self,
            width=100,
            border_width=0,
            fg_color=self._button_fg_color,
            hover_color=self._button_hover_color,
            text_color=self._button_text_color,
            text=self._cancel_button_text,
            command=self._cancel_event
        )
        self._cancel_button.grid(row=2, column=1, columnspan=1, padx=(10, 20), pady=(0, 20), sticky='ew')

        self.after(150, lambda: self._entry.focus())
        self._entry.bind('<Return>', self._ok_event)
