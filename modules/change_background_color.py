from enum import Enum
from tkinter.ttk import Style


class BackgroundTheme(Enum):
    LIGHT = '#F0F0F0'
    DARK = 'black'


def set_color_to_labels(labels_dict, opposite_color, current_color):
    for label_key in labels_dict.items().mapping.values():
        label_key.config(background=opposite_color, foreground=current_color)


def get_opposite_color(current_color):
    return BackgroundTheme.DARK if current_color == BackgroundTheme.LIGHT else BackgroundTheme.LIGHT


def get_btn_content(opposite_color):
    return '\u263C' if opposite_color == BackgroundTheme.LIGHT else '\u263E'


def set_color_to_radiobtn(radiobtn_dict, opposite_color, current_color):
    radio_button_style = Style()
    radio_button_style.configure(
        'Wild.TRadiobutton',
        background=opposite_color,
        foreground=current_color,
    )

    for radiobtn_key in radiobtn_dict.items().mapping.values():
        radiobtn_key.config(style='Wild.TRadiobutton')


class ChangeAppBackgroundTheme:
    def __init__(self):
        self.bg_color = BackgroundTheme.LIGHT
        self.bg_table_color = BackgroundTheme.LIGHT

    def change_background_color(self, app, frame, labels_dict, btn, radiobtn_dict):
        opposite_color = get_opposite_color(self.bg_color)
        bg_current_color_code = self.bg_color.value
        bg_opposite_color_code = opposite_color.value
        app.config(background=bg_opposite_color_code)
        frame.config(background=bg_opposite_color_code)
        set_color_to_labels(labels_dict, bg_opposite_color_code, bg_current_color_code)
        set_color_to_radiobtn(radiobtn_dict, bg_opposite_color_code, bg_current_color_code)
        btn.config(text=get_btn_content(opposite_color))
        self.bg_color = opposite_color

    def change_table_page_background_color(self, app, table_page_frame, btn):
        opposite_color = get_opposite_color(self.bg_table_color)
        bg_opposite_color_code = opposite_color.value
        app.config(background=bg_opposite_color_code)
        table_page_frame.config(background=bg_opposite_color_code)
        btn.config(text=get_btn_content(opposite_color))
        self.bg_table_color = opposite_color
