from enum import Enum


class BackgroundTheme(Enum):
    LIGHT = '#F0F0F0'
    DARK = 'black'


class ChangeAppBackgroundTheme:
    def __init__(self):
        self.bg_color = BackgroundTheme.LIGHT

    def set_color_to_labels(self, labels_dict, opposite_color, current_color):
        for label_key in labels_dict.items().mapping.values():
            label_key.config(background=opposite_color, foreground=current_color)

    def get_opposite_color(self, current_color):
        return BackgroundTheme.DARK if current_color == BackgroundTheme.LIGHT else BackgroundTheme.LIGHT

    def get_btn_content(self, opposite_color):
        return '\u263C' if opposite_color == BackgroundTheme.LIGHT else '\u263E'

    def change_background_color(self, root, frame, labels_dict, btn):
        opposite_color = self.get_opposite_color(self.bg_color)
        bg_current_color_code = self.bg_color.value
        bg_opposite_color_code = opposite_color.value
        root.config(background=bg_opposite_color_code)
        frame.config(background=bg_opposite_color_code)
        self.set_color_to_labels(labels_dict, bg_opposite_color_code, bg_current_color_code)
        btn.config(text=self.get_btn_content(opposite_color))
        self.bg_color = opposite_color
