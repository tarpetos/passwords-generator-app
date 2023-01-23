def label_lang_change(labels_dict, list_of_labels):
    for label_number, label in enumerate(labels_dict):
        labels_dict[label].config(text=list_of_labels[label_number])


def btn_lang_change(buttons_dict, list_of_buttons):
    for btn_number, btn in enumerate(buttons_dict):
        buttons_dict[btn].config(text=list_of_buttons[btn_number])


def radiobtn_lang_change(radiobtns_dict, list_of_radiobtns):
    for btn_number, btn in enumerate(radiobtns_dict):
        radiobtns_dict[btn].config(text=list_of_radiobtns[btn_number])
