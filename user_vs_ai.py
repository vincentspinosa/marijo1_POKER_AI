from ui import ui
from rules import player

sm_blind = int(input("Small blind: "))
starting_chips = int(input("Starting chips chips: "))
players = (player.Player(chips=starting_chips), player.Player(chips=starting_chips))
ai_index = int(input("AI starting position (Big blind: 0, Small blind: 1): "))
while True:
    game_ui = ui.UI(players, ai_index, small_blind=sm_blind, big_blind=(sm_blind * 2))
    game_ui.play_preflop()
    if len(game_ui.active_players) > 1 and len(game_ui.all_in_players) + 1 < len(game_ui.active_players):
        game_ui.play_flop()
    if len(game_ui.active_players) > 1 and len(game_ui.all_in_players) + 1 < len(game_ui.active_players):
        game_ui.play_turn()
    if len(game_ui.active_players) > 1 and len(game_ui.all_in_players) + 1 < len(game_ui.active_players):
        game_ui.play_river()
    print("Hand done.\n")
