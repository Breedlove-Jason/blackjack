import random
from constants import SUITS, RANKS

class Deck:
    def __init__(self):
        """Initialize a deck with cards and build it."""
        self.cards = []
        self.build()

    def build(self):
        """Build a standard deck of 52 cards."""
        for value in RANKS:
            for suit in SUITS:
                self.cards.append((value, suit))

    def shuffle(self):
        """Shuffle the deck."""
        random.shuffle(self.cards)

    def deal(self):
        """Deal one card from the deck. Returns None if the deck is empty."""
        return self.cards.pop(0) if len(self.cards) > 0 else None


class Hand:
    def __init__(self):
        """Initialize a hand with an empty set of cards and reset the score."""
        self.cards = []
        self.card_img = []
        self.value = 0

    def add_card(self, card):
        """Add a card to the hand."""
        if card:
            self.cards.append(card)

    def calc_hand(self):
        """Calculate the score of the hand according to Blackjack rules."""
        self.value = 0
        non_aces = [card for card in self.cards if card[0] != "A"]
        aces = [card for card in self.cards if card[0] == "A"]

        for card in non_aces:
            rank = card[0]
            self.value += 10 if rank in "JQK" else int(rank)

        for ace in aces:
            self.value += 11 if self.value <= 10 else 1

    def display_cards(self):
        """Convert cards into image names (without file extensions)."""
        self.card_img = ["".join(card) for card in self.cards]
