from ui import ui
from rules import player

sm_blind = int(input("Small blind: "))
bg_blind = int(input("Big blind: "))
p0_chips = int(input("Player 0 chips: "))
p1_chips = int(input("Player 1 chips: "))
players = (player.Player(chips=p0_chips), player.Player(chips=p1_chips))
ai_index = int(input("AI position (Starting as Dealer: 0, Starting as Small Blind: 1): "))
game_ui = ui.UI(players, ai_index, small_blind=sm_blind, big_blind=bg_blind)

while not game_ui.is_game_over():
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
    winner = int(input(f"Winner (0 for P0, 1 for P1): "))
    game_ui.end_round(winner)
    game_ui.move_dealer_button()

print(f"\nGame is over! Winner is player {winner}.")
print(f"\nChips of player {winner}: {game_ui.players[winner].chips}\n")
