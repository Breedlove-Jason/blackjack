import tkinter as tk


class BlackjackGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Blackjack Game")
        self.master.geometry("800x600")  # Adjust size as needed

        self.setup_game_area()
        self.setup_action_buttons()

    def setup_game_area(self):
        self.dealer_label = tk.Label(self.master, text="Dealer's Hand:", font=("Arial", 14))
        self.dealer_label.pack()

        self.player_label = tk.Label(self.master, text="Player's Hand:", font=("Arial", 14))
        self.player_label.pack(pady=(10, 0))  # Add some padding

        # Placeholder for cards, you'll update these in your game logic
        self.dealer_cards = tk.Label(self.master, text="??", font=("Arial", 14))
        self.dealer_cards.pack()

        self.player_cards = tk.Label(self.master, text="A 10", font=("Arial", 14))
        self.player_cards.pack()

    def setup_action_buttons(self):
        self.hit_button = tk.Button(self.master, text="Hit", font=("Arial", 12), command=self.on_hit)
        self.hit_button.pack(side=tk.LEFT, padx=(10, 5))

        self.stay_button = tk.Button(self.master, text="Stay", font=("Arial", 12), command=self.on_stay)
        self.stay_button.pack(side=tk.LEFT, padx=(5, 10))

    def on_hit(self):
        # Placeholder for hit button functionality
        print("Hit button clicked")

    def on_stay(self):
        # Placeholder for stay button functionality
        print("Stay button clicked")
