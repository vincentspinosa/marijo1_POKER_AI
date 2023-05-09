from gameState import GameState
from player import Player

#n_players = int(input("Number of players: "))
n_players = 2
players = ()
for i in range(n_players):
    #players += (Player(chips=int(input(f"Player {i} chips: "))), )
    players += (Player(chips=1000), )
#sm_bld = int(input("Small blind: "))
#bg_bld = int(input("Blig blind: "))
game_state = GameState(players, 0, small_blind=10, big_blind=20)
game_state.play_preflop()
if len(game_state.active_players) > 1 and len(game_state.all_in_players) + 1 < len(game_state.active_players):
    game_state.play_flop()
if len(game_state.active_players) > 1 and len(game_state.all_in_players) + 1 < len(game_state.active_players):
    game_state.play_turn()
if len(game_state.active_players) > 1 and len(game_state.all_in_players) + 1 < len(game_state.active_players):
    game_state.play_river()
print("Hand done.\n")
