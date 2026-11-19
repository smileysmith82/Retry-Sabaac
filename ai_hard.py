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

        strength = max(0.0, min(1.0, 1.0 - (hand_distance / self.call_distance)))

        if betting.current_bet == 0:

            raise_chance = aggression * strength

            bluff_chance = bluff * (1.0 - strength)

            total_raise_chance = max(0.0, min(0.95, raise_chance * 0.75 + bluff_chance * 0.5))

            if random.random() < total_raise_chance:
                raise_amount = self.get_dynamic_raise(hand_distance, aggression, bluff)

                if self.can_raise(game, raise_amount):
                    betting.action_raise(raise_amount)
                    return

            betting.action_call()
            return

        call_cost = betting.current_bet

        credits = max(1, player.credits)

        cost_ratio = min(1.0, call_cost / credits)

        willingness = strength + (risk * 0.25)

        required_strength = 0.35 + cost_ratio * (0.5 - risk * 0.25)

        if strength < required_strength and random.random() > risk:
            betting.betting_fold()
            return

        raise_chance = aggression * strength * 0.75

        raise_chance += bluff * (1.0 - strength) * 0.35

        raise_chance *= (1.0 - cost_ratio * 0.5)

        if random.random() < raise_chance:
            raise_amount = self.get_dynamic_raise(hand_distance, aggression, bluff)
            if self.can_raise(game, betting.current_bet + raise_amount):
                betting.action_raise(betting.current_bet + raise_amount)
                return

            
        betting.action_call()
        return
        



# EDIT THIS ONE V
    def make_move(self, game):
        if game.phase == game.BETTING_PHASE:
            return self.make_betting_move(game)

        player = game.current_player
        hand = player.hand

        #If Sabacc, see if there is a better sabacc. If not, stand
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

        #Check to see if Swapping with the discard pile creates a 0 hand.
        if game.discard_pile and self.can_swap(player):
            discard_card = game.discard_pile[-1]
            
            best_index, best_value = self.find_best_ranked_swap(hand, discard_card)
            if best_index is not None:
                current_value = self.get_hand_value(hand)
                higher_category = best_value[0] > current_value[0]
                if higher_category:
                    swap(game,best_index, source="discard")
                    return
        

        risk = self.personality["risk"]
        aggression = self.personality["aggression"]

        probabilities = self.get_draw_improvement_probability(player)
        draw_probability = probabilities["improvement"]

        draw_score = self.weigh_probability(
                    probabilities["higher_category"],
                    probabilities["same_category"],
                    probabilities["average_improvement"]
                )
        
        swap_probabilities = self.get_swap_draw_improvement_probability(player)

        best_swap_index = None
        best_swap_score = 0.0
        best_swap_probability = 0.0

        
            
        if swap_probabilities:
            best_swap_index = max(swap_probabilities,
                    key=lambda index: swap_probabilities[index]["score"])

            best_swap_score = swap_probabilities[best_swap_index]["score"]

            best_swap_probability = swap_probabilities[best_swap_index]["improvement"]
    
        required_probability = 1.0 - risk
        best_improvement_probability = draw_probability

        if self.can_swap(player):
            best_improvement_probability = max(best_improvement_probability, best_swap_probability)

        if best_swap_score > draw_score:
            if (best_swap_probability >= required_probability and self.can_swap(player)):
                swap(game, best_swap_index, source="draw")
                return
            if (draw_probability >= required_probability and self.can_draw(player)):
                draw_card(game)
                return
        else:
            if (draw_probability >= required_probability
                 and self.can_draw(player)):
                draw_card(game)
                return

            if (best_swap_probability >= required_probability and self.can_swap(player)):
                swap(game, best_swap_index, source="draw")
                return
            
        hand_strength = self.get_hand_strength(hand)

        
        required_hand_strength = .1 + (aggression * 0.3)
        required_hand_strength = max(0.05, min(0.40, required_hand_strength))
        

        if hand_strength >= required_hand_strength:
            stand(game)
            return


        if best_improvement_probability < required_probability:
            fold(game)
            return
        stand(game)
        return


    def get_hand_strength(self, hand):
        hand_value = self.get_hand_value(hand)
        category = hand_value[0]

        if category == wh.NULRHEK:
            total = abs(sum(card.rank for card in hand))
            return 1.0 / (1 + total)

        return category / wh.PURE_SABAAC
        

    def get_dynamic_raise(self, hand_distance, aggression, bluff):
        strength_factor = max(1, (self.call_distance / (hand_distance + 1)))

        aggression_factor = 0.5 + aggression
        bluff_factor = 1 + (bluff*0.5)
        base_raise = stt.MINIMUM_RAISE * aggression_factor * strength_factor * bluff_factor

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
                "worse": new_value < current_value,
                "same_category": (
                    new_value[0] == current_value[0]
                    and new_value > current_value),
                "improvement_amount": (
                    new_value[1] - current_value[1]
                    if new_value[0] == current_value[0] == wh.NULRHEK
                    else None)    
                
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
                "worse": 0.0,
                "average_improvement": 0.0
            }

        total_outcomes = len(outcomes)


        improving_outcomes = [
            outcome for outcome in outcomes if outcome["improved"]
        ]

        higher_category_outcomes = [
            outcome for outcome in outcomes if outcome["higher_category"]
        ]

        same_category_outcomes = [
            outcome for outcome in outcomes if outcome["same_category"]
        ]
        improving_amounts = [
            outcome["improvement_amount"]
            for outcome in same_category_outcomes
            if outcome["improvement_amount"] is not None
        ]

        average_improvement = (
            sum(improving_amounts) / len(improving_amounts)
            if improving_amounts else 0.0
        )

        worse_outcomes = [
            outcome for outcome in outcomes if outcome["worse"]
        ]

        

        return {
            "improvement": len(improving_outcomes) / total_outcomes,
            "higher_category": len(higher_category_outcomes) / total_outcomes,
            "same_category": len(same_category_outcomes) / total_outcomes,
            "worse": len(worse_outcomes) / total_outcomes,
            "average_improvement": average_improvement
        }

    def get_swap_draw_outcomes(self, planning_state):
            outcomes = []

            hand = planning_state["hand"]
            unknown_cards = planning_state["unknown_cards"]

            current_value = self.get_hand_value(hand)

            if not unknown_cards or not hand:
                return outcomes

            for index in range(len(hand)):
                for drawn_card in unknown_cards:
                    new_hand = hand.copy()
                    new_hand[index] = drawn_card

                    new_value = self.get_hand_value(new_hand)

                    outcomes.append({
                        "discard_index": index,
                        "drawn_card": drawn_card,
                        "discarded_card": hand[index],
                        "hand_value": new_value,
                        "improved": new_value > current_value,
                        "higher_category": new_value[0] > current_value[0],
                        "same_category": (
                            new_value[0] == current_value[0]
                            and new_value > current_value
                        ),
                        "worse": new_value < current_value,
                        "improvement_amount": (
                            new_value[1] - current_value[1]
                            if new_value[0] == current_value[0] == wh.NULRHEK
                            else None
                        )
                    })

            return outcomes
    
    def get_swap_draw_improvement_probability(self,player):
        planning_state = {
           "hand": player.hand.copy(),
           "unknown_cards": self.memory.get_unknown_cards().copy()
        }

        outcomes = self.get_swap_draw_outcomes(planning_state)

        probabilities = {}

        for index in range(len(player.hand)):
            index_outcomes = [
                outcome for outcome in outcomes
                if outcome["discard_index"] == index
            ]

            if not index_outcomes:
                probabilities[index] = {
                    "discarded_card": player.hand[index],
                    "improvement": 0.0,
                    "higher_category": 0.0,
                    "same_category": 0.0,
                    "worse": 0.0,
                    "average_improvement": 0.0,
                    "score": 0.0
                }
                continue

            total_outcomes = len(index_outcomes)


            improving_outcomes = [
            outcome for outcome in index_outcomes
            if outcome["improved"]
            ]

            higher_category_outcomes = [
                outcome for outcome in index_outcomes
                if outcome["higher_category"]
            ]

            same_category_outcomes = [
                outcome for outcome in index_outcomes
                if outcome["same_category"]
            ]

            improvement_amounts = [
                outcome["improvement_amount"] for outcome in same_category_outcomes
                if outcome["improvement_amount"] is not None
            ]

            average_improvement = (
                sum(improvement_amounts) / len(improvement_amounts)
                if improvement_amounts else 0.0
            )

            worse_outcomes = [
                outcome for outcome in index_outcomes
                if outcome["worse"]
            ]

        

            probabilities[index] = {
                "discarded_card": player.hand[index],
                "improvement": len(improving_outcomes) / total_outcomes,
                "higher_category": len(higher_category_outcomes) / total_outcomes,
                "same_category": len(same_category_outcomes) / total_outcomes,
                "worse": len(worse_outcomes) / total_outcomes,
                "average_improvement": average_improvement,
                "score": self.weigh_probability(
                    len(higher_category_outcomes) / total_outcomes,
                    len(same_category_outcomes) / total_outcomes,
                    average_improvement
                )
            }


        return probabilities

#Fix average improvement to be a weight as well
    def weigh_probability(self, p_higher_category, p_same_category, average_improvement):
        improvement_weight = average_improvement/ 10
        score_probability = (p_higher_category * 3.0) + (p_same_category * 1.0 * improvement_weight)
        return score_probability
    
#EDIT
    def create_planning_state(self, game, player):
        return {
            "hand": player.hand.copy(),
            "unknown_cards": self.memory.get_unknown_cards().copy(),
            "top_discard": game.discard_pile[-1] if game.discard_pile else None,
            "credits": player.credits
        }