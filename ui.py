from gameState import GameState
from player import Player

sm_bld = int(input("Small blind: "))
bg_bld = int(input("Blig blind: "))
while True:
    n_players = 2
    players = ()
    target_player_chips = int(input("Target player chips: "))
    target_player_index = int(input("Target player index: "))
    if target_player_index == 0:
        players += (Player(chips=target_player_chips), )
        players += (Player(chips=int(input("Opposite player chips: "))), )
    else:
        players += (Player(chips=int(input("Opposite player chips: "))), )
        players += (Player(chips=target_player_chips), )
    game_state = GameState(players, target_player_index, small_blind=sm_bld, big_blind=bg_bld)
    game_state.play_preflop()
    if len(game_state.active_players) > 1 and len(game_state.all_in_players) + 1 < len(game_state.active_players):
        game_state.play_flop()
    if len(game_state.active_players) > 1 and len(game_state.all_in_players) + 1 < len(game_state.active_players):
        game_state.play_turn()
    if len(game_state.active_players) > 1 and len(game_state.all_in_players) + 1 < len(game_state.active_players):
        game_state.play_river()
    print("Hand done.\n")
