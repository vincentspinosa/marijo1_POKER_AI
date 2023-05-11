from gameState import GameState
from player import Player

n_players = 2
sm_bld = int(input("Small blind: "))
bg_bld = int(input("Blig blind: "))
players = ()
for i in range(n_players):
    players += (Player(chips=int(input(f"Player {i} chips: "))), )
target_player_index = int(input("Target player index: "))
game_state = GameState(players, target_player_index, small_blind=sm_bld, big_blind=bg_bld)
game_state.play_preflop()
if len(game_state.active_players) > 1 and len(game_state.all_in_players) + 1 < len(game_state.active_players):
    game_state.play_flop()
if len(game_state.active_players) > 1 and len(game_state.all_in_players) + 1 < len(game_state.active_players):
    game_state.play_turn()
if len(game_state.active_players) > 1 and len(game_state.all_in_players) + 1 < len(game_state.active_players):
    game_state.play_river()
print("Hand done.\n")
