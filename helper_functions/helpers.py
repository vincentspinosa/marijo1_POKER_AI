from tkinter import messagebox, simpledialog

def force_int_input(question):
    answer = input(question)
    try:
        return int(answer)
    except:
        return force_int_input(question)

def force_gui_int_input(question):
    while True:
        try:
            return simpledialog.askinteger("Input", question)
        except ValueError:
            messagebox.showwarning("Invalid input", "Please enter a valid integer.")