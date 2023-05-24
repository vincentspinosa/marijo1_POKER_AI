from ui.ui import UI, new_hand
from rules.player import Player
from helper_functions.helpers import force_int_input

sm_blind = force_int_input("Small blind: ")
players_chips = force_int_input("Players chips: ")
players = (Player(chips=players_chips), Player(chips=players_chips))
first_dealer = force_int_input("First dealer position (AI: 0, Opposite player: 1): ")
game_ui = UI(players, ai_player_index=0, dealer_position=first_dealer, small_blind=sm_blind, big_blind=(sm_blind * 2))

print("\nLet's begin!")
print(f"\nAI is Player 0")
print(f"You are Player 1")
print("\n")

while game_ui.is_game_over() == False:
    game_ui = new_hand(game_ui)
    game_ui.round(stage='pre-flop')
    game_ui.set_if_hand_over()
    if game_ui.handOver == False:
        game_ui.round(stage='flop')
        game_ui.set_if_hand_over()
    if game_ui.handOver == False:
        game_ui.round(stage='turn')
        game_ui.set_if_hand_over()
    if game_ui.handOver == False:
        game_ui.round(stage='river')
    winner = None
    if len(game_ui.active_players) > 1:
        len_cc = len(game_ui.community_cards)
        if len_cc < 5:
            game_ui.community_cards += [game_ui.deck.deal() for _ in range(5 - len_cc)]
        winner = game_ui.showdown(game_ui.players)
    else:
        winner = game_ui.active_players[0]
    if winner is not None:
        winner = game_ui.get_player_position(winner)
    print(f"\nWinner is Player {winner}".upper())
    game_ui.end_hand(winner)
    game_ui.move_dealer_button()

winnerDict = {0: "Marijo1 (Player 0)", 1: "You (Player 1)"}
print(f"\nGame is over! Winner is player {winnerDict[winner]}.")
print(f"\nChips of player {winner}: {game_ui.players[winner].chips}")
print("\n")