class Player:
    def __init__(self, chips=1000):
        self.chips = chips
        self.hand = []

    def bet(self, amount):
        self.chips -= amount
        return amount

    """ def fold(self):
        self.hand = [] """

    def __str__(self):
        return f"Player has {self.chips} chips and a hand of {self.hand[0]} and {self.hand[1]}"
