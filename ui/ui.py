from gameState.gameState import GameState
from eval import evalAgent
from helper_functions.helpers import force_int_input
from rules.player import Player
from ai import ai


class UI(GameState):
    def __init__(self, players:tuple[Player], ai_player_index:int, dealer_position:int=0, small_blind:int=10, big_blind:int=20, current_pot:int=0, current_stage:str='pre-flop'):
        super().__init__(players, ai_player_index, dealer_position, small_blind, big_blind, current_pot, current_stage)

    """ 
        methods of the UI class:

            - deal_hole_cards(self)
            - deal_community_cards(self)
            - new_hand(self)
            - is_game_over(self)
            - is_hand_over(self)
            - is_round_over(self)
            - play_round(self)
            - round(self, stage)
            - reset_round(self)
            - end_round(self, winner)
            - move_dealer_button(self)
            - collect_blinds(self)
            - ai_action(self)
            - get_action(self, actions)
            - human_action(self)
            - available_human_player_actions(self)
            - print_round_info(self)
    """

    def deal_hole_cards(self) -> None:
        self.deck.shuffle()
        for player in self.players:
            player.hand = [self.deck.deal(), self.deck.deal()]

    def deal_community_cards(self) -> None:
        if self.current_stage == 'flop':
            self.community_cards = [self.deck.deal() for _ in range(3)]
        elif self.current_stage in ['turn', 'river']:
            self.community_cards += [self.deck.deal()]

    def is_game_over(self) -> bool:
        if self.players[0].chips == 0 or self.players[1].chips == 0:
            return True
        return False

    def is_hand_over(self) -> bool:
        if len(self.active_players) < 2 or len(self.all_in_players) == len(self.active_players):
            return True
        return False

    def is_round_over(self) -> bool:
        if len(self.active_players) < 2 or len(self.all_in_players) == len(self.active_players):
            return True
        if self.round_turns >= len(self.round_players) or self.current_stage == 'pre-flop':
            active_bets = [bet for player, bet in self.current_bets.items() if player in self.active_players]
            print(f"\nActive bets: {active_bets}\n")
            if len(set(active_bets)) == 1:
                return True 
        return False

    def play_round(self) -> None:
        while not self.is_round_over():
            if self.current_player == self.ai_player:
                action = self.ai_action()
            else:
                action = self.human_action()
                if action[0] == 'raise':
                    raise_amount = force_int_input("Raise amount:")
                    action = (action[0], raise_amount)
            self.handle_action(action[0], raise_amount=action[1])
            self.next_player()
        self.reset_round()

    def round(self, stage:str='pre-flop') -> None:
        if stage != 'pre-flop':
            self.current_stage = stage
        if self.current_stage == 'pre-flop':
            self.collect_blinds()
            self.deal_hole_cards()
        else:
            self.deal_community_cards()
        self.print_round_info()
        self.play_round()

    def reset_round(self) -> None:
        self.current_player = self.players[(self.dealer_position + 1) % len(self.players)]
        self.round_turns = 0
        self.round_players = self.active_players

    def end_round(self, winnerIndex:int) -> None:
        if winnerIndex == 0 or winnerIndex == 1:
            self.players[winnerIndex].chips += self.current_pot
        else:
            self.players[0].chips = int(self.players[0].chips + (self.current_pot / 2))
            self.players[1].chips = int(self.players[1].chips + (self.current_pot / 2))
        self.current_pot = 0

    def move_dealer_button(self) -> None:
        self.dealer_position = (self.dealer_position + 1) % len(self.players)

    def collect_blinds(self) -> None:
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

    def ai_action(self) -> tuple:
        print("\nAI's TURN")
        # printing for testing
        print("\nAI's hand:")
        for card in self.current_player.hand:
            print(card.__str__())
        ai_move = evalAgent.get_play(ai.algorithm(self, 1)['probability_distribution'])[0]
        print(f"\nAI's MOVE: {ai_move}\n")
        return ai_move
    
    def get_action(self, actions:list[tuple]) -> tuple:
        index = -1
        for i in actions:
            index += 1
            print(f"{index} - {i}")
        return actions[int(input("\nChosen action: "))]
    
    def human_action(self) -> tuple:
        player = self.current_player
        print("\nYour hand:")
        for card in player.hand:
            print(card.__str__())
        print("\nAvailable actions:")
        actions = self.available_human_player_actions()
        return self.get_action(actions)
    
    def available_human_player_actions(self) -> list[tuple]:
        actions = []
        if self.current_player not in self.active_players:
            return actions
        actions.append(('fold', 0))
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

    def print_round_info(self) -> None:
        print("\n-----------------------------------------------")
        print(f"\nRound: {self.current_stage}".upper())
        print(f"\nCurrent pot: {self.current_pot}".upper())
        self.print_players_chips()
        if len(self.community_cards) > 0:
            self.print_community_cards()
        print("\n-----------------------------------------------")
        print("\n")

    def print_players_chips(self) -> None:
        x = 0
        for player in self.players:
            print(f"\nChips of player {x}: {player.chips}".upper())
            x += 1

    def print_community_cards(self) -> None:
        print("\nCommunity cards:")
        for card in self.community_cards:
            print(card.__str__())


def new_hand(gameUI:UI) -> UI:
    new_hand = UI(gameUI.players, gameUI.get_player_position(gameUI.ai_player), gameUI.dealer_position, gameUI.small_blind, gameUI.big_blind, 0, 'pre-flop')
    return new_hand
