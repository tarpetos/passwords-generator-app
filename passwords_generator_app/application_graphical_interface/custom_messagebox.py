import warnings
import tkinter

from typing import Tuple

from customtkinter import CTkToplevel, CTkFrame, CTkLabel, CTkButton


class BaseMessageBox(CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        warnings.filterwarnings('ignore', category=UserWarning)  # ignore warning about using not CTkImage
        self.MIN_MESSAGEBOX_WIDTH = 200
        self.MIN_MESSAGEBOX_HEIGHT = 100

        self.resizable(False, False)
        self.minsize(self.MIN_MESSAGEBOX_WIDTH, self.MIN_MESSAGEBOX_HEIGHT)
        self.wait_visibility()
        self.grab_set()

        self._messagebox_frame = CTkFrame(self, fg_color='transparent')
        self._messagebox_frame.pack(fill='both', expand=True, padx=5, pady=5)

        self._inner_frame = CTkFrame(self._messagebox_frame, fg_color='transparent')
        self._inner_frame.pack(fill='both', expand=True, padx=5, pady=5)

        self.messagebox_image = CTkLabel(self._inner_frame, text='')
        self.messagebox_image.pack(side='left', fill='both', expand=True, padx=(0, 5))

        self.messagebox_label = CTkLabel(self._inner_frame)
        self.messagebox_label.pack(side='left', fill='both', expand=True)

        self.info_image = '::tk::icons::information'
        self.warning_image = '::tk::icons::warning'
        self.error_image = '::tk::icons::error'
        self.question_image = '::tk::icons::question'

    def inner_frame_content(self, title: str | None, message: str | None, image: str, wrap_length: int):
        self.title(title)

        self.messagebox_image.configure(image=image)
        self.messagebox_label.configure(text=message, wraplength=wrap_length)

    def base_show(self, title: str | None, message: str | None, image: str, wrap_length: int, button_option: str):
        self.inner_frame_content(title, message, image, wrap_length)

        close_button = CTkButton(self._messagebox_frame, text=button_option, command=lambda: self.destroy())
        close_button.pack(padx=5, pady=5)
        self.wait_window()

    def base_ask(
            self,
            title: str | None,
            message: str | None,
            wrap_length: int,
            button_options: Tuple[str, str]
    ) -> bool:
        response = tkinter.BooleanVar(value=False)

        self.inner_frame_content(title, message, self.question_image, wrap_length)

        true_button = CTkButton(self._messagebox_frame, text=button_options[0], command=lambda: response.set(True))
        true_button.pack(side='left', fill='both', expand=True, padx=20, pady=5)

        false_button = CTkButton(self._messagebox_frame, text=button_options[1], command=lambda: response.set(False))
        false_button.pack(side='right', fill='both', expand=True, padx=20, pady=5)

        self.wait_variable(response)
        self.destroy()

        return response.get()


def show_info(title: str | None, message: str | None, button_option: str = 'Ok', wrap_length: int = 0) -> None:
    message_box = BaseMessageBox()
    message_box.base_show(title, message, message_box.info_image, wrap_length, button_option)


def show_error(title: str | None, message: str | None, button_option: str = 'Ok', wrap_length: int = 0) -> None:
    message_box = BaseMessageBox()
    message_box.base_show(title, message, message_box.error_image, wrap_length, button_option)


def show_warning(title: str | None, message: str | None, button_option: str = 'Ok', wrap_length: int = 0) -> None:
    message_box = BaseMessageBox()
    message_box.base_show(title, message, message_box.warning_image, wrap_length, button_option)


def ask_yes_no(
        title: str | None,
        message: str | None,
        button_options_data: Tuple[str, str] = ('Yes', 'No'),
        wrap_length: int = 0
) -> bool:
    message_box = BaseMessageBox()
    return message_box.base_ask(title, message, wrap_length, button_options_data)


def ask_ok_cancel(
        title: str | None,
        message: str | None,
        button_options_data: Tuple[str, str] = ('Ok', 'Cancel'),
        wrap_length: int = 0
) -> bool:
    message_box = BaseMessageBox()
    return message_box.base_ask(title, message, wrap_length, button_options_data)
