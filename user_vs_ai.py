import time
from ui.ui import UI, new_hand
from rules.player import Player
from helper_functions.helpers import force_int_input

playersDict = {0: "Marijo1 (Player 0)", 1: "You (Player 1)"}
# if print_ai_crds is True, Marijo1's hand will be printed in the terminal
print_ai_crds = False

sm_blind = force_int_input("\nSmall blind: ")
players_chips = force_int_input("Players chips (both players will start wih the amount entered): ")
players = (Player(chips=players_chips), Player(chips=players_chips))
print("\nIn this game, Marijo1 is indexed as Player 0, and you are indexed as Player 1.")
first_dealer = force_int_input("First dealer of the game (Marijo1: 0, You: 1): ")
game_ui = UI(players, ai_player_index=0, dealer_position=first_dealer, small_blind=sm_blind, big_blind=(sm_blind * 2))

print("\nLet's begin!")

time.sleep(1)

while game_ui.is_game_over() == False:
    print("\nStarting a new hand!")
    game_ui = new_hand(game_ui)
    time.sleep(1)
    game_ui.round(stage='pre-flop', print_ai_cards=print_ai_crds)
    time.sleep(1)
    game_ui.set_if_hand_over()
    if game_ui.handOver == False:
        game_ui.round(stage='flop', print_ai_cards=print_ai_crds)
        game_ui.set_if_hand_over()
        time.sleep(1)
    if game_ui.handOver == False:
        game_ui.round(stage='turn', print_ai_cards=print_ai_crds)
        game_ui.set_if_hand_over()
        time.sleep(1)
    if game_ui.handOver == False:
        game_ui.round(stage='river', print_ai_cards=print_ai_crds)
        time.sleep(1)
    winner = None
    if len(game_ui.active_players) > 1:
        print("Going to showdown!".upper())
        len_cc = len(game_ui.community_cards)
        if len_cc < 5:
            game_ui.community_cards += [game_ui.deck.deal() for _ in range(5 - len_cc)]
        game_ui.print_showdown_info()
        winner = game_ui.showdown(game_ui.players)
    else:
        print("Not going to showdown!".upper())
        winner = game_ui.active_players[0]
    if winner is not None:
        winner = game_ui.get_player_position(winner)
        print(f"\nHand is over! {playersDict[winner]} won the hand.".upper())
    else:
        print("\nHands are equal! The pot is split between both players.")
    time.sleep(1)
    game_ui.end_hand(winner)
    game_ui.move_dealer_button()

print(f"\nGame is over! The winner is {playersDict[winner]}.".upper())
print(f"\nChips of {playersDict[winner]}: {game_ui.players[winner].chips}".upper())
print("\n")
