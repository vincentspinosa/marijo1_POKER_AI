import random
#from rules.card import Card
from treys import Card

class Deck:
    def __init__(self):
        self.cards = [Card.new(rank + suit) for suit in 'shdc' for rank in Card.STR_RANKS]

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def deal(self) -> list:
        return self.cards.pop()

""" class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for rank in range(2, 15) for suit in ('hearts', 'diamonds', 'clubs', 'spades')]

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def deal(self) -> list:
        return self.cards.pop() """
