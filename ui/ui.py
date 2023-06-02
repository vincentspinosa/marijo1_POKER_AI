from gameState.gameState import GameState
from eval import evalAgent
from helper_functions.helpers import force_int_input
from rules.player import Player
from ai import ai
from treys import Card

# new_hand() is declared below the UI class!

class UI(GameState):
    def __init__(self, ai_iterations: int, players: tuple[Player], ai_player_index: int, ai_verbose: int=0, ai_verbose_steps: int=50, dealer_position: int=0, small_blind: int=10, big_blind: int=20, current_pot: int=0, current_stage: str='pre-flop'):
        super().__init__(players=players, ai_player_index=ai_player_index, dealer_position=dealer_position, small_blind=small_blind, big_blind=big_blind, current_pot=current_pot, current_stage=current_stage)
        self.ai_iterations = ai_iterations
        self.hand_is_over:bool = False
        self.ai_verbose = ai_verbose
        self.ai_verbose_steps = ai_verbose_steps
        print(self.ai_verbose)

    """ 
        methods of the UI class:

            - deal_hole_cards(self)
            - deal_community_cards(self)
            - new_hand(self)
            - is_game_over(self)
            - set_if_hand_over(self)
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
            - print_players_chips(self)
            - print_community_cards(self)
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

    def set_if_hand_over(self) -> None:
        if self.hand_is_over == True:
            return
        if self.dontHaveToAnswer == True:
            self.hand_is_over = True
            return
        if len(self.active_players) < 2 or len(self.all_in_players) == len(self.active_players):
            self.hand_is_over = True
            return
        if len(self.all_in_players) == len(self.active_players) - 1 and self.round_turns > 0:
            active_bets = [bet for player, bet in self.current_bets.items() if player in self.active_players]
            print(f"\nActive bets: {active_bets}\n")
            print(f"Len set active bets: {len(set(active_bets))}".upper())
            if len(set(active_bets)) == 1:
                print("1 player is all in but all bets are the same size.".upper())
                self.hand_is_over = True
                return
        if self.ai_player.chips == 0 or self.get_next_player(self.ai_player).chips == 0:
            self.hand_is_over = True
            return

    def is_round_over(self) -> bool:
        if len(self.active_players) < 2 or len(self.all_in_players) == len(self.active_players):
            return True
        if self.round_turns >= len(self.round_players) or self.current_stage == 'pre-flop':
            active_bets = [bet for player, bet in self.current_bets.items() if player in self.active_players]
            print(f"\nActive bets: {active_bets}\n")
            if len(set(active_bets)) == 1:
                return True 
        return False

    def play_round(self, print_ai_cards=False) -> None:
        self.reset_round()
        while not self.is_round_over():
            if self.current_player == self.ai_player:
                action = self.ai_action(print_ai_cards=print_ai_cards)
            else:
                action = self.human_action()
                if action[0] == 'raise':
                    raise_amount = force_int_input("Raise amount: ")
                    action = (action[0], raise_amount)
            self.handle_action(action[0], raise_amount=action[1])
            self.next_player()

    def round(self, stage:str='pre-flop', print_ai_cards=False) -> None:
        if stage != 'pre-flop':
            self.current_stage = stage
        if self.current_stage == 'pre-flop':
            self.collect_blinds()
            self.deal_hole_cards()
        else:
            self.deal_community_cards()
        self.print_round_info()
        self.play_round(print_ai_cards=print_ai_cards)

    def reset_round(self) -> None:
        self.current_player = self.players[(self.dealer_position + 1) % len(self.players)]
        self.round_turns = 0
        self.round_players = self.active_players

    def first_to_act_rule(self) -> None:
        if self.current_pot % 2 == 1:
            self.players[(self.dealer_position + 1) % 2].chips += 1
            self.current_pot -= 1

    def split_pot(self) -> None:
        self.first_to_act_rule()
        self.players[0].chips = int(self.players[0].chips + (self.current_pot / 2))
        self.players[1].chips = int(self.players[1].chips + (self.current_pot / 2))

    def end_hand(self, winnerIndex:int or None) -> None:
        if len(self.active_players) > 1:
            if self.lastActionIsCheck == True or not (winnerIndex == 0 or winnerIndex == 1):
                self.split_pot()
            else:
                self.players[winnerIndex].chips += self.current_pot
        else:
            self.active_players[0].chips += self.current_pot
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
        print("\nBlinds collected!")

    def ai_action(self, print_ai_cards=False) -> tuple:
        print("\nMarijo1's TURN")
        if print_ai_cards == True:
            print("\nMarijo1's hand:")
            for card in self.current_player.hand:
                print(Card.print_pretty_card(card))
        ai_move = evalAgent.get_play(ai.algorithm(self, iterations=self.ai_iterations, verboseLevel=self.ai_verbose, verboseIterationsSteps=self.ai_verbose_steps))[0]
        print(f"\nMarijo1's MOVE: {ai_move}\n")
        return ai_move
    
    def get_action(self, actions:list[tuple]) -> tuple:
        index = -1
        for i in actions:
            index += 1
            print(f"{index} - {i}")
        return actions[force_int_input("\nChosen action: ")]
    
    def human_action(self) -> tuple:
        player = self.current_player
        print("\nYour hand:")
        Card.print_pretty_cards(player.hand)
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
        players_dict = {0: "Marijo1", 1: "You"}
        self.print_players_chips(players_dict)
        if len(self.community_cards) > 0:
            self.print_community_cards()
        print("\n-----------------------------------------------")

    def print_showdown_info(self) -> None:
        print("\nShowdown!".upper())
        players_dict = {0: "Marijo1", 1: "Your"}
        self.print_community_cards()
        self.print_players_cards(players_dict)

    def print_players_chips(self, players_dict:dict) -> None:
        x = 0
        for player in self.players:
            print(f"\nChips of {players_dict[x]}: {player.chips}".upper())
            x += 1

    def print_players_cards(self, players_dict:dict) -> None:
        print("\nPlayers's card:")
        x = 0
        for p in self.players:
            print(f"\n{players_dict[x]} cards:")
            Card.print_pretty_cards(p.hand)
            x += 1

    def print_community_cards(self) -> None:
        print("\nCommunity cards:")
        Card.print_pretty_cards(self.community_cards)

def new_hand(gameUI:UI) -> UI:
    new_hand = UI(ai_iterations=gameUI.ai_iterations, players=gameUI.players, ai_player_index=gameUI.get_player_position(gameUI.ai_player), ai_verbose=gameUI.ai_verbose, ai_verbose_steps=gameUI.ai_verbose_steps, dealer_position=gameUI.dealer_position, small_blind=gameUI.small_blind, big_blind=gameUI.big_blind, current_pot=0, current_stage='pre-flop')
    return new_hand
