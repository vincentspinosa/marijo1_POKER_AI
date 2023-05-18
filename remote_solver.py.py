from ui import ui
from rules import player

while True:
    sm_blind = int(input("Small blind: "))
    p0_chips = int(input("Player 0 chips: "))
    p1_chips = int(input("Player 1 chips: "))
    players = (player.Player(chips=p0_chips), player.Player(chips=p1_chips))
    ai_index = int(input("AI position (Big blind: 0, Small blind: 1): "))
    game_ui = ui.UI(players, ai_index, small_blind=sm_blind, big_blind=(sm_blind * 2))
    game_ui.play_preflop()
    if len(game_ui.active_players) > 1 and len(game_ui.all_in_players) + 1 < len(game_ui.active_players):
        game_ui.play_flop()
    if len(game_ui.active_players) > 1 and len(game_ui.all_in_players) + 1 < len(game_ui.active_players):
        game_ui.play_turn()
    if len(game_ui.active_players) > 1 and len(game_ui.all_in_players) + 1 < len(game_ui.active_players):
        game_ui.play_river()
    print("Hand done.\n")
