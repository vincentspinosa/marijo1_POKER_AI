from gameState import GameState
from player import Player

n_players = int(input("Number of players: "))
players = ()
for i in range(n_players):
    players += (Player(chips=int(input(f"Player {i} chips: "))), )
sm_bld = int(input("Small blind: "))
bg_bld = int(input("Blig blind: "))
game_state = GameState(players, 0, small_blind=sm_bld, big_blind=bg_bld)
game_state.play_preflop()
if len(game_state.active_players) > 1:
    game_state.play_flop()
if len(game_state.active_players) > 1:
    game_state.play_turn()
if len(game_state.active_players) > 1:
    game_state.play_river()
print("Hand done.\n")
