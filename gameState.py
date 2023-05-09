from hand_evaluator import HandEvaluator
from deck import Deck

class GameState:
    def __init__(self, players, target_player_index, dealer_position=0, small_blind=10, big_blind=20, current_pot=0, current_stage='pre-flop'):
        self.players = players
        self.target_player = players[target_player_index]
        self.active_players = tuple(players)
        self.dealer_position = dealer_position
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.deck = Deck()
        self.community_cards = []
        self.current_pot = current_pot
        self.current_bets = {player: 0 for player in players}
        self.current_stage = current_stage
        self.all_in_players = []
        self.hand_evaluator = HandEvaluator()
        self.current_player = self.players[(self.dealer_position + 1) % len(players)]
        self.round_turns = 0
        self.round_players = self.active_players

    def determine_hole_cards(self):
        for x in range(2):
            index = -1
            for i in self.deck.cards:
                index += 1
                print(f"{index} - {i}")
            y = int(input(f"\nCard {x}: "))
            self.target_player.hand.append(self.deck.cards[y])
            self.deck.cards.pop(y)

    def deal_community_cards(self):
        self.deck.shuffle()
        if self.current_stage == 'flop':
            self.community_cards = [self.deck.deal() for _ in range(3)]
        elif self.current_stage in ['turn', 'river']:
            self.community_cards.append(self.deck.deal())

    def determine_community_cards(self):
        if self.current_stage == 'flop':
            nb_cards = 3
        elif self.current_stage in ['turn', 'river']:
            nb_cards = 1
        for x in range(nb_cards):
            index = -1
            for i in self.deck.cards:
                index += 1
                print(f"{index} - {i}")
            y = int(input(f"\nCard {x}: "))
            self.community_cards.append(self.deck.cards[y])
            self.deck.cards.pop(y)


    def eliminate_player(self, player):
        self.active_players = self.active_players[:self.get_player_position(player)] + self.active_players[(self.get_player_position(player) + 1):]

    def available_actions(self):
        actions = []

        if self.current_player not in self.active_players:
            return actions

        current_bet = max(self.current_bets.values())
        player_bet = self.current_bets[self.current_player]

        if self.current_player.chips + player_bet >= current_bet:
            if player_bet < current_bet:
                actions.append(('call', None))
            else:
                actions.append(('check', None))

        if len(self.all_in_players) + 1 < len(self.active_players):
            if self.current_player.chips + player_bet >= current_bet + self.big_blind:
                min_raise = current_bet - player_bet + self.big_blind
                max_raise = self.current_player.chips

                if min_raise < max_raise:
                    raise_buckets = self.calculate_raise_buckets(self.current_player, min_raise, max_raise)
                    for raise_amount in raise_buckets:
                        actions.append(('raise', raise_amount))
                else:
                    actions.append(('raise', min_raise))

        actions.append(('all-in', None))
        actions.append(('fold', None))
        return actions

    def calculate_raise_buckets(self, player, min_raise, max_raise):
        raise_buckets = [min_raise]
        current_raise = min_raise
        while current_raise < max_raise:
            next_raise = int(current_raise + (0.33 * player.chips))
            if next_raise > max_raise:
                break
            raise_buckets.append(next_raise)
            current_raise = next_raise
        return raise_buckets

    def get_player_position(self, player):
        return self.players.index(player)

    def get_next_player(self, player):
        position = self.get_player_position(player)
        next_position = (position + 1) % len(self.players)
        return self.players[next_position]

    def next_player(self):
        self.current_player = self.get_next_player(self.current_player)

    def showdown(self, players):
        # Calculate the hand ranks for each player
        player_hands = []
        for player in players:
            hand_rank, hand = self.hand_evaluator.evaluate_hand(player.hand, self.community_cards)
            player_hands.append((player, hand_rank, hand))

        # Sort the player hands by rank and the actual hand in descending order
        player_hands.sort(key=lambda x: (x[1], x[2]), reverse=True)

        # Find the highest rank and hands with the same highest rank
        highest_rank = player_hands[0][1]
        winning_hands = [player_hand for player_hand in player_hands if player_hand[1] == highest_rank]

        # If there's only one winning hand, return the corresponding player
        if len(winning_hands) == 1:
            return winning_hands[0][0]

        # If there are multiple winning hands, compare their high cards to determine the winner
        winning_player = winning_hands[0][0]
        winning_hand_high_card = winning_hands[0][2][0].rank
        for i in range(1, len(winning_hands)):
            current_hand_high_card = winning_hands[i][2][0].rank
            if current_hand_high_card > winning_hand_high_card:
                winning_player = winning_hands[i][0]
                winning_hand_high_card = current_hand_high_card

        return winning_player

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
            print(len(self.active_players))
        self.round_turns += 1

    def reset_round(self):
        self.current_player = self.players[(self.dealer_position + 1) % len(self.players)]
        self.round_turns = 0
        self.round_players = self.active_players

    def go_to_showdown(self):
        if len(self.all_in_players) == len(self.active_players):
            self.community_cards.append(self.deck.deal() for _ in range(5 - len(self.community_cards)))

    def is_round_over(self):
        if len(self.active_players) < 2:
            return True
        if self.round_turns >= len(self.round_players):
            active_bets = [bet for player, bet in self.current_bets.items() if player in self.active_players]
            print(f"\nActive bets: {active_bets}\n")
            if all(bet == 0 for bet in active_bets):
                return True
        if len(self.all_in_players) == len(self.active_players):
            return True   
        return False
    

    ###########################################################

            # UI functions

    ###########################################################

    def deal_hole_cards(self):
        self.deck.shuffle()
        self.target_player.hand = [self.deck.deal(), self.deck.deal()]

    """ def move_dealer_button(self):
        self.dealer_position = (self.dealer_position + 1) % len(self.players) """

    def player_action(self):
        actions = self.available_actions()
        print(f"\nPLAYER {self.get_player_position(self.current_player)}'s TURN\n")
        if self.current_player == self.target_player:
            print("\nCFR TIME!\n")
            print(f"\nCFR suggestion: {actions[0]}\n")
        index = -1
        for i in actions:
            index += 1
            print(f"{index} - {i}")
        return actions[int(input("\nChosen action: "))]

    def collect_blinds(self):
        small_blind_player = self.players[(self.dealer_position + 1) % len(self.players)]
        big_blind_player = self.players[(self.dealer_position + 2) % len(self.players)]
        small_blind_amount = min(small_blind_player.chips, self.small_blind)
        big_blind_amount = min(big_blind_player.chips, self.big_blind)

        small_blind_player.bet(small_blind_amount)
        big_blind_player.bet(big_blind_amount)
        self.current_bets[small_blind_player] = small_blind_amount
        self.current_bets[big_blind_player] = big_blind_amount
        self.current_pot += small_blind_amount + big_blind_amount

    def play_round(self):
        # player_action() returns the next action and the raise amount (if applicable)
        while not self.is_round_over() and len(self.all_in_players) < len(self.active_players):
            action = self.player_action()
            self.handle_action(action[0], raise_amount=action[1])
            self.next_player()
        self.reset_round()

    def play_preflop(self):
        print("\nPREFLOP\n")
        self.determine_hole_cards()
        self.collect_blinds()
        self.play_round()

    def play_flop(self):
        print("\nFLOP\n")
        self.current_stage = 'flop'
        self.determine_community_cards()
        self.play_round()

    def play_turn(self):
        print("\nTURN\n")
        self.current_stage = 'turn'
        self.determine_community_cards()
        self.play_round()

    def play_river(self):
        print("\nRIVER\n")
        self.current_stage = 'river'
        self.determine_community_cards()
        self.play_round()