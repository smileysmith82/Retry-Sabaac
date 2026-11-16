import ai_base as ab
from player_actions import draw_card, swap, stand, fold
import settings as stt
import random

class EasyAI(ab.AIPlayer):
    def __init__(self, personality):
        super().__init__(personality=personality, difficulty="Easy", noise=1.5)
        self.swap_distance = 5
        self.fold_distance = 15
        self.low_credit_threshold = 25
        self.raise_distance = 3
        self.call_distance = 10
        self.raise_amount = stt.MINIMUM_RAISE


    def make_move(self, game):
        if game.phase == game.BETTING_PHASE:
            return self.make_betting_move(game)

        player = game.current_player
        hand = player.hand
        risk = self.personality["risk"]

        hand_distance = self.add_noise(self.get_hand_distance(hand))
        
        #Stand
        if self.is_sabaac(hand):
            stand(game)
            return 

        #Regular Swap
        if game.discard_pile and self.can_swap(player):            
            discard_card = game.discard_pile[-1]
            zero_index = self.find_zero_swap(hand,discard_card)
            if zero_index is not None:
                swap(game, zero_index, source="discard")
                return
            if random.random() < risk:
                discard_card = game.discard_pile[-1]
                swap_index = self.find_best_swap(hand, 
                    discard_card, self.swap_distance)
                if swap_index is not None:
                    swap(game, swap_index, source="discard")
                    return

        #Fold if the hand is super bad
        if hand_distance >= self.fold_distance:
            fold(game)
            return

        #Stand if low credits
        if player.credits <= self.low_credit_threshold:
            stand(game)
            return 

        #Regular Draw
        if self.can_draw(player):
            if random.random() < risk:
                draw_card(game)
                return
        
        if self.can_swap(player):
            if hand_distance >= self.fold_distance * 0.6:
                if random.random() < risk * 0.4:
                    worst_index = self.get_worst_card(hand)
                    swap(game, worst_index, source="draw")
                    return 

        stand(game)
        return

    def make_betting_move(self,game):
        betting = game.betting
        player = game.current_player
        hand = player.hand

        hand_distance = self.add_noise(self.get_hand_distance(hand))
        aggression = self.personality["aggression"]
        risk = self.personality["risk"]
        bluff = self.personality["bluff"]
        
        if betting.current_bet == 0:
            if hand_distance <= self.raise_distance * aggression:
                new_bet = betting.current_bet + self.raise_amount
                if self.can_raise(game, new_bet):
                    betting.action_raise(new_bet)
                    return

            if random.random() < bluff:
                new_bet = betting.current_bet + self.raise_amount
                if self.can_raise(game, new_bet):
                    betting.action_raise(new_bet)
                    return

            betting.check()
            return

        if hand_distance <= self.raise_distance * aggression:
            new_bet = betting.current_bet + self.raise_amount

            if self.can_raise(game, new_bet):
                betting.action_raise(new_bet)
                return

        if random.random() < bluff:
            new_bet = betting.current_bet + self.raise_amount
            if self.can_raise(game, new_bet):
                betting.action_raise(new_bet)
                return
            
        if hand_distance <= self.call_distance * risk:
            betting.action_call()
            return

        betting.betting_fold()


