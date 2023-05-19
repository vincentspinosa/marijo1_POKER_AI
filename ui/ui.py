from gameState import gameState
from eval import evalAgent
from helper_functions import helpers

class UI(gameState.GameState):
    def __init__(self, players, target_player_index, dealer_position=0, small_blind=10, big_blind=20, current_pot=0, current_stage='pre-flop'):
        super().__init__(players, target_player_index, dealer_position, small_blind, big_blind, current_pot, current_stage)

    def is_game_over(self):
        if self.players[0].chips == 0 or self.players[1].chips == 0:
            return True
        return False

    def is_hand_over(self):
        if len(self.active_players) > 1 and len(self.all_in_players) + 1 < len(self.active_players):
            return False
        return True

    def is_round_over(self):
        if len(self.active_players) < 2:
            return True
        if self.round_turns >= len(self.round_players) or self.current_stage == 'pre-flop':
            active_bets = [bet for player, bet in self.current_bets.items() if player in self.active_players]
            print(f"\nActive bets: {active_bets}\n")
            if len(set(active_bets)) == 1:
                return True
        if len(self.all_in_players) == len(self.active_players):
            return True   
        return False

    def reset_round(self):
        self.current_player = self.players[(self.dealer_position + 1) % len(self.players)]
        self.round_turns = 0
        self.round_players = self.active_players

    def end_round(self, winner):
        reward = self.current_pot
        self.players[winner].chips += reward
        self.current_pot = 0

    def eliminate_player(self, player):
        self.active_players = self.active_players[:self.get_player_position(player)] + self.active_players[(self.get_player_position(player) + 1):]

    def move_dealer_button(self):
        self.dealer_position = (self.dealer_position + 1) % len(self.players)

    def get_next_player(self, player):
        position = self.get_player_position(player)
        next_position = (position + 1) % len(self.players)
        return self.players[next_position]

    def next_player(self):
        self.current_player = self.get_next_player(self.current_player)
    
    def get_action(self, actions):
        index = -1
        for i in actions:
            index += 1
            print(f"{index} - {i}")
        return actions[helpers.force_int_input("\nChosen action: ")]

    def player_action(self):
        actions = self.available_actions()
        print(f"\nPLAYER {self.get_player_position(self.current_player)}'s TURN\n")
        print("\nCFR TIME!\n")
        print(f"\nCFR suggestion: {evalAgent.eval(self, 3)}\n")
        return self.get_action(actions)
    
    def available_opposite_player_actions(self):
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
                actions.append(('raise', 0))
        actions.append(('all-in', self.current_player.chips))
        return actions
    
    def opposite_player_action(self):
        actions = self.available_opposite_player_actions()
        print(f"\nPLAYER {self.get_player_position(self.current_player)}'s TURN\n")
        return self.get_action(actions)

    def play_round(self):
        while not self.is_round_over() and len(self.all_in_players) < len(self.active_players):
            if self.current_player == self.target_player:
                action = self.player_action()
            else:
                action = self.opposite_player_action()
                if action[0] == 'raise':
                    raise_amount = helpers.force_int_input("Raise amount:")
                    action = (action[0], raise_amount)
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
    
    def determine_hole_cards(self):
        for x in range(2):
            index = -1
            for i in self.deck.cards:
                index += 1
                print(f"{index} - {i}")
            y = helpers.force_int_input(f"\nCard {x}: ")
            self.target_player.hand.append(self.deck.cards[y])
            self.deck.cards.pop(y)

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
            y = helpers.force_int_input(f"\nCard {x}: ")
            self.community_cards.append(self.deck.cards[y])
            self.deck.cards.pop(y)

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

        if small_blind_player.chips == 0:
            self.all_in_players.append(small_blind_player)
        if big_blind_player.chips == 0:
            self.all_in_players.append(big_blind_player)