from tkinter import messagebox, Label, Entry
from tkinter.constants import LEFT, W, END, E
from tkinter.simpledialog import Dialog
from customtkinter import CTkLabel, CTkEntry


class _CustomDialog(Dialog):
    def __init__(self, title, prompt, lang_state, initialvalue=None, parent=None):
        self.prompt = prompt

        self.initialvalue = initialvalue

        self.lang_state = lang_state

        Dialog.__init__(self, parent, title)

    def destroy(self):
        self.entry = None
        Dialog.destroy(self)

    def body(self, master):
        self.winfo_toplevel().wm_resizable(False, False)

        w = Label(master, text=self.prompt, justify=LEFT)
        w.grid(row=0, padx=5, sticky=W)

        self.entry = Entry(master, name="entry")
        self.entry.grid(row=1, padx=5, sticky=W + E)

        if self.initialvalue is not None:
            self.entry.insert(0, self.initialvalue)
            self.entry.select_range(0, END)

        return self.entry

    def validate(self):
        try:
            result = self.getresult()
        except ValueError:
            if self.lang_state:
                messagebox.showwarning(
                    "Invalid input",
                    "Not an integer! Try again.",
                    parent=self
                )
            else:
                messagebox.showwarning(
                    "Некоректний ввід",
                    "Введено не ціле число! Спробуйте ще раз.",
                    parent=self
                )
            return 0

        self.result = result

        return 1


class _QueryInteger(_CustomDialog):
    def getresult(self):
        return self.getint(self.entry.get())


def askinteger(title, prompt, lang_state, **kw):
    d = _QueryInteger(title, prompt, lang_state, **kw)
    return d.result


class _QueryString(_CustomDialog):
    def __init__(self, *args, **kw):
        if 'show' in kw:
            self.__show = kw['show']
            del kw['show']
        else:
            self.__show = None
        _CustomDialog.__init__(self, *args, **kw)

    def body(self, master):
        entry = _CustomDialog.body(self, master)
        if self.__show is not None:
            entry.configure(show=self.__show)
        return entry

    def getresult(self):
        return self.entry.get()


def askstring(title, prompt, lang_state, **kw):
    d = _QueryString(title, prompt, lang_state, **kw)
    return d.result


class CustomAskIntegerDialog(Dialog):
    def __init__(self, title, prompt, lang_state, initialvalue=None, parent=None):
        self.prompt = prompt
        self.initialvalue = initialvalue
        self.lang_state = lang_state
        super().__init__(parent, title)

    def body(self, master):
        self.winfo_toplevel().wm_resizable(False, False)
        w = CTkLabel(master, text=self.prompt, justify=LEFT, text_color='black')
        w.grid(row=0, padx=5, sticky=W)

        self.entry = CTkEntry(master)
        self.entry.grid(row=1, padx=5, sticky=W + E)

        if self.initialvalue is not None:
            self.entry.insert(0, self.initialvalue)
            self.entry.select_range(0, END)

        return self.entry

    def validate(self):
        try:
            result = self.getresult()
        except ValueError:
            if self.lang_state:
                messagebox.showwarning(
                    "Invalid input",
                    "Not an integer! Try again.",
                    parent=self
                )
            else:
                messagebox.showwarning(
                    "Некоректний ввід",
                    "Введено не ціле число! Спробуйте ще раз.",
                    parent=self
                )
            return 0

        self.result = result

        return 1

    def getresult(self):
        return self.getint(self.entry.get())


def custom_askinteger(title, prompt, lang_state, **kw):
    dialog = CustomAskIntegerDialog(title, prompt, lang_state, **kw)
    return dialog.result
