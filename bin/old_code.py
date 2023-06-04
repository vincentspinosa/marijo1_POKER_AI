#remote solver

""" def ask_card_input(self, nb_cards, hole_cards=True):
    for x in range(nb_cards):
        index = -1
        for i in self.deck.cards:
            index += 1
            print(f"{index} - {i}")
        y = helpers.force_int_input(f"\nCard {x}: ")
        if hole_cards == True:
            self.target_player.hand.append(self.deck.cards[y])
        else:
            self.community_cards.append(self.deck.cards[y])
        self.deck.cards.pop(y)

def determine_hole_cards(self):
    self.ask_card_input(2, hole_cards=True)

def determine_community_cards(self):
    if self.current_stage == 'flop':
        nb_cards = 3
    elif self.current_stage in ['turn', 'river']:
        nb_cards = 1
    self.ask_card_input(nb_cards, hole_cards=False) """