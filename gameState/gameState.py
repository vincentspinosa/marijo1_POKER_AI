from rules import hand_evaluator
from rules import deck

class GameState:
    def __init__(self, players, target_player_index, dealer_position=0, small_blind=10, big_blind=20, current_pot=0, current_stage='pre-flop'):
        self.players = players
        self.target_player = players[target_player_index]
        self.active_players = tuple(players)
        self.dealer_position = dealer_position
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.deck = deck.Deck()
        self.community_cards = []
        self.current_pot = current_pot
        self.current_bets = {player: 0 for player in players}
        self.current_stage = current_stage
        self.all_in_players = []
        self.hand_evaluator = hand_evaluator.HandEvaluator()
        self.current_player = self.players[(self.dealer_position + 1) % len(players)]
        self.round_turns = 0
        self.round_players = self.active_players

    def get_player_position(self, player):
        return self.players.index(player)

    def calculate_raise_buckets(self, player, min_raise):
        return [min_raise, min_raise + int((player.chips - min_raise) / 4), min_raise + int((player.chips - min_raise) / 2)]

    def available_actions(self):
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

    def handle_action(self, action, raise_amount=0):
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
            self.current_bets[self.current_player] = bet_amount
            self.all_in_players.append(self.current_player)
        elif action == 'fold':
            self.players[self.get_player_position(self.get_next_player(self.current_player))].chips += self.current_pot
            self.eliminate_player(self.current_player)
            print(f"Folded. Number of active players: {len(self.active_players)}")
        self.round_turns += 1

    def go_to_showdown(self):
        self.community_cards += [self.deck.deal() for _ in range(5 - len(self.community_cards))]

    def showdown(self, players):
        # Calculate the hand ranks for each player
        player_hands = []
        for player in players:
            hand_rank, hand = self.hand_evaluator.evaluate_hand(list(player.hand), list(self.community_cards))
            player_hands.append((player, hand_rank, hand))
        # Sort the player hands by rank and the actual hand in descending order
        player_hands.sort(key=lambda x: (x[1], [card.rank for card in x[2]]), reverse=True)
        # Find the highest rank and hands with the same highest rank
        highest_rank = player_hands[0][1]
        winning_hands = [player_hand for player_hand in player_hands if player_hand[1] == highest_rank]
        # If there's only one winning hand, return the corresponding player
        if len(winning_hands) == 1:
            return winning_hands[0][0]
        # If there are multiple winning hands, compare their high cards to determine the winner
        winning_player = winning_hands[0][0]
        winning_hand_high_card = winning_hands[0][2][0].rank
        winners = 1
        for i in range(1, len(winning_hands)):
            current_hand_high_card = winning_hands[i][2][0].rank
            if current_hand_high_card > winning_hand_high_card:
                winning_player = winning_hands[i][0]
                winning_hand_high_card = current_hand_high_card
                winners = 1
            elif current_hand_high_card == winning_hand_high_card:
                winners = 2
        if winners < 2:
            return winning_player  
        return None
