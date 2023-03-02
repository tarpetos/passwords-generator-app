def label_lang_change(labels_dict, list_of_labels):
    for label_number, label in enumerate(labels_dict):
        labels_dict[label].configure(text=list_of_labels[label_number])


def btn_lang_change(buttons_dict, list_of_buttons):
    for btn_number, btn in enumerate(buttons_dict):
        buttons_dict[btn].configure(text=list_of_buttons[btn_number])
