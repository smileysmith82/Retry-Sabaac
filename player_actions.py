import random
import settings as set

def notify_hard_ai_draw(game, drawing_player, drawn_card):
    from ai_hard import HardAI

    for player in game.players:
        if not player.is_ai or not isinstance(player.ai, HardAI):
            continue

        if player is drawing_player:
            player.ai.memory.update_card_location(drawn_card, "own_hand", drawing_player)
            continue

        player.ai.memory.opponent_drew_card(drawing_player)

def notify_hard_ai_swap(game, swapping_player, taken_card, discarded_card, source):
    from ai_hard import HardAI

    for player in game.players:
        if not player.is_ai or not isinstance(player.ai, HardAI):
            continue

        memory = player.ai.memory

        memory.update_card_location(discarded_card, "discard_pile")

        if player is swapping_player:
            memory.update_card_location(taken_card, "own_hand", swapping_player)

        elif source == "discard":
            memory.update_card_location(taken_card, "opponent_hand", swapping_player)

def notify_hard_ai_fold(game, folding_player, folded_cards, visible_card):
    from ai_hard import HardAI

    for player in game.players:
        if not player.is_ai or not isinstance(player.ai, HardAI):
            continue

        memory = player.ai.memory

        if player is folding_player:
            for card in folding_player.hand:
                memory.update_card_location(card, "discard_pile")

        else:
            memory.reset_opponent_hand(folding_player)

            memory.remember_top_discard(visible_card)
            memory.opponent_hand_sizes.pop(folding_player, None)

def notify_hard_ai_spike_start(game):
    from ai_hard import HardAI

    for player in game.players:
        if not player.is_ai or not isinstance(player.ai, HardAI):
            continue

        memory = player.ai.memory

        for card in memory.get_cards_at_location("own_hand"):
            memory.update_card_location(card, "discard_pile")

        for opponent in game.players:
            if opponent is player:
                continue
            memory.reset_opponent_hand(opponent)

def notify_hard_ai_spike_end(game):
    from ai_hard import HardAI
    for player in game.players:
        if not player.is_ai or not isinstance(player.ai, HardAI):
            continue

        memory = player.ai.memory
        for opponent in game.players:
            if opponent is player:
                continue
            memory.remember_opponent_hand_size(opponent, len(opponent.hand))
        
        memory.remember_own_hand(player)
        memory.remember_top_discard(game.discard_pile[-1] if game.discard_pile else None)

        

def draw_card(game):
    player = game.current_player
    if not game.pay(player, set.DRAW_COST):
        return "NOT_ENOUGH_CREDITS" #invalid Action
    game.refill_draw_pile()

    card = game.deck.shuffled_deck.pop()
    player.hand.append(card)

    notify_hard_ai_draw(game, player, card)

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

    notify_hard_ai_swap(game, player, swapped_card, discarded_card, source)

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
    visible_card = game.discard_pile[-1] if folded_cards else None

    notify_hard_ai_fold(game, player, folded_cards, visible_card)

    game.next_turn()

    return "SUCCESS"

def print_memory(self, ai_player):
    print(f"\n--- {ai_player.name}'s Card Memory ---")

    print("Own Hand:")
    for card in self.get_cards_at_location("own_hand"):
        print(f"  {card}")

    print("Known Opponent Cards:")
    for card in self.get_cards_at_location("opponent_hand"):
        owner = self.cards[card]["owner"]
        print(f"  {owner.name}: {card}")

    print("Known Discard Cards:")
    for card in self.get_cards_at_location("discard_pile"):
        print(f"  {card}")

    print(f"Unknown Cards: {len(self.get_unknown_cards())}")

    print("Opponent Hand Sizes:")
    for opponent, hand_size in self.opponent_hand_sizes.items():
        known = len(self.get_known_opponent_cards(opponent))
        unknown = self.get_unknown_opponent_count(opponent)

        print(
            f"  {opponent.name}: "
            f"{hand_size} total, "
            f"{known} known, "
            f"{unknown} unknown"
        )


