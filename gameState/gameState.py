from rules.hand_evaluator import HandEvaluator
from rules.deck import Deck
from rules.player import Player


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
        self.hand_evaluator:HandEvaluator = HandEvaluator()
        self.current_player:Player = self.players[(self.dealer_position + 1) % len(players)]
        self.round_turns:int = 0
        self.round_players:tuple = self.active_players

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
        return [min_raise, min_raise + int((player.chips - min_raise) / 4), min_raise + int((player.chips - min_raise) / 2)]

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
        elif action == 'call':
            call_amount = max(self.current_bets.values()) - self.current_bets[self.current_player]
            print(f"\nCall amount: {call_amount}\n")
            self.current_player.bet(call_amount)
            self.current_pot += call_amount
            self.current_bets[self.current_player] = 0
            self.current_bets[self.get_next_player(self.current_player)] = 0
        elif action == 'raise':
            raise_amount = min(raise_amount, self.current_player.chips)
            self.current_player.bet(raise_amount)
            self.current_pot += raise_amount
            self.current_bets[self.current_player] += raise_amount
        elif action == 'all-in':
            bet_adversary = self.current_bets[self.get_next_player(self.current_player)]
            bet_amount = self.current_player.chips
            if bet_amount < bet_adversary:
                bet_diff = bet_adversary - bet_amount
                self.current_pot -= bet_diff
                self.players[self.get_player_position(self.get_next_player(self.current_player))].chips += bet_diff
            self.current_player.bet(bet_amount)
            self.current_pot += bet_amount
            self.current_bets[self.current_player] += bet_amount
            self.all_in_players.append(self.current_player)
        elif action == 'fold':
            self.eliminate_player(self.current_player)
            print(f"Folded. Number of active players: {len(self.active_players)}")
        self.round_turns += 1

    def showdown(self, players:tuple[Player]) -> Player or None:
        player_hands = []
        for player in players:
            hand_rank, hand = self.hand_evaluator.evaluate_hand(list(player.hand), list(self.community_cards))
            player_hands.append({"player": player, "hand_rank": hand_rank, "hand": hand})
        player_hands.sort(key=lambda x: (x["hand_rank"], [card.rank for card in x["hand"]]), reverse=True)
        highest_rank = player_hands[0]["hand_rank"]
        winning_hands = [p for p in player_hands if p["hand_rank"] == highest_rank]
        if len(winning_hands) == 1:
            return winning_hands[0]["player"]
        # If there are multiple winning hands, compare their high cards to determine the winner
        winning_player = winning_hands[0]["player"]
        winning_hand_high_card = winning_hands[0]["hand"][0].rank
        winners = 1
        for i in range(1, len(winning_hands)):
            current_hand_high_card = winning_hands[i]["hand"][0].rank
            if current_hand_high_card > winning_hand_high_card:
                winning_player = winning_hands[i]["player"]
                winning_hand_high_card = current_hand_high_card
                winners = 1
            elif current_hand_high_card == winning_hand_high_card:
                winners = 2
        if winners < 2:
            return winning_player  
        return None
