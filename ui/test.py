import time
from ui import UI, new_hand
from ai.rules.player import Player
from helper_functions.helpers import force_int_input

# The goal of this script is to test the level of the AI
# Here, only hands are played, not full games
# For each hand, both the AI and the Player have 1000 chips
# The small blind is 10, the big blind 20, there is no ante

numberOfHandsPlayed = 0
Marijo1Return = 0

playersDict = {0: "Marijo1 (Player 0)", 1: "You (Player 1)"}
# if print_ai_crds is True, Marijo1's hand will be printed in the terminal
print_ai_crds = True

iterations = 30000
ai_verbose_lvl = 2
sm_blind = 10
players_chips = 1000

players = (Player(chips=players_chips), Player(chips=players_chips))
print("\nFor this test, Marijo1 is indexed as Player 0, and you are indexed as Player 1.")
first_dealer = force_int_input("First dealer of the test (Marijo1: 0, You: 1): ")
game_ui = UI(ai_iterations=iterations, players=players, ai_player_index=0, ai_verbose=ai_verbose_lvl, dealer_position=first_dealer, small_blind=sm_blind, big_blind=(sm_blind * 2))

print("\nLet's begin!")
time.sleep(1)

play = True
while play == True:
    # SPECIFIC TO TEST.PY
    print(f"\nHand n°{numberOfHandsPlayed + 1}")
    print(f"Current return of Marijo1: {Marijo1Return}")
    # SAME AS USER_VS_AI.PY
    print("\nStarting a new hand!")
    game_ui = new_hand(game_ui)
    game_ui.players[0].chips = players_chips
    game_ui.players[1].chips = players_chips
    time.sleep(1)
    game_ui.round(stage='pre-flop', print_ai_cards=print_ai_crds)
    time.sleep(1)
    game_ui.set_if_hand_over()
    if game_ui.hand_is_over == False:
        game_ui.round(stage='flop', print_ai_cards=print_ai_crds)
        game_ui.set_if_hand_over()
        time.sleep(1)
    if game_ui.hand_is_over == False:
        game_ui.round(stage='turn', print_ai_cards=print_ai_crds)
        game_ui.set_if_hand_over()
        time.sleep(1)
    if game_ui.hand_is_over == False:
        game_ui.round(stage='river', print_ai_cards=print_ai_crds)
        time.sleep(1)
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
    time.sleep(1)
    game_ui.end_hand(winnerIndex)
    game_ui.move_dealer_button()
    # SPECIFIC TO TEST.PY
    numberOfHandsPlayed += 1
    Marijo1Return += game_ui.ai_player.chips - 1000
    if force_int_input(f"\nPlay again ? 0 = Yes ; 1 = No : ") == 1:
        play = False

print(f"\nTest over !")
print(f"\nMarijo1 had a return of {Marijo1Return} in {numberOfHandsPlayed} hands.")
print("\n")