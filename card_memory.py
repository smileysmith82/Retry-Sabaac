
class CardMemory:
    def __init__(self):
        # Every physical card and its known location.
        # Possible locations: own_hand, opponent_hand,
        # discard_pile, unknown.
        self.cards = {}

        self.opponent_hand_sizes = {}

    def initialize_cards(self, cards):
        self.cards.clear()
        self.opponent_hand_sizes.clear()

        for card in cards:
            self.cards[card] = {
                "location": "unknown",
                "owner": None}

    def initialize_opponent_hand_sizes(self, players, ai_player):
        for player in players:
            if player is not ai_player:
                self.remember_opponent_hand_size(player, len(player.hand))

    def update_card_location(self, card, location, owner=None):
        if card not in self.cards:
            return

        self.cards[card]["location"] = location
        self.cards[card]["owner"] = owner

    def remember_own_hand(self, player):
        for card in player.hand:
            self.update_card_location(card, "own_hand", player)

    def remember_top_discard(self, card):
        if card is not None:
            self.update_card_location(card, "discard_pile")

    def remember_opponent_hand_size(self, opponent, hand_size):
        self.opponent_hand_sizes[opponent] = hand_size

    def get_cards_at_location(self, location):
        return { card for card, info in self.cards.items() 
                if info["location"] == location }

    def get_known_opponent_cards(self, opponent):
        return { card for card, info in self.cards.items() 
                if info["location"] == "opponent_hand" and info["owner"] == opponent }

    def get_unknown_opponent_count(self, opponent):
        hand_size = self.opponent_hand_sizes.get(opponent, 0)
        known_cards = len(self.get_known_opponent_cards(opponent))
        return hand_size - known_cards

    def get_unknown_cards(self):
        return self.get_cards_at_location("unknown")

    def opponent_drew_card(self, opponent):
        current_size = self.opponent_hand_sizes.get(opponent, 0)
        self.remember_opponent_hand_size(opponent, current_size + 1)

    def reset_opponent_hand(self, opponent):
        for card, info in self.cards.items():
            if info["location"] == "opponent_hand" and info["owner"] == opponent:
                self.update_card_location(card, "discard_pile", None)

    def forget_discard_pile(self):
        for card in self.get_cards_at_location("discard_pile"):
            self.update_card_location(card, "unknown", None)