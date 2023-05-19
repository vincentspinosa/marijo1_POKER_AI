import tkinter as tk
from tkinter import messagebox
from rules import player
from ui import ui
from rules import player
from helper_functions import helpers

def new_game():
    global game_ui
    sm_blind = helpers.force_gui_int_input("Small blind: ")
    bg_blind = helpers.force_gui_int_input("Big blind: ")
    players_chips = helpers.force_gui_int_input("Players chips: ")
    players = (player.Player(chips=players_chips), player.Player(chips=players_chips))
    ai_index = helpers.force_gui_int_input("AI position (Starting as Dealer: 0, Starting as Small Blind: 1): ")
    game_ui = ui.UI(players, ai_index, small_blind=sm_blind, big_blind=bg_blind)
    play_hand()

def play_hand():
    global game_ui
    if game_ui.is_game_over():
        messagebox.showinfo("Game Over", f"Game is over! Winner is player {winner}.\nChips of player {winner}: {game_ui.players[winner].chips}")
        return
    game_ui = game_ui.new_hand()
    game_ui.play_preflop()
    if not game_ui.is_hand_over():
        game_ui.play_flop()
    if not game_ui.is_hand_over():
        game_ui.play_turn()
    if not game_ui.is_hand_over():
        game_ui.play_river()
    winner = helpers.force_gui_int_input(f"Winner (0 for P0, 1 for P1): ")
    game_ui.end_round(winner)
    game_ui.move_dealer_button()
    play_hand()

root = tk.Tk()

button = tk.Button(root, 
                   text="New Game", 
                   command=new_game)
button.pack(pady=100) 

root.mainloop()
