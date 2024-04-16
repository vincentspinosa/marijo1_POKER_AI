import time
import random
from ui import UI, new_hand
from ai.rules.player import Player
from helper_functions.helpers import force_int_input

default = True
playersDict = {0: "Marijo1 (Base)", 1: "Experimental"}
# if print_ai_crds is True, Marijo1's hand will be printed in the terminal
print_ai_crds = True

if default == False:
    iterations = force_int_input("Number of iterations: ")
    ai_verbose_lvl = force_int_input("\nAI verbose level: ")
    sm_blind = force_int_input("\nSmall blind: ")
    players_chips = force_int_input("Players chips (both players will start wih the amount entered): ")
else:
    iterations = 5000
    ai_verbose_lvl = 2
    sm_blind = 10
    players_chips = 1000

players = (Player(chips=players_chips), Player(chips=players_chips))
first_dealer = random.randint(0, 1)
game_ui = UI(ai_iterations=iterations, players=players, ai_player_index=0, ai_verbose=ai_verbose_lvl, dealer_position=first_dealer, small_blind=sm_blind, big_blind=(sm_blind * 2))

print("\nLet's begin!")
time.sleep(1)

while game_ui.is_game_over() == False:
    print("\nStarting a new hand!")
    game_ui = new_hand(game_ui)
    game_ui.round_2AI(stage='pre-flop', print_ai_cards=print_ai_crds)
    game_ui.set_if_hand_over()
    if game_ui.hand_is_over == False:
        game_ui.round_2AI(stage='flop', print_ai_cards=print_ai_crds)
        game_ui.set_if_hand_over()
    if game_ui.hand_is_over == False:
        game_ui.round_2AI(stage='turn', print_ai_cards=print_ai_crds)
        game_ui.set_if_hand_over()
    if game_ui.hand_is_over == False:
        game_ui.round_2AI(stage='river', print_ai_cards=print_ai_crds)
    winner = None
    if len(game_ui.active_players) > 1 and game_ui.lastActionIsCheck == False:
        print("Going to showdown!".upper())
        len_cc = len(game_ui.community_cards)
        if len_cc < 5:
            game_ui.community_cards += [game_ui.deck.deal() for _ in range(5 - len_cc)]
        game_ui.print_showdown_info()
        winner = game_ui.showdown(game_ui.players)
    else:
        print("Not going to showdown!".upper())
        if len(game_ui.active_players) > 1:
            winner = None
        else:
            winner = game_ui.active_players[0]
    if winner is not None:
        winnerIndex = game_ui.get_player_position(winner)
        print(f"\nHand is over! {playersDict[winnerIndex]} won the hand.".upper())
    else:
        winnerIndex = None
        if len(game_ui.active_players) > 1 and game_ui.lastActionIsCheck == False:
            print("\nHands are equal!")
        print("\nThe pot is split between both players.")
    game_ui.end_hand(winnerIndex)
    game_ui.move_dealer_button()

print(f"\nGame is over! The winner is {playersDict[winnerIndex]}.".upper())
print(f"\nChips of {playersDict[winnerIndex]}: {game_ui.players[winnerIndex].chips}".upper())
print("\n")
