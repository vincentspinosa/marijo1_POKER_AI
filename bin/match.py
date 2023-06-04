from ui import UI
from eval import evalAgent
from ai import ai
from helper_functions import helpers

class Match(UI):
    def __init__(self, players, target_player_index, dealer_position=0, small_blind=10, big_blind=20, current_pot=0, current_stage='pre-flop'):
        super().__init__(players, target_player_index, dealer_position, small_blind, big_blind, current_pot, current_stage)

