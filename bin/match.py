from ui import UI
from eval import evalAgent

class Match(UI):
    def __init__(self, players, target_player_index, dealer_position=0, small_blind=10, big_blind=20, current_pot=0, current_stage='pre-flop'):
        super().__init__(players, target_player_index, dealer_position, small_blind, big_blind, current_pot, current_stage)

    def deal_hole_cards(self):
        self.deck.shuffle()
        for player in self.players:
            player.hand = [self.deck.deal(), self.deck.deal()]

    def deal_community_cards(self):
        if self.current_stage == 'flop':
            self.community_cards = [self.deck.deal() for _ in range(3)]
        elif self.current_stage in ['turn', 'river']:
            self.community_cards += [self.deck.deal()]

    def create_deck_to_send_to_ai(self, target_player_index):
        return self.deck + self.get_next_player(target_player_index).hand
    def play_preflop(self):
        print("\nPREFLOP\n")
        self.determine_hole_cards()
        self.collect_blinds()
        self.play_round()
    
    def get_action(self, actions):
        index = -1
        for i in actions:
            index += 1
            print(f"{index} - {i}")
        return actions[int(input("\nChosen action: "))]

    def ai_action(self):
        actions = self.available_actions()
        print("\nAI's TURN")
        print(f"\nAI's MOVE: {evalAgent.eval(self, 3)}\n")
        return self.get_action(actions)
    
    def opposite_player_action(self):
        print("\n Your hand:")
        player = self.players[self.get_player_position(self.current_player)]
        for card in player.hand:
            print(card.__str__())
        actions = self.available_opposite_player_actions()
        print(f"\nPLAYER {self.get_player_position(self.current_player)}'s TURN\n")
        return self.get_action(actions)

    def play_round(self):
        while not self.is_round_over() and len(self.all_in_players) < len(self.active_players):
            if self.current_player == self.target_player:
                action = self.ai_action()
            else:
                action = self.opposite_player_action()
                if action[0] == 'raise':
                    raise_amount = int(input("Raise amount:"))
                    action = (action[0], raise_amount)
            self.handle_action(action[0], raise_amount=action[1])
            self.next_player()
        self.reset_round()

    def play_flop(self):
        print("\nFLOP\n")
        self.current_stage = 'flop'
        self.deal_community_cards()
        self.play_round()

    def play_turn(self):
        print("\nTURN\n")
        self.current_stage = 'turn'
        self.deal_community_cards()
        self.play_round()

    def play_river(self):
        print("\nRIVER\n")
        self.current_stage = 'river'
        self.deal_community_cards()
        self.play_round()
        