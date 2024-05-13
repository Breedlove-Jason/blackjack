import pygame

# Display dimensions and colors
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

# Fonts
pygame.init()
FONT = pygame.font.SysFont("Arial", 20)
TEXT_FONT = pygame.font.SysFont("Comic Sans MS", 25)
GAME_END_FONT = pygame.font.SysFont("DejaVuSans", 100)
BLACKJACK_FONT = pygame.font.SysFont("Roboto", 70)

# Card properties
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)

# Suits and Ranks
SUITS = ["H", "D", "C", "S"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
