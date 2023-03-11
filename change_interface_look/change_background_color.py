import customtkinter

from tkinter.ttk import Style
from enum import Enum


class BackgroundTheme(Enum):
    LIGHT = 'Light'
    DARK = 'Dark'


def get_current_color() -> str:
    current_mode = customtkinter.get_appearance_mode()
    return current_mode


def get_general_background(current_color: str) -> tuple[str, str]:
    return ('\u263E', BackgroundTheme.DARK.value) if current_color == BackgroundTheme.LIGHT.value else ('\u263C', BackgroundTheme.LIGHT.value)


def get_bg_for_dialogs(current_color: str) -> tuple[str, str]:
    return ('#D9D9D9', '#292929') if current_color == BackgroundTheme.LIGHT.value else ('#292929', '#D9D9D9')


def change_messagebox_color():
    current_mode = get_current_color()

    messagebox_style = Style()
    edit_cell_entry_style = Style()

    messagebox_bg_color = get_bg_for_dialogs(current_mode)[0]
    messagebox_font_color = get_bg_for_dialogs(current_mode)[1]
    messagebox_style.configure('.', background=messagebox_bg_color, foreground=messagebox_font_color)
    edit_cell_entry_style.configure(
        'EntryStyle.TEntry',
        foreground=messagebox_font_color,
        fieldbackground=messagebox_bg_color,
        insertwidth=2,
        insertcolor='#007FFF',
    )


def change_pop_up_color(box, label) -> str:
    current_mode = get_current_color()

    box_bg_color = get_bg_for_dialogs(current_mode)[0]
    box_font_color = get_bg_for_dialogs(current_mode)[1]

    box.configure(bg=box_bg_color)
    label.configure(foreground=box_font_color, background=box_bg_color)

    return box_bg_color


def change_search_box_color(canvas_widget):
    current_mode = get_current_color()

    new_background = get_bg_for_dialogs(current_mode)[0]
    canvas_widget.configure(background=new_background)


def change_background_color(btn):
    current_mode = get_current_color()
    new_btn_content = get_general_background(current_mode)[0]
    btn.configure(text=new_btn_content)

    new_app_theme = get_general_background(current_mode)[1]
    customtkinter.set_appearance_mode(new_app_theme)

    change_messagebox_color()
