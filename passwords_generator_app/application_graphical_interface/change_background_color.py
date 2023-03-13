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
    return ('\u263E', BackgroundTheme.DARK.value) \
        if current_color == BackgroundTheme.LIGHT.value else ('\u263C', BackgroundTheme.LIGHT.value)


def get_bg_for_dialogs(current_color: str) -> tuple[str, str]:
    return ('#D9D9D9', '#292929') if current_color == BackgroundTheme.LIGHT.value else ('#292929', '#D9D9D9')


def get_bg_for_scrollbars(current_color: str) -> tuple[str, str, str]:
    return ('#686868', '#9B9B9B', '#000000') \
        if current_color == BackgroundTheme.LIGHT.value else ('#202020', '#484848', '#D9D9D9')


def treeview_field_background(current_color: str) -> str:
    return '#E0E0E0' if current_color == BackgroundTheme.LIGHT.value else '#404040'


def change_element_bg_color():
    current_mode = get_current_color()

    messagebox_style = Style()
    messagebox_colors = get_bg_for_dialogs(current_mode)

    messagebox_bg_color = messagebox_colors[0]
    messagebox_font_color = messagebox_colors[1]
    messagebox_style.configure('.', background=messagebox_bg_color, foreground=messagebox_font_color)

    treeview_style = Style()
    field_color = treeview_field_background(current_mode)
    treeview_style.configure(
        'TreeviewStyle.Treeview',
        borderwidth=0,
        background=messagebox_bg_color,
        foreground=messagebox_font_color,
        fieldbackground=field_color,
    )

    edit_cell_entry_style = Style()
    edit_cell_entry_style.configure(
        'EntryStyle.TEntry',
        foreground=messagebox_font_color,
        fieldbackground=messagebox_bg_color,
        insertwidth=2,
        insertcolor='#007FFF',
    )

    scrollbar_style = Style()
    scrollbar_colors = get_bg_for_scrollbars(current_mode)
    scrollbar_style.configure(
        'TScrollbar',
        gripcount=0,
        borderwidth=0,
        background=scrollbar_colors[0],
        troughcolor=scrollbar_colors[1],
        arrowcolor=scrollbar_colors[2],
    )


def change_pop_up_color(box, label) -> str:
    current_mode = get_current_color()

    pop_up_colors = get_bg_for_dialogs(current_mode)
    box_bg_color = pop_up_colors[0]
    box_font_color = pop_up_colors[1]

    box.configure(bg=box_bg_color)
    label.configure(foreground=box_font_color, background=box_bg_color)

    return box_bg_color


def change_search_box_color(canvas_widget):
    current_mode = get_current_color()

    search_box_color = get_bg_for_dialogs(current_mode)
    new_background = search_box_color[0]
    canvas_widget.configure(background=new_background)


def change_background_color(btn):
    current_mode = get_current_color()

    bg_colors = get_general_background(current_mode)
    new_btn_content = bg_colors[0]
    btn.configure(text=new_btn_content)

    new_app_theme = bg_colors[1]
    customtkinter.set_appearance_mode(new_app_theme)

    change_element_bg_color()
