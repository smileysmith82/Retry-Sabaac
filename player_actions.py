import random
import settings as set

def draw_card(game):
    player = game.current_player
    if not game.pay(player, set.DRAW_COST):
        return "NOT_ENOUGH_CREDITS" #invalid Action
    game.refill_draw_pile()

    card = game.deck.shuffled_deck.pop()
    player.hand.append(card)

    game.next_turn() 
    return "SUCCESS"

def swap(game, hand_index, source="discard"):
    player = game.current_player

    if not game.pay(player, set.SWAP_COST):
        return "NOT_ENOUGH_CREDITS" #invalid Action
    if source == "discard":
        swapped_card = game.discard_pile.pop()

    elif source == "draw":
        game.refill_draw_pile()
        swapped_card = game.deck.shuffled_deck.pop()

    else:
        return "INVALID_SOURCE"

    discarded_card = player.hand[hand_index]
    game.discard_pile.append(discarded_card)
    player.hand[hand_index] = swapped_card

    game.next_turn()
    return "SUCCESS"

def stand(game):
    player = game.current_player

    game.next_turn()
    return "SUCCESS"

def reveal_cards(game):
    for player in game.players:
        print(player.name)
        print([str(card) for card in player.hand])

def fold(game):
    player = game.current_player
    player.folded = True
    folded_cards = player.hand[:]
    random.shuffle(folded_cards)
    game.discard_pile.extend(folded_cards)
    player.hand.clear()
    game.next_turn()

    return "SUCCESS"


