from tkinter.ttk import Style


def change_text_pos():
    text_positioning_radiobuttons = Style()

    text_positioning_radiobuttons.layout(
        'TRadiobutton', [
            ('Radiobutton.padding', {'children':
                [('Radiobutton.indicator', {'side': 'top', 'sticky': ''}),
                    ('Radiobutton.focus', {'side': 'left', 'children':
                        [('Radiobutton.label', {'sticky': 'nswe'})], 'sticky': ''})]
        })]
    )
