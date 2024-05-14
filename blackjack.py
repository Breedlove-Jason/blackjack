import pygame
import random
import sys
import os
import time

# Constants
DISPLAY_WIDTH = 900
DISPLAY_HEIGHT = 700

BACKGROUND_COLOR = (34, 139, 134)
GRAY = (220, 220, 220)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
LIGHT_SLATE = (119, 136, 153)
DARK_SLATE = (119, 136, 153)
DARK_RED = (94, 21, 21)

SUITS = ["H", "D", "C", "S"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

pygame.init()
font = pygame.font.SysFont("Arial", 20)
textfont = pygame.font.SysFont("Comic Sans MS", 25)
game_end = pygame.font.SysFont("dejavusans", 100)
blackjack_font = pygame.font.SysFont("Roboto", 70)


# Deck and Hand Classes
class Deck:
    """
    Represents a deck of cards.
    """

    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        """
        Builds a new deck of cards.
        """
        self.cards = [(rank, suit) for suit in SUITS for rank in RANKS]

    def shuffle(self):
        """
        Shuffles the deck of cards.
        """
        random.shuffle(self.cards)

    def deal(self):
        """
        Deals a card from the deck.
        """
        return self.cards.pop(0) if self.cards else None


class Hand:
    """
    Represents a hand of cards.
    """

    def __init__(self):
        self.cards = []
        self.value = 0

    def add_card(self, card):
        """
        Adds a card to the hand.
        """
        self.cards.append(card)
        self.calc_value()

    def calc_value(self):
        """
        Calculates the value of the hand.
        """
        self.value = 0
        aces = 0
        for rank, suit in self.cards:
            if rank in "JQK":
                self.value += 10
            elif rank == "A":
                aces += 1
                self.value += 11
            else:
                self.value += int(rank)
        while self.value > 21 and aces:
            self.value -= 10
            aces -= 1

    def win_condition(self, other_hand):
        if self.value > 21:
            return "Player Busts! Dealer Wins!"
        elif other_hand.value > 21:
            return "Dealer Busts! Player Wins!"
        elif self.value > other_hand.value:
            return "Player Wins!"
        elif self.value < other_hand.value:
            return "Dealer Wins!"
        else:
            return "It's a Tie!"

    def display_cards(self):
        """
        Displays the cards in the hand.
        """
        return ["".join(card) for card in self.cards]


# Helper Functions
def text_objects(text, font, color):
    """
    Creates a text surface and its rect.
    """
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def display_text(screen, text, font, x, y, color):
    """
    Displays text on the screen.
    """
    text_surf, text_rect = text_objects(text, font, color)
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)


def game_texts(screen, text, x, y):
    """
    Displays game text on the screen.
    """
    display_text(screen, text, textfont, x, y, BLACK)


def game_finish(screen, text, x, y, color):
    """
    Displays game finish text on the screen.
    """
    display_text(screen, text, game_end, x, y, color)
    pygame.display.flip()
    time.sleep(4)  # Delay to make the result visible


def display_card(screen, card, x, y):
    """
    Displays a card on the screen.
    """
    card_value, card_suit = card
    card_img = pygame.image.load(os.path.join('assets', 'images', f'{card_value}{card_suit}.png'))
    screen.blit(card_img, (x, y))


def deal_card(deck, hand):
    """
    Deals a card to a hand.
    """
    hand.add_card(deck.deal())


def handle_events():
    global game_state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                game_state = 'play'
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_c:
                game_state = 'play'


# Game Functions
def game_intro():
    """
    Displays the game intro screen.
    """
    global game_state
    while game_state == 'intro':
        handle_events()

        screen.fill(BACKGROUND_COLOR)
        game_texts(screen, "Welcome to Blackjack!", DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 4)
        game_texts(screen, "Press 'C' to play or 'Q' to quit", DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2)
        pygame.display.flip()
        clock.tick(15)


def game_loop():
    """
    Main game loop for blackjack.
    """
    global game_state
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    dealer_hand = Hand()

    deal(deck, player_hand, dealer_hand)

    while game_state == 'play':
        handle_events()

        screen.fill(BACKGROUND_COLOR)

        game_texts(screen, "Blackjack", DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 8)
        game_texts(screen, "Player's Hand", DISPLAY_WIDTH // 4, DISPLAY_HEIGHT // 4)
        game_texts(screen, "Dealer's Hand", 3 * DISPLAY_WIDTH // 4, DISPLAY_HEIGHT // 4)

        x_player = 100
        x_dealer = DISPLAY_WIDTH // 2 + 100

        for card in player_hand.cards:
            display_card(screen, card, x_player, DISPLAY_HEIGHT // 2)
            x_player += 100  # Increment to offset cards

        for card in dealer_hand.cards:
            display_card(screen, card, x_dealer, DISPLAY_HEIGHT // 2)
            x_dealer += 100  # Increment to offset cards

        # Redraw buttons each frame
        draw_button("Deal", 50, 650, 100, 50, LIGHT_SLATE, DARK_SLATE, lambda: deal(deck, player_hand, dealer_hand))
        draw_button("Hit", 200, 650, 100, 50, LIGHT_SLATE, DARK_SLATE, lambda: hit(deck, player_hand))
        draw_button("Stand", 350, 650, 100, 50, LIGHT_SLATE, DARK_SLATE, lambda: stand(deck, player_hand, dealer_hand))

        pygame.display.flip()
        clock.tick(30)  # Limit the frame rate to 30 FPS

        if player_hand.value > 21:
            player_bust = True
            game_state = 'end'
            game_finish(screen, "Player Busts! Dealer Wins!", DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2, RED)
        elif dealer_hand.value > 21:
            game_state = 'end'
            game_finish(screen, "Dealer Busts! Player Wins!", DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2, GREEN)


def game_over_screen():
    """
    Displays the game over screen with options to play again or quit.
    """
    global game_state
    while game_state == 'end':
        handle_events()

        screen.fill(BACKGROUND_COLOR)
        game_texts(screen, "Game Over", DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 4)
        game_texts(screen, "Press 'P' to play again or 'Q' to quit", DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2)
        pygame.display.flip()
        clock.tick(15)


# Helper functions for button interactions
def deal(deck, player_hand, dealer_hand):
    player_hand.cards.clear()
    dealer_hand.cards.clear()
    for _ in range(2):
        deal_card(deck, player_hand)
        deal_card(deck, dealer_hand)
    player_hand.calc_value()
    dealer_hand.calc_value()


def hit(deck, hand):
    if len(hand.cards) < 5:
        deal_card(deck, hand)
        hand.calc_value()


def stand(deck, player_hand, dealer_hand):
    while dealer_hand.value < 17:
        deal_card(deck, dealer_hand)
        dealer_hand.calc_value()

    check_win(player_hand, dealer_hand)


def check_win(player_hand, dealer_hand):
    result = player_hand.win_condition(dealer_hand)
    game_finish(screen, result, DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2, GREEN if "Wins" in result else BLACK)
    global game_state
    game_state = 'end'


def draw_button(text, x, y, width, height, inactive_color, active_color, action):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1:
            action()
            pygame.event.clear(pygame.MOUSEBUTTONDOWN)  # Clear the button press event
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))
    game_texts(screen, text, x + width / 2, y + height / 2)


# Main Code
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Blackjack")
clock = pygame.time.Clock()

game_state = 'intro'  # Define game_state before calling game_intro

while True:
    if game_state == 'intro':
        game_intro()
    elif game_state == 'play':
        game_loop()
    elif game_state == 'end':
        game_over_screen()

pygame.quit()
sys.exit()
