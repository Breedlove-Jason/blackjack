import pygame
import sys
import time
from constants import *
from blackjack_deck import Deck, Hand


def text_objects(text, font, color=BLACK):
    """Render text as a surface object."""
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def draw_text(screen, text, font, x, y, color=BLACK):
    """Draw text centered at (x, y) on the given screen."""
    text_surf, text_rect = text_objects(text, font, color)
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)


def button(screen, msg, x, y, w, h, ic, ac, action=None):
    """Create a clickable button with a message."""
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    color = ac if x + w > mouse[0] > x and y + h > mouse[1] > y else ic
    pygame.draw.rect(screen, color, (x, y, w, h))

    text_surf, text_rect = text_objects(msg, FONT)
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(text_surf, text_rect)

    if click[0] == 1 and action:
        action()


class BlackjackGame:
    def __init__(self):
        """Initialize the Blackjack game components."""
        self.deck = Deck()
        self.deck.shuffle()
        self.dealer = Hand()
        self.player = Hand()
        self.player_card_count = 0
        self.running = True

        # Setup Pygame display
        self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption("Blackjack")
        self.reset_display()

    def reset_display(self):
        """Reset the main display and background."""
        self.screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(self.screen, GRAY, pygame.Rect(0, 0, 250, 700))

    def play(self):
        """Main game loop."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            button(self.screen, "Deal", 30, 100, 150, 50, LIGHT_SLATE, DARK_SLATE, self.deal)
            button(self.screen, "Hit", 30, 200, 150, 50, LIGHT_SLATE, DARK_SLATE, self.hit)
            button(self.screen, "Stand", 30, 300, 150, 50, LIGHT_SLATE, DARK_SLATE, self.stand)
            button(self.screen, "EXIT", 30, 500, 150, 50, LIGHT_SLATE, DARK_RED, self.exit_game)

            pygame.display.flip()

    def exit_game(self):
        """Exit the game."""
        pygame.quit()
        sys.exit()

    def deal(self):
        """Deal initial hands to the player and dealer."""
        self.player = Hand()
        self.dealer = Hand()
        self.deck.shuffle()
        for _ in range(2):
            self.player.add_card(self.deck.deal())
            self.dealer.add_card(self.deck.deal())
        self.player_card_count = 2

        self.show_hands()
        self.check_blackjack()

    def hit(self):
        """Give the player one more card."""
        self.player.add_card(self.deck.deal())
        self.player_card_count += 1

        if self.player_card_count > 4:
            return

        self.show_hands()
        self.check_blackjack()

        if self.player.value > 21:
            self.show_dealer_hand()
            draw_text(self.screen, "Player Bust", GAME_END_FONT, 500, 350, RED)
            time.sleep(4)
            self.reset_display()

    def stand(self):
        """Finalize the dealer's hand and compare with the player."""
        while self.dealer.value < 17:
            self.dealer.add_card(self.deck.deal())
            self.dealer.calc_hand()

        self.show_hands(final=True)

        if self.dealer.value > 21 or self.player.value > self.dealer.value:
            message = "Player Wins!"
        elif self.player.value < self.dealer.value:
            message = "Dealer Wins!"
        else:
            message = "It's a Tie!"

        draw_text(self.screen, message, GAME_END_FONT, 500, 350, GREEN if "Wins" in message else BLACK)
        time.sleep(4)
        self.reset_display()

    def check_blackjack(self):
        """Check for Blackjack conditions and handle accordingly."""
        self.player.calc_hand()
        self.dealer.calc_hand()
        dealer_faceup_card = "./assets/images/" + self.dealer.card_img[1] + ".png"

        if self.player.value == 21 and self.dealer.value == 21:
            draw_text(self.screen, "Both Blackjack", BLACKJACK_FONT, 500, 250, GRAY)
        elif self.player.value == 21:
            draw_text(self.screen, "Player Blackjack", BLACKJACK_FONT, 500, 250, GRAY)
        elif self.dealer.value == 21:
            draw_text(self.screen, "Dealer Blackjack", BLACKJACK_FONT, 500, 250, GRAY)
        else:
            return

        time.sleep(4)
        self.reset_display()

    def show_hands(self, final=False):
        """Show the player's and dealer's hands on the screen."""
        self.player.calc_hand()
        self.dealer.calc_hand()
        self.player.display_cards()
        self.dealer.display_cards()

        # Dealer's cards
        draw_text(self.screen, "Dealer's hand:", TEXT_FONT, 500, 150)
        dealer_card_1 = pygame.image.load("./assets/images/" + self.dealer.card_img[0] + ".png").convert()
        dealer_card_2 = pygame.image.load("./assets/images/back.png").convert() if not final else pygame.image.load("./assets/images/" + self.dealer.card_img[1] + ".png").convert()
        self.screen.blit(dealer_card_1, (400, 200))
        self.screen.blit(dealer_card_2, (550, 200))

        # Player's cards
        draw_text(self.screen, "Player's hand:", TEXT_FONT, 500, 450)
        x_offset = 400
        for img_name in self.player.card_img:
            card_img = pygame.image.load("./assets/images/" + img_name + ".png").convert()
            self.screen.blit(card_img, (x_offset, 500))
            x_offset += 150

        pygame.display.flip()


if __name__ == "__main__":
    game = BlackjackGame()
    game.play()
