from ui import ui
from rules import player
from helper_functions import helpers

sm_blind = helpers.force_int_input("Small blind: ")
bg_blind = helpers.force_int_input("Big blind: ")
ai_index = helpers.force_int_input("AI position (Starting as Dealer: 0, Starting as Small Blind: 1): ")
p0_chips = helpers.force_int_input("Player 0 chips: ")
p1_chips = helpers.force_int_input("Player 1 chips: ")
players = (player.Player(chips=p0_chips), player.Player(chips=p1_chips))
game_ui = ui.UI(players, ai_index, small_blind=sm_blind, big_blind=bg_blind)

while not game_ui.is_game_over():
    game_ui = game_ui.new_hand()
    print("\nNew hand!")
    x = 0
    for p in game_ui.players:
        print(f"\nChips of player {x}: {p.chips}")
        x += 1
    game_ui.play_preflop()
    if not game_ui.is_hand_over():
        game_ui.play_flop()
    if not game_ui.is_hand_over():
        game_ui.play_turn()
    if not game_ui.is_hand_over():
        game_ui.play_river()
    print("Hand done.\n")
    winner = helpers.force_int_input(f"Winner (0 for P0, 1 for P1): ")
    game_ui.end_round(winner)
    game_ui.move_dealer_button()

print(f"\nGame is over! Winner is player {winner}.")
print(f"\nChips of player {winner}: {game_ui.players[winner].chips}\n")
