from player_actions import draw_card, swap, stand, fold


class AIPlayer:

    def make_move(self, game):
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

        draw_card(game)