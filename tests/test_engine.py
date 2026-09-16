import json
import unittest
from engine import Deck, Hand, Game

def cards(*ranks):
    return [(r, 'S') for r in ranks]

class Rules(unittest.TestCase):
    def test_deck_unique(self):
        deck = Deck()
        self.assertEqual(len(set(deck.cards)), 52)
    def test_aces(self):
        for ranks, expected in [(('A','A','9'),21),(('A','A','9','K'),21),(('A','6'),17),(('K','Q','2'),22)]:
            hand = Hand()
            for card in cards(*ranks): hand.add_card(card)
            self.assertEqual(hand.value, expected)
    def test_naturals(self):
        for ranks, result in [(('A','9','K','8'),'win'),(('9','A','8','K'),'loss'),(('A','A','K','K'),'push')]:
            game = Game(); game.deal(cards(*ranks))
            self.assertEqual(game.result, result)
            self.assertEqual(game.phase, 'over')
    def test_hidden_card(self):
        game = Game(); game.deal(cards('9','K','7','8'))
        state = json.loads(game.snapshot())
        self.assertEqual(state['dealer'], [['K','S'],None])
        self.assertIsNone(state['dealer_total'])
        game.stand()
        self.assertEqual(json.loads(game.snapshot())['dealer_total'], 18)
    def test_bust_and_lockout(self):
        game = Game(); game.deal(cards('K','9','8','8','K'))
        game.hit(); self.assertEqual(game.result, 'loss')
        self.assertFalse(game.hit()); self.assertFalse(game.stand())
        self.assertEqual(game.scores['loss'], 1)
    def test_no_redeal_during_hand(self):
        game = Game(); game.deal(cards('9','K','8','8'))
        self.assertFalse(game.deal()); self.assertEqual(game.rounds, 1)
    def test_dealer_soft17_stands(self):
        game = Game(); game.deal(cards('K','A','8','6','K'))
        game.stand(); self.assertEqual(len(game.dealer.cards),2)
        self.assertEqual(game.result, 'win')
    def test_dealer_draw_bust(self):
        game = Game(); game.deal(cards('K','9','8','7','K'))
        game.stand(); self.assertEqual(game.result, 'win')
    def test_hit21_auto_settles(self):
        game = Game(); game.deal(cards('K','9','5','8','6'))
        game.hit(); self.assertEqual(game.result,'win')
    def test_push(self):
        game = Game(); game.deal(cards('K','9','8','9'))
        game.stand(); self.assertEqual(game.result,'push')
    def test_more_than_five_cards(self):
        game = Game(); game.deal(cards('2','K','2','7','2','2','2','2'))
        for _ in range(4): game.hit()
        self.assertEqual(len(game.player.cards),6)
        self.assertEqual(game.phase,'playing')
    def test_next_hand_preserves_score(self):
        game = Game(); game.deal(cards('A','9','K','8'))
        game.deal(cards('9','K','7','8'))
        self.assertEqual(game.rounds,2); self.assertEqual(game.scores['win'],1)
        self.assertEqual(game.result,'')
    def test_ready_actions_ignored(self):
        game = Game(); self.assertFalse(game.hit()); self.assertFalse(game.stand())

if __name__ == '__main__': unittest.main()
