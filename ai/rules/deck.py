import random
from treys import Card

class Deck:
    def __init__(self):
        self.cards = [Card.new(rank + suit) for suit in 'shdc' for rank in Card.STR_RANKS]

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def deal(self) -> list:
        return self.cards.pop()
