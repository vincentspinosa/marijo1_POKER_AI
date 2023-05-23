from gameState import gameState
from eval import evalAgent
from helper_functions import helpers

class UI(gameState.GameState):
    def __init__(self, players, ai_player_index, dealer_position=0, small_blind=10, big_blind=20, current_pot=0, current_stage='pre-flop'):
        super().__init__(players, ai_player_index, dealer_position, small_blind, big_blind, current_pot, current_stage)

    def new_hand(self):
        new_hand = UI(self.players, self.get_player_position(self.ai_player), self.dealer_position, self.small_blind, self.big_blind, 0, 'pre-flop')
        return new_hand

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
        if winner == 0 or winner == 1:
            self.players[winner].chips += self.current_pot
        else:
            self.players[0].chips = int(self.players[0].chips + (self.current_pot / 2))
            self.players[1].chips = int(self.players[1].chips + (self.current_pot / 2))
        self.current_pot = 0

    def eliminate_player(self, player):
        self.active_players = self.active_players[:self.get_player_position(player)] + self.active_players[(self.get_player_position(player) + 1):]

    def move_dealer_button(self):
        self.dealer_position = (self.dealer_position + 1) % len(self.players)

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

    def print_round_info(self):
        print("\n-----------------------------------------------")
        print(f"\nRound: {self.current_stage}".upper())
        x = 0
        for player in self.players:
            print(f"\nChips of player {x}: {player.chips}".upper())
            x += 1
        print(f"\nCurrent pot: {self.current_pot}".upper())
        print("\n-----------------------------------------------")
        print("\n")
