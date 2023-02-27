from enum import Enum
from tkinter import ttk
from tkinter.ttk import Style


class BackgroundTheme(Enum):
    LIGHT = '#D3D3D3'
    MAX_LIGHT = 'white'
    DARK = 'black'


def set_color_to_labels(labels_dict, opposite_color, current_color):
    for label_key in labels_dict.items().mapping.values():
        label_key.config(background=opposite_color, foreground=current_color)


def change_buttons_border_color(current_color, opposite_color, bg_opposite_color_code):
    style_config = ttk.Style()

    if opposite_color == BackgroundTheme.DARK:
        btn_color = 'gray'
    else:
        btn_color = BackgroundTheme.MAX_LIGHT.value

    style_config.configure('TButton', background=btn_color)
    style_config.configure('TFrame', background=bg_opposite_color_code)
    btn_label_color = get_btn_label_color(opposite_color)
    style_config.configure('.', background=bg_opposite_color_code, foreground=btn_label_color)


def get_opposite_color(current_color):
    return BackgroundTheme.DARK if current_color == BackgroundTheme.LIGHT else BackgroundTheme.LIGHT


def get_btn_content(opposite_color):
    return '\u263C' if opposite_color == BackgroundTheme.LIGHT else '\u263E'


def get_btn_label_color(opposite_color):
    return BackgroundTheme.DARK.value if opposite_color == BackgroundTheme.LIGHT else BackgroundTheme.MAX_LIGHT.value


def set_color_to_radiobtn(radiobtn_dict, opposite_color, current_color):
    radio_button_style = Style()
    radio_button_style.configure(
        'TRadiobutton',
        background=opposite_color,
        foreground=current_color,
    )
    radio_button_style.map('TRadiobutton', background=[('active', opposite_color)])


class AppBackgroundTheme:
    def __init__(self):
        self.bg_color = BackgroundTheme.LIGHT
        self.bg_table_color = BackgroundTheme.LIGHT

    def change_background_color(self, labels_dict, btn, radiobtn_dict):
        opposite_color = get_opposite_color(self.bg_color)
        bg_current_color_code = self.bg_color.value
        bg_opposite_color_code = opposite_color.value
        set_color_to_labels(labels_dict, bg_opposite_color_code, bg_current_color_code)
        set_color_to_radiobtn(radiobtn_dict, bg_opposite_color_code, bg_current_color_code)
        btn.config(text=get_btn_content(opposite_color))
        change_buttons_border_color(bg_current_color_code, opposite_color, bg_opposite_color_code)
        self.bg_color = opposite_color
