import random
from rules.card import Card

class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for rank in range(2, 15) for suit in ('coeur', 'carreaux', 'trefle', 'pique')]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()
