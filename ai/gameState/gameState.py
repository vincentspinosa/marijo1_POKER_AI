from treys import Evaluator
from ..rules.deck import Deck
from ..rules.player import Player


class GameState:
    def __init__(self, players:tuple[Player], ai_player_index:int, dealer_position:int=0, small_blind:int=10, big_blind:int=20, current_pot:int=0, current_stage:str='pre-flop'):
        self.players:tuple = players
        self.ai_player:Player = players[ai_player_index]
        self.active_players:tuple = players
        self.dealer_position:int = dealer_position
        self.small_blind:int = small_blind
        self.big_blind:int = big_blind
        self.deck:Deck = Deck()
        self.ai_deck:list = []
        self.community_cards:list = []
        self.current_pot:int = current_pot
        self.current_bets:dict = {player: 0 for player in players}
        self.current_stage:str = current_stage
        self.all_in_players:list = []
        self.hand_evaluator:Evaluator = Evaluator()
        self.current_player:Player = self.players[(self.dealer_position + 1) % len(players)]
        self.round_turns:int = 0
        self.round_players:tuple = self.active_players
        self.lastActionIsCheck:bool = False
        self.dontHaveToAnswer = False

    """
        Methods of the GameState class:

            - get_player_position(self, player:Player) -> int
            - calculate_raise_buckets(self, player:Player, min_raise:int) -> list
            - available_actions(self) -> list
            - showdown(self, players:tuple[Player]) -> Player or None
    """

    def get_player_position(self, player:Player) -> int:
        return self.players.index(player)

    def calculate_raise_buckets(self, player:Player, min_raise:int, current_bet:int) -> list:
        x = max(min_raise, current_bet * 2)
        buckets = []
        while x <= player.chips / 2:
            buckets.append(x)
            x *= 2
        return buckets

    def available_actions(self) -> list:
        actions = []
        if self.current_player not in self.active_players:
            return actions
        actions.append(('fold', 0))
        current_bet = max(self.current_bets.values())
        player_bet = self.current_bets[self.current_player]
        if self.current_player.chips + player_bet > current_bet:
            if player_bet < current_bet:
                if self.current_player.chips > current_bet - player_bet:
                    actions.append(('call', current_bet - player_bet))
            else:
                actions.append(('check', 0))
                actions.pop(0)
        if len(self.all_in_players) + 1 < len(self.active_players):
            if self.current_player.chips + player_bet >= current_bet + self.big_blind:
                min_raise = current_bet - player_bet + self.big_blind
                max_raise = self.current_player.chips
                if min_raise < max_raise:
                    raise_buckets = self.calculate_raise_buckets(self.current_player, min_raise, current_bet)
                    for raise_amount in raise_buckets:
                        actions.append(('raise', raise_amount))
        actions.append(('all-in', self.current_player.chips))
        return actions

    def showdown(self, players:tuple[Player]) -> Player | None:
        x = self.hand_evaluator.evaluate(players[0].hand, self.community_cards)
        y = self.hand_evaluator.evaluate(players[1].hand, self.community_cards)
        if x < y:
            return players[0]
        if y < x:
            return players[1]
        return None
