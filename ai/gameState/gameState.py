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
            - get_next_player(self, player:Player) -> Player
            - next_player(self) -> None
            - eliminate_player(self, player:Player) -> None
            - calculate_raise_buckets(self, player:Player, min_raise:int) -> list
            - available_actions(self) -> list
            - handle_action(self, action:str, raise_amount:int=0) -> None
            - showdown(self, players:tuple[Player]) -> Player or None
    """

    def get_player_position(self, player:Player) -> int:
        return self.players.index(player)

    def get_next_player(self, player:Player) -> Player:
        position = self.get_player_position(player)
        next_position = (position + 1) % len(self.players)
        return self.players[next_position]

    def next_player(self) -> None:
        self.current_player = self.get_next_player(self.current_player)

    def eliminate_player(self, player:Player) -> None:
        self.active_players = self.active_players[:self.get_player_position(player)] + self.active_players[(self.get_player_position(player) + 1):]

    def calculate_raise_buckets(self, player:Player, min_raise:int) -> list:
        return [min_raise, min_raise + int((player.chips - min_raise) / 16), min_raise + int((player.chips - min_raise) / 8), min_raise + int((player.chips - min_raise) / 4), min_raise + int((player.chips - min_raise) / 2)]

    def available_actions(self) -> list:
        actions = []
        actions.append(('fold', 0))
        if self.current_player not in self.active_players:
            return actions
        current_bet = max(self.current_bets.values())
        player_bet = self.current_bets[self.current_player]
        if self.current_player.chips + player_bet > current_bet:
            if player_bet < current_bet and self.current_player.chips > current_bet - player_bet:
                actions.append(('call', current_bet - player_bet))
            else:
                actions.append(('check', 0))
                actions.pop(0)
        if len(self.all_in_players) + 1 < len(self.active_players):
            if self.current_player.chips + player_bet >= current_bet + self.big_blind:
                min_raise = current_bet - player_bet + self.big_blind
                max_raise = self.current_player.chips
                if min_raise < max_raise:
                    raise_buckets = self.calculate_raise_buckets(self.current_player, min_raise)
                    for raise_amount in raise_buckets:
                        actions.append(('raise', raise_amount))
                else:
                    actions.append(('raise', min_raise))
        actions.append(('all-in', self.current_player.chips))
        return actions

    def handle_action(self, action:str, raise_amount:int=0) -> None:
        print(f"\nHANDLING THE ACTION {str(action).upper()}\n")
        if action == 'check':
            self.current_bets[self.current_player] = 0
            self.lastActionIsCheck = True
        elif action == 'call':
            call_amount = max(self.current_bets.values()) - self.current_bets[self.current_player]
            print(f"\nCall amount: {call_amount}\n")
            self.current_player.bet(call_amount)
            self.current_pot += call_amount
            self.current_bets[self.current_player] = 0
            self.current_bets[self.get_next_player(self.current_player)] = 0
            self.lastActionIsCheck = False
        elif action == 'raise':
            if raise_amount >= self.current_player.chips:
                self.handle_action('all-in', raise_amount=raise_amount)
            else:
                self.current_player.bet(raise_amount)
                self.current_pot += raise_amount
                self.current_bets[self.current_player] += raise_amount
                self.lastActionIsCheck = False
        elif action == 'all-in':
            opp = self.get_next_player(self.current_player)
            bet_adversary = self.current_bets[self.get_next_player(self.current_player)]
            bet_amount = self.current_player.chips
            if bet_amount <= bet_adversary:
                self.dontHaveToAnswer = True
            bet_total = bet_amount + self.current_bets[self.current_player]
            if bet_total <= bet_adversary:
                bet_diff = bet_adversary - bet_total
                self.current_pot -= bet_diff
                self.get_next_player(self.current_player).chips += bet_diff
            elif opp.chips + bet_adversary < bet_amount:
                bet_amount -= (bet_amount - opp.chips - bet_adversary)
            self.current_player.bet(bet_amount)
            self.current_pot += bet_amount
            self.current_bets[self.current_player] += bet_amount
            self.all_in_players.append(self.current_player)
            self.lastActionIsCheck = False
        elif action == 'fold':
            self.eliminate_player(self.current_player)
            self.lastActionIsCheck = False
            print(f"Folded. Number of active players: {len(self.active_players)}")
        self.round_turns += 1

    def showdown(self, players:tuple[Player]) -> Player or None:
        x = self.hand_evaluator.evaluate(players[0].hand, self.community_cards)
        y = self.hand_evaluator.evaluate(players[1].hand, self.community_cards)
        if x < y:
            return players[0]
        if y < x:
            return players[1]
        return None
