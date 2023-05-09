from ..game_state import GameState
from ..rules_of_the_game import Deck

class GameStateAI(GameState):
    def __init__(self, players, dealer_position=0, small_blind=10, big_blind=20, current_pot=0, current_stage='pre-flop'):
        super().__init__(players, dealer_position, small_blind, big_blind, current_pot, current_stage)

    def deal_all_community_cards(self):
        deck = Deck()
        deck.shuffle()
        if self.current_stage == 'flop':
            self.community_cards = [deck.deal() for _ in range(3)]
        if self.current_stage == 'turn':
            self.community_cards = [deck.deal() for _ in range(4)]
        if self.current_stage == 'river':
            self.community_cards = [deck.deal() for _ in range(5)]