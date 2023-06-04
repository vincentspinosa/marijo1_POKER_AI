class Card:
    def __init__(self, rank: int, suit: str):
        self.rank = rank
        self.suit = suit
        if self.rank < 11:
            self.sign = self.rank
        else:
            if self.rank == 11:
                self.sign = 'jack'
            elif self.rank == 12:
                self.sign = 'queen'
            elif self.rank == 13:
                self.sign = 'king'
            elif self.rank == 14:
                self.sign = 'ace'
            else:
                self.sign = None

    def __str__(self) -> str:
        return f"{self.sign} of {self.suit}".upper()
