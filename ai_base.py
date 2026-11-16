import winning_hands as wh
import settings as stt
import random


class AIPlayer:
    def __init__(self, personality, difficulty, noise):
        self.personality = personality
        self.difficulty = difficulty
        self.noise = noise

    def add_noise(self, score):
        noise_factor = random.uniform(1-self.noise, 1 + self.noise)
        return score * noise_factor

    def evaluate_hand(self, hand):
        return wh.evaluate_hand(hand)

    def get_hand_type(self, hand):
        evaluation = self.evaluate_hand(hand)
        return evaluation[0]

    def get_hand_name(self, hand):
        hand_type = self.get_hand_type(hand)
        return wh.HAND_NAMES[hand_type]

    def get_hand_total(self, hand):
        return sum(card.rank for card in hand)

    def is_sabaac(self, hand):
        return self.get_hand_total(hand) == 0

    def get_hand_distance(self, hand):
        return abs(self.get_hand_total(hand))

    def find_best_swap(self, hand, replacement_card, max_distance):
        best_index = None
        best_distance = float('inf')
        for index, card in enumerate(hand):
            new_hand = self.get_replacement_hand(
                hand, index, replacement_card)
            new_distance = self.get_hand_distance(new_hand)

            if new_distance <= abs(max_distance):
                if new_distance < best_distance:
                    best_distance = new_distance
                    best_index = index

        return best_index
    
    def find_zero_swap(self, hand, replacement_card):
        for index, card in enumerate(hand):
            new_total = self.get_hand_total(self.get_replacement_hand(hand, index, replacement_card))
            if new_total == 0:
                return index
        return None

    def get_replacement_hand(self, hand, index, replacement_card):
        new_hand = hand[:]
        new_hand[index] = replacement_card
        return new_hand

    def get_hand_value(self, hand):
        evaluation = self.evaluate_hand(hand)

        return evaluation

    def can_afford(self, player, cost):
        return player.credits >= cost

    def can_draw(self, player):
        return self.can_afford(player, stt.DRAW_COST)

    def can_swap(self, player):
        return self.can_afford(player, stt.SWAP_COST)

    
    
    
    #Betting Methods
    
    def get_current_bet(self, game):
        return game.betting.current_bet
    
    def get_player_bet(self, game, player):
        return game.betting.player_bets[player]
    
    def get_amount_to_call(self, game, player):
        return game.betting.current_bet - game.betting.player_bets[player]

    def can_call(self,game):
        return game.betting.can_call()
    
    def can_raise(self, game, new_bet):
        return game.betting.can_raise(new_bet)


    def get_worst_card(self, hand):
        return max(range(len(hand)), key=lambda i: abs(hand[i].rank))