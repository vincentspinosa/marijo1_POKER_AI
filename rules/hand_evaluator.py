from rules.card import Card

HAND_RANKS = {
    'HIGH_CARD': 1,
    'PAIR': 2,
    'TWO_PAIR': 3,
    'THREE_OF_A_KIND': 4,
    'STRAIGHT': 5,
    'FLUSH': 6,
    'FULL_HOUSE': 7,
    'FOUR_OF_A_KIND': 8,
    'STRAIGHT_FLUSH': 9,
    'ROYAL_FLUSH': 10
}

class HandEvaluator:
    def __init__(self):
        self.rank = 0
        self.hand = []

    def evaluate_hand(self, player_cards: list[Card], community_cards: list[Card]) -> tuple:
        all_cards = player_cards + community_cards
        all_cards.sort(key=lambda x: x.rank, reverse=True)

        if self.check_royal_flush(all_cards):
            return (HAND_RANKS['ROYAL_FLUSH'], self.hand)
        elif self.check_straight_flush(all_cards):
            return (HAND_RANKS['STRAIGHT_FLUSH'], self.hand)
        elif self.check_n_of_a_kind(all_cards, 4):
            return (HAND_RANKS['FOUR_OF_A_KIND'], self.hand)
        elif self.check_full_house(all_cards):
            return (HAND_RANKS['FULL_HOUSE'], self.hand)
        elif self.check_flush(all_cards):
            return (HAND_RANKS['FLUSH'], self.hand)
        elif self.check_straight(all_cards):
            return (HAND_RANKS['STRAIGHT'], self.hand)
        elif self.check_n_of_a_kind(all_cards, 3):
            return (HAND_RANKS['THREE_OF_A_KIND'], self.hand)
        elif self.check_two_pair(all_cards):
            return (HAND_RANKS['TWO_PAIR'], self.hand)
        elif self.check_n_of_a_kind(all_cards, 2):
            return (HAND_RANKS['PAIR'], self.hand)
        else:
            self.hand = all_cards[:5]
            return (HAND_RANKS['HIGH_CARD'], self.hand)

    def check_flush(self, cards: list[Card]) -> bool:
        # Determine if all cards have the same suit
        suits = [card.suit for card in cards]
        if len(set(suits)) == 1:
            self.hand = cards[:5]
            return True
        return False

    def check_straight(self, cards: list[Card]) -> bool:
        # Determine if the cards form a straight
        unique_ranks = sorted(set([card.rank for card in cards]), reverse=True)
        if len(unique_ranks) < 5:
            return False
        for i in range(4):
            if unique_ranks[i] - unique_ranks[i+1] != 1:
                return False
        self.hand = [card for card in cards if card.rank in unique_ranks[:5]]
        return True

    def check_n_of_a_kind(self, cards: list[Card], n: int) -> bool:
        # Determine if there are n cards with the same rank
        rank_counts = {card.rank: 0 for card in cards}
        for card in cards:
            rank_counts[card.rank] += 1
        for rank, count in rank_counts.items():
            if count == n:
                self.hand = [card for card in cards if card.rank == rank]
                return True
        return False

    def check_full_house(self, cards: list[Card]) -> bool:
        # Determine if the cards form a full house (three of a kind and a pair)
        rank_counts = {card.rank: 0 for card in cards}
        for card in cards:
            rank_counts[card.rank] += 1
        has_three = False
        has_two = False
        for rank, count in rank_counts.items():
            if count == 3:
                has_three = True
                self.hand = [card for card in cards if card.rank == rank]
            elif count == 2:
                has_two = True
                self.hand += [card for card in cards if card.rank == rank]
        return has_three and has_two

    def check_two_pair(self, cards: list[Card]) -> bool:
        # Determine if the cards form two pairs
        rank_counts = {card.rank: 0 for card in cards}
        for card in cards:
            rank_counts[card.rank] += 1
        pairs = [rank for rank, count in rank_counts.items() if count == 2]
        if len(pairs) < 2:
            return False
        self.hand = [card for card in cards if card.rank in pairs]
        return True

    def check_straight_flush(self, cards: list[Card]) -> bool:
        # Determine if the cards form a straight flush
        if self.check_flush(cards) and self.check_straight(cards):
            return True
        return False

    def check_royal_flush(self, cards: list[Card]) -> bool:
        # Determine if the cards form a royal flush (A, K, Q, J, 10 of the same suit)
        if self.check_flush(cards):
            rank_set = set([card.rank for card in cards])
            if rank_set == {'A', 'K', 'Q', 'J', '10'}:
                self.hand = cards[:5]
                return True
        return False
