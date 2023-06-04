import tkinter as tk

class CardSelectionWindow:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Select a card")
        self.selected_index = tk.IntVar()

    def on_button_click(self, index):
        # When a button is clicked, we store the index of the card
        self.selected_index.set(index)
        # Then we destroy the window to end the mainloop
        """ self.window.destroy() """


