import customtkinter

from customtkinter import CTkButton
from tkinter.ttk import Style

from typing import Dict


class ColorConfig:
    LIGHT: str = "Light"
    DARK: str = "Dark"

    COLORS_LIGHT: Dict[str, str] = {
        "general_app_bg": LIGHT,
        "change_bg_button": "\u263C",
        "treeview_cell_bg_color": "#292929",
        "treeview_cell_font_color": "#D9D9D9",
        "treeview_scrollbar_bg": "#202020",
        "treeview_scrollbar_trough_color": "#484848",
        "treeview_scrollbar_arrow_color": "#D9D9D9",
        "treeview_input_bg": "#404040",
        "treeview_insert_color": "#007FFF",
    }

    COLORS_DARK: Dict[str, str] = {
        "general_app_bg": DARK,
        "change_bg_button": "\u263E",
        "treeview_cell_bg_color": "#D9D9D9",
        "treeview_cell_font_color": "#292929",
        "treeview_scrollbar_bg": "#686868",
        "treeview_scrollbar_trough_color": "#9B9B9B",
        "treeview_scrollbar_arrow_color": "#000000",
        "treeview_input_bg": "#E0E0E0",
        "treeview_insert_color": "#007FFF",
    }

    @classmethod
    def get_colors(cls, current_color: str = LIGHT) -> Dict[str, str]:
        return cls.COLORS_DARK if current_color == cls.LIGHT else cls.COLORS_LIGHT


def change_treeview_frame_elements_color():
    current_mode: str = customtkinter.get_appearance_mode()
    all_colors: Dict[str, str] = ColorConfig.get_colors(current_mode)

    treeview_style: Style = Style()
    treeview_style.configure(
        ".",
        background=all_colors["treeview_cell_bg_color"],
        foreground=all_colors["treeview_cell_font_color"],
    )

    treeview_style.configure(
        "TreeviewStyle.Treeview",
        borderwidth=0,
        font=("Consolas", 12),
        background=all_colors["treeview_cell_bg_color"],
        foreground=all_colors["treeview_cell_font_color"],
        fieldbackground=all_colors["treeview_input_bg"],
    )

    treeview_style.configure(
        "EntryStyle.TEntry",
        foreground=all_colors["treeview_cell_font_color"],
        fieldbackground=all_colors["treeview_cell_bg_color"],
        insertwidth=2,
        insertcolor=all_colors["treeview_insert_color"],
    )

    treeview_style.configure(
        "TScrollbar",
        gripcount=0,
        borderwidth=0,
        background=all_colors["treeview_scrollbar_bg"],
        troughcolor=all_colors["treeview_scrollbar_trough_color"],
        arrowcolor=all_colors["treeview_scrollbar_arrow_color"],
    )


def change_appearance_mode(change_bg_button: CTkButton):
    current_mode: str = customtkinter.get_appearance_mode()
    all_colors: Dict[str, str] = ColorConfig.get_colors(current_mode)

    change_bg_button.configure(text=all_colors["change_bg_button"])
    customtkinter.set_appearance_mode(all_colors["general_app_bg"])

    change_treeview_frame_elements_color()
