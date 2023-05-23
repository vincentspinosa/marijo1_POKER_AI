class Card:
    def __init__(self, rank: int, suit: str):
        self.rank:int = rank
        self.suit:str = suit

    def __str__(self) -> str:
        return f"{self.rank} of {str(self.suit).upper()}"
