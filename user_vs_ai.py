from rules import player
from ui.ui import UI
from rules import player
from helper_functions import helpers

sm_blind = helpers.force_int_input("Small blind: ")
players_chips = helpers.force_int_input("Players chips: ")
players = (player.Player(chips=players_chips), player.Player(chips=players_chips))
first_dealer = helpers.force_int_input("First dealer position (AI: 0, Opposite player: 1): ")
game_ui = UI(players, target_player_index=0, dealer_position=first_dealer, small_blind=sm_blind, big_blind=(sm_blind * 2))

while not game_ui.is_game_over():
    game_ui = game_ui.new_hand()
    game_ui.round('pre-flop')
    if not game_ui.is_hand_over():
        game_ui.round('flop')
    if not game_ui.is_hand_over():
        game_ui.round('turn')
    if not game_ui.is_hand_over():
        game_ui.round('river')
    if len(game_ui.active_players) > 1:
        winner = game_ui.showdown(game_ui.players)
    else:
        winner = game_ui.active_players[0]
    game_ui.end_round(winner)
    game_ui.move_dealer_button()

print(f"\nGame is over! Winner is player {winner}.")
print(f"\Chips of player {winner}: {game_ui.players[winner].chips}")