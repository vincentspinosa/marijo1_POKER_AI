class Player:
    def __init__(self, chips: int=1000):
        self.chips = chips
        self.hand = []

    def bet(self, amount: int) -> int:
        self.chips -= amount
        return amount

    def __str__(self) -> str:
        return f"Player has {self.chips} chips and a hand of {self.hand[0]} and {self.hand[1]}"
