import ai_base as ab
from player_actions import draw_card, swap, stand, fold
import settings as stt
import random

class MediumAI(ab.AIPlayer):
    def __init__(self, personality):
        super().__init__(personality=personality, difficulty="Medium", noise=0.8)
        self.swap_distance = 8
        self.fold_distance = 18
        self.low_credit_threshold = 25
        self.raise_distance = 4
        self.call_distance = 12
        self.raise_amount = stt.MINIMUM_RAISE

    def make_move(self, game):
        if game.phase == game.BETTING_PHASE:
            return self.make_betting_move(game)

        player = game.current_player
        hand = player.hand
        risk = self.personality["risk"]

        hand_distance = self.add_noise(self.get_hand_distance(hand))

        if self.is_sabaac(hand):
            stand(game)
            return

        if game.discard_pile and self.can_swap(player):
            discard_card = game.discard_pile[-1]
            zero_index = self.find_zero_swap(hand, discard_card)
            if zero_index is not None:
                swap(game, zero_index, source="discard")
                return

        discard_improves = False
        best_swap = None
        new_distance = None

        if game.discard_pile:
            discard_card = game.discard_pile[-1]
            best_swap = self.find_best_swap(hand, discard_card, 99)
            if best_swap is not None:
                new_hand = self.get_replacement_hand(hand, best_swap, discard_card)
                new_distance = self.get_hand_distance(new_hand)
                if new_distance < hand_distance:
                    discard_improves = True

        if hand_distance <= 4:
            if discard_improves and hand_distance - new_distance >= 3 and risk >= 0.4:
                swap(game, best_swap, source="discard")
                return
            if self.can_draw(player) and risk >= 0.7:
                draw_card(game)
                return
            stand(game)
            return

        elif hand_distance <= 9:
            if discard_improves:
                swap(game, best_swap, source="discard")
                return
            if self.can_draw(player):
                if random.random() < (0.45 + risk* 0.35):
                    draw_card(game)
                    return
            stand(game)
            return

        elif hand_distance <= 14:
            if discard_improves:
                swap(game, best_swap, source="discard")
                return
            
            if self.can_swap(player) and game.discard_pile:
                discard_card = game.discard_pile[-1] 
                discard_distance = abs(self.get_hand_total(hand) - discard_card.rank)                    
                if discard_distance > hand_distance and risk >= 0.5:
                    worst_index = self.get_worst_card(hand)
                    swap(game, worst_index, source="draw")
                    return

            if self.can_draw(player):
                draw_card(game)
                return

            stand(game)
            return

        else:
            if discard_improves:
                swap(game, best_swap, source="discard")
                return

            if self.can_swap(player):
                worst_index = self.get_worst_card(hand)
                swap(game, worst_index, source="draw")
                return

            if self.can_draw(player):
                draw_card(game)
                return

            if risk < 0.4:
                fold(game)
                return

            stand(game)
            return
    
    def get_dynamic_raise(self, hand_distance, aggression, bluff):
        strength_factor = max(1, (self.call_distance / (hand_distance + 1)))

        base_raise = stt.MINIMUM_RAISE * aggression * strength_factor

        if hand_distance > self.call_distance:
            base_raise *= (0.5 + bluff)

        return int(base_raise)

    def make_betting_move(self, game):
        betting = game.betting
        player = game.current_player
        hand = player.hand

        hand_distance = self.add_noise(self.get_hand_distance(hand))

        aggression = self.personality["aggression"]
        risk = self.personality["risk"]
        bluff = self.personality["bluff"]

        if betting.current_bet == 0:

            if hand_distance <= self.raise_distance * aggression:
                raise_amount = self.get_dynamic_raise(hand_distance, aggression, bluff)
                new_bet = betting.current_bet + raise_amount
                if self.can_raise(game, new_bet):
                    betting.action_raise(new_bet)
                    return

            if bluff > 0.4 and random.random() < bluff * 0.5:
                raise_amount = self.get_dynamic_raise(hand_distance, aggression, bluff)
                new_bet = betting.current_bet + raise_amount
                if self.can_raise(game, new_bet):
                    betting.action_raise(new_bet)
                    return

            betting.action_call()
            return


        if hand_distance <= self.raise_distance * aggression:
            raise_amount = self.get_dynamic_raise(hand_distance, aggression, bluff)
            new_bet = betting.current_bet + raise_amount
            if self.can_raise(game, new_bet):
                betting.action_raise(new_bet)
                return
        #Bluff raise
        if hand_distance <= self.call_distance * 1.5:
            if bluff > 0.5 and random.random() < bluff * 0.4:
                raise_amount = self.get_dynamic_raise(hand_distance, aggression, bluff)
                new_bet = betting.current_bet + raise_amount
                if self.can_raise(game, new_bet):
                    betting.action_raise(new_bet)
                    return
        #Medium hand (call)
        if hand_distance <= self.call_distance:
            betting.action_call()
            return

        #Weak Hand: Call if risk is high
        if hand_distance <= self.call_distance * 1.5 and risk >= 0.6:
            betting.action_call()
            return

        if risk < 0.5 and bluff <0.4:
            betting.betting_fold()
            return

        betting.action_call()
        return

        