import pygame as pygame

display_width = 900
display_height = 700

background_color = (34, 139, 134)
gray = (220, 220, 220)
black = (0, 0, 0)
green = (0, 200, 0)
red = (255, 0, 0)
light_slat = (119, 136, 153)
dark_slat = (119, 136, 153)
dark_red = (94, 21, 21)

pygame.init()
font = pygame.font.SysFont("Arial", 20)
textfont = ("Comic Sans MS", 25)
game_end = pygame.font.SysFont("dejavusans", 100)
blackjack = pygame.font.SysFont("Roboto", 70)
SUITS = ["H", "D", "C", "S"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
