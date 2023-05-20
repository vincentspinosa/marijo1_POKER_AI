import tkinter as tk
from tkinter import messagebox
from rules import player
from ui import ui
from rules import player
from helper_functions import helpers

def new_game():
    global game_ui
    sm_blind = helpers.force_gui_int_input("Small blind: ")
    players_chips = helpers.force_gui_int_input("Players chips: ")
    players = (player.Player(chips=players_chips), player.Player(chips=players_chips))
    first_dealer = helpers.force_gui_int_input("First dealer position (AI: 0, Opposite player: 1): ")
    game_ui = ui.UI(players, target_player_index=0, dealer_position=first_dealer, small_blind=sm_blind, big_blind=(sm_blind * 2))
    play_hand()

def play_hand():
    global game_ui
    game_ui = game_ui.new_hand()
    game_ui.start_round('pre-flop')
    if not game_ui.is_hand_over():
        game_ui.start_round('flop')
    if not game_ui.is_hand_over():
        game_ui.start_round('turn')
    if not game_ui.is_hand_over():
        game_ui.start_round('river')
    winner = helpers.force_gui_int_input(f"Winner (AI: 0, Opposite player: 1): ")
    game_ui.end_round(winner)
    game_ui.move_dealer_button()
    if game_ui.is_game_over():
        messagebox.showinfo("Game Over", f"Game is over! Winner is player {winner}.\nChips of player {winner}: {game_ui.players[winner].chips}")
        return
    play_hand()


root = tk.Tk()

button = tk.Button(root, 
                   text="New Game", 
                   command=new_game)
button.pack(pady=100) 

root.mainloop()
