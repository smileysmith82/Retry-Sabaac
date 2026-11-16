import random
import ai_base as ab
from player_actions import draw_card, swap, stand, fold
import settings as stt
from card_memory import CardMemory
import winning_hands as wh

class HardAI(ab.AIPlayer):
    def __init__(self, personality):
        super().__init__(personality=personality, difficulty="Hard", noise=0.05)
        self.swap_distance = 4
        self.fold_distance = 18
        self.low_credit_threshold = 25
        self.raise_distance = 4
        self.call_distance = 12
        self.raise_amount = stt.MINIMUM_RAISE
        self.memory = CardMemory()

    def evaluate_hand(self, hand):
        return wh.evaluate_hand(hand)
    
    def find_best_ranked_swap(self, hand, replacement_card):
        current_value = self.get_hand_value(hand)

        best_index = None
        best_value = current_value

        for index in range(len(hand)):
            new_hand = self.get_replacement_hand(
                hand, index, replacement_card)
            new_value = self.get_hand_value(new_hand)

            if new_value > best_value:
                best_value = new_value
                best_index = index

        return best_index, best_value
    
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


# EDIT THIS ONE V
    def make_move(self, game):
        if game.phase == game.BETTING_PHASE:
            return self.make_betting_move(game)

        player = game.current_player
        hand = player.hand
        

        risk = self.personality["risk"]
        hand_distance = self.add_noise(self.get_hand_distance(hand))


        if self.is_sabaac(hand):

            if game.discard_pile and self.can_swap(player):
                discard_card = game.discard_pile[-1]

                best_index, best_value = self.find_best_ranked_swap(hand, discard_card)
                if best_index is not None:
                    current_value = self.get_hand_value(hand)
                    higher_category = best_value[0] > current_value[0]
                    if higher_category:
                        swap(game,best_index, source="discard")
                        return

            stand(game)
            return

        if game.discard_pile and self.can_swap(player):
            discard_card = game.discard_pile[-1]
            
            best_index, best_value = self.find_best_ranked_swap(hand, discard_card)
            if best_index is not None:
                current_value = self.get_hand_value(hand)
                higher_category = best_value[0] > current_value[0]
                if higher_category:
                    swap(game,best_index, source="discard")
                    return

        discard_improves = False
        best_swap = None


        if game.discard_pile:
            discard_card = game.discard_pile[-1]
            best_swap, best_swap_value = self.find_best_ranked_swap(hand, discard_card)
            if best_swap is not None:
                discard_improves = True
                
        cards_by_rank = self.get_unknown_cards_by_rank()
        probabilities = self.get_draw_improvement_probability(player)



        
        
        if hand_distance <= 4:
            if discard_improves and self.can_swap(player) and risk >= 0.4:
                swap(game, best_swap, source="discard")
                return
            if self.can_draw(player) and risk >= 0.7:
                draw_card(game)
                return
            stand(game)
            return

        elif hand_distance <= 9:
            if discard_improves and self.can_swap(player):
                swap(game, best_swap, source="discard")
                return
            if self.can_draw(player):
                if random.random() < (0.45 + risk* 0.35):
                    draw_card(game)
                    return
            stand(game)
            return

        elif hand_distance <= 14:
            if discard_improves and self.can_swap(player):
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
            if discard_improves and self.can_swap(player):
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

#Maybe Edit
    def get_draw_outcomes(self, planning_state):
        outcomes = []

        current_value = self.get_hand_value(planning_state["hand"])

        unknown_cards = planning_state["unknown_cards"]
        if not unknown_cards:
            return outcomes

        for card in unknown_cards:
            new_hand = planning_state["hand"].copy()
            new_hand.append(card)

            new_value = self.get_hand_value(new_hand)

            outcomes.append({
                "card": card,
                "hand_value": new_value,
                "improved": new_value > current_value,
                "higher_category": new_value[0] > current_value[0],
                "probability": 1 / len(unknown_cards),
                "worse": new_value < current_value
            })

        return outcomes


#EDIT
    def get_unknown_cards_by_rank(self):
        unknown_cards = self.memory.get_unknown_cards()
        cards_by_rank = {}

        for card in unknown_cards:
            rank = card.rank

            if rank not in cards_by_rank:
                cards_by_rank[rank] = 0

            cards_by_rank[rank] += 1

        return cards_by_rank

#EDIT
    def get_draw_improvement_probability(self, player):
        planning_state = {
           "hand": player.hand.copy(),
           "unknown_cards": self.memory.get_unknown_cards().copy()
        }

        outcomes = self.get_draw_outcomes(planning_state)

        if not outcomes:
            return {
                "improvement": 0.0,
                "higher_category": 0.0,
                "same_category": 0.0,
                "worse": 0.0
            }

        total_outcomes = len(outcomes)


        improving_outcomes = [
            outcome for outcome in outcomes if outcome["improved"]
        ]

        higher_category_outcomes = [
            outcome for outcome in outcomes if outcome["higher_category"]
        ]

        same_category_outcomes = [
            outcome for outcome in improving_outcomes if not outcome["higher_category"]
        ]

        worse_outcomes = [
            outcome for outcome in outcomes if outcome["worse"]
        ]

        return {
            "improvement": len(improving_outcomes) / total_outcomes,
            "higher_category": len(higher_category_outcomes) / total_outcomes,
            "same_category": len(same_category_outcomes) / total_outcomes,
            "worse": len(worse_outcomes) / total_outcomes
        }

#EDIT
    def create_planning_state(self, game, player):
        return {
            "hand": player.hand.copy(),
            "unknown_cards": self.memory.get_unknown_cards().copy(),
            "top_discard": game.discard_pile[-1] if game.discard_pile else None,
            "credits": player.credits
        }



