from ui import ui
from rules import player

sm_blind = int(input("Small blind: "))
bg_blind = int(input("Big blind: "))
p0_chips = int(input("Player 0 chips: "))
p1_chips = int(input("Player 1 chips: "))
players = (player.Player(chips=p0_chips), player.Player(chips=p1_chips))
ai_index = int(input("AI position (Dealer/Big blind: 0, Small blind: 1): "))
game_ui = ui.UI(players, ai_index, small_blind=sm_blind, big_blind=bg_blind)

while not game_ui.is_game_over:
    game_ui.play_preflop()
    if not game_ui.is_hand_over():
        game_ui.play_flop()
    if not game_ui.is_hand_over():
        game_ui.play_turn()
    if not game_ui.is_hand_over():
        game_ui.play_river()
    print("Hand done.\n")
