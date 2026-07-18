import tkinter as tk

class SummaryCard(tk.Frame):
    def __init__(self, parent, title, value):
        super().__init__(parent, relief="ridge", borderwidth=2)

        self.title_label = tk.Label(self, text=title, font=("Arial", 10))
        self.title_label.pack(padx=10, pady=(10, 0))

        self.value_label = tk.Label(self, text=value, font=("Arial", 16, "bold"))
        self.value_label.pack(padx=10, pady=(0, 10))

    def update_value(self, new_value):
        self.value_label.config(text=new_value)


class ValidatedEntry(tk.Entry):
    def __init__(self, parent, validate_function):
        super().__init__(parent)
        self.validate_function = validate_function
        self.bind("<FocusOut>", self.on_focus_out)

    def on_focus_out(self, event):
        text = self.get()
        is_valid = self.validate_function(text)

        if is_valid == True:
            self.config(bg="white")
        else:
            self.config(bg="#ffdddd")

    def is_valid(self):
        text = self.get()
        return self.validate_function(text)


class ConfirmDialog:
    @staticmethod
    def ask(title, message):
        result = messagebox.askyesno(title, message)
        return result

