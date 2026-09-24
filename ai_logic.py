from player_actions import draw_card, swap, stand, fold
import settings as stt
import math

class AIPlayer:

    def make_move(self, game):
        if game.phase == game.BETTING_PHASE:
            return self.make_betting_move(game)

        player = game.current_player

        hand_total = game.total_of_hand(player.hand)

        if hand_total == 0:
            stand(game)
            return

        if game.discard_pile:
            discard_card = game.discard_pile[-1]

            for index, card in enumerate(player.hand):
                new_total = hand_total - card.rank + discard_card.rank

                if new_total == 0:
                    swap(game, index, source="discard")
                    return
        #Bad Hand
        if hand_total >= 15:
            fold(game)
            return


        if player.credits <= 5:
            stand(game)

        draw_card(game)

    def make_betting_move(self, game):
        betting = game.betting
        player = game.current_player

        hand_total = game.total_of_hand(player.hand)


        if betting.current_bet == 0:
            if hand_total <= abs(3):
                new_bet = betting.current_bet + stt.MINIMUM_RAISE
                if betting.can_raise(new_bet):
                    betting.action_raise(new_bet)
                    return
                
            betting.check()
            return

        amount_to_call = betting.current_bet - betting.player_bets[player]

        if hand_total <= abs(2):            
            new_bet = betting.current_bet + stt.MINIMUM_RAISE
            if betting.can_raise(new_bet):
                betting.action_raise(new_bet)
                return

        if hand_total <= abs(5):            
            betting.action_call()
            return

        betting.betting_fold() 