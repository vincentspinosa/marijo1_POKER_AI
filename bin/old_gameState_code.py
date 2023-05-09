def deal_all_community_cards(self):
    self.deck.shuffle()
    if self.current_stage == 'flop':
        self.community_cards = [self.deck.deal() for _ in range(3)]
    if self.current_stage == 'turn':
        self.community_cards = [self.deck.deal() for _ in range(4)]
    if self.current_stage == 'river':
        self.community_cards = [self.deck.deal() for _ in range(5)]