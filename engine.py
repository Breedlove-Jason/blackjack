"""Browser rules adapted from Jason Breedlove's original Deck and Hand classes.
No display dependency; the original Pygame editions remain unchanged.
"""
import json
import random

SUITS = ['H', 'D', 'C', 'S']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

class Deck:
    def __init__(self, cards=None):
        self.cards = list(cards) if cards is not None else [(r, s) for s in SUITS for r in RANKS]
        if cards is None:
            random.shuffle(self.cards)

    def deal(self):
        if not self.cards:
            raise ValueError('Deck exhausted')
        return self.cards.pop(0)

class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    @property
    def value(self):
        value = sum(11 if r == 'A' else 10 if r in ('J', 'Q', 'K') else int(r) for r, _ in self.cards)
        aces = sum(r == 'A' for r, _ in self.cards)
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    @property
    def natural(self):
        return len(self.cards) == 2 and self.value == 21

class Game:
    def __init__(self):
        self.player, self.dealer = Hand(), Hand()
        self.phase = 'ready'
        self.message = 'Your seat is ready.'
        self.result = ''
        self.rounds = 0
        self.scores = {'win': 0, 'loss': 0, 'push': 0}

    def deal(self, cards=None):
        if self.phase == 'playing':
            return False
        self.deck = Deck(cards)
        self.player, self.dealer = Hand(), Hand()
        self.phase, self.result = 'playing', ''
        self.message = 'Your move. Hit or stand?'
        self.rounds += 1
        for _ in range(2):
            self.player.add_card(self.deck.deal())
            self.dealer.add_card(self.deck.deal())
        if self.player.natural and self.dealer.natural:
            self.finish('push', 'Two blackjacks. A perfect tie.')
        elif self.player.natural:
            self.finish('win', 'Blackjack. Beautifully played.')
        elif self.dealer.natural:
            self.finish('loss', 'Dealer blackjack. The next hand is yours.')
        return True

    def finish(self, result, message):
        if self.phase != 'playing':
            return
        self.phase, self.result, self.message = 'over', result, message
        self.scores[result] += 1

    def hit(self):
        if self.phase != 'playing':
            return False
        self.player.add_card(self.deck.deal())
        if self.player.value > 21:
            self.finish('loss', 'Over 21. Dealer takes the hand.')
        elif self.player.value == 21:
            self.stand()
        return True

    def stand(self):
        if self.phase != 'playing':
            return False
        while self.dealer.value < 17:
            self.dealer.add_card(self.deck.deal())
        if self.dealer.value > 21:
            self.finish('win', 'Dealer busts. This hand is yours.')
        elif self.player.value > self.dealer.value:
            self.finish('win', 'You win. A well-played hand.')
        elif self.player.value < self.dealer.value:
            self.finish('loss', 'Dealer wins. Another hand awaits.')
        else:
            self.finish('push', 'Push. An even match.')
        return True

    def snapshot(self):
        hidden = self.phase == 'playing'
        return json.dumps({'phase': self.phase, 'message': self.message, 'result': self.result,
            'player': self.player.cards, 'dealer': self.dealer.cards[:1] + [None] if hidden else self.dealer.cards,
            'player_total': self.player.value, 'dealer_total': None if hidden else self.dealer.value,
            'rounds': self.rounds, 'scores': self.scores})
