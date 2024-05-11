from random import randint

CARD_MAP = {
    1: ("A", (1, 11)),  # Ace can be 1 or 11
    2: ("2", 2),
    3: ("3", 3),
    4: ("4", 4),
    5: ("5", 5),
    6: ("6", 6),
    7: ("7", 7),
    8: ("8", 8),
    9: ("9", 9),
    10: ("10", 10),
    11: ("J", 10),
    12: ("Q", 10),
    13: ("K", 10),
}


def draw_card():
    """Draw a single card from the deck."""
    card = randint(1, 13)
    card_face, card_value = CARD_MAP[card]
    return card_face, card_value


def player_choice(hand_value):
    """Handle the player's decision to hit or stay."""
    while True:
        choice = input("Do you want to hit or stay? (Enter 'h' for hit and 's' for stay): ")
        if choice.lower() == 'h':
            card_face, card_value = draw_card()
            if card_face == "A":
                card_value = 11 if hand_value + 11 <= 21 else 1
            hand_value += card_value
            print(f"You were dealt a {card_face}. Your total is now {hand_value}.")
            if hand_value >= 21:
                break
        elif choice.lower() == 's':
            print(f"You chose to stay. Your total is {hand_value}.")
            break
        else:
            print("Invalid choice. Please enter 'h' for hit or 's' for stay.")
    return hand_value


def computer_choice():
    """Automatically decide the dealer's moves."""
    hand_value = 0
    while hand_value < 17:
        card_face, card_value = draw_card()
        card_value = card_value if isinstance(card_value, int) else 11 if hand_value + 11 <= 21 else 1
        hand_value += card_value
    return hand_value


def winner(player_hand_value, computer_hand_value):
    """Determine the game's winner."""
    if player_hand_value > 21:
        return "Computer wins!"
    elif computer_hand_value > 21 or player_hand_value > computer_hand_value:
        return "Player wins!"
    elif player_hand_value == computer_hand_value:
        return "It's a tie!"
    else:
        return "Computer wins!"


def game_loop():
    """The main game loop."""
    while True:
        player_card1_face, player_card1_value = draw_card()
        player_card2_face, player_card2_value = draw_card()
        print(f"You were dealt: {player_card1_face}, {player_card2_face}")
        player_hand_value = player_card1_value + (player_card2_value if isinstance(player_card2_value, int) else 11)

        final_player_hand_value = player_choice(player_hand_value)

        if final_player_hand_value <= 21:
            final_computer_hand_value = computer_choice()
            print(f"Dealer's final hand value: {final_computer_hand_value}")
        else:
            print("Player busts!")
            break

        game_winner = winner(final_player_hand_value, final_computer_hand_value)
        print(game_winner)
        break


if __name__ == "__main__":
    game_loop()
