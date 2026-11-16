
import unittest
from dataclasses import dataclass

from ai_hard import HardAI
from card_memory import CardMemory
from player_actions import (
    notify_hard_ai_spike_start,
    notify_hard_ai_spike_end
)


@dataclass(frozen=True)
class TestCard:
    name: str

    def __str__(self):
        return self.name


class TestPlayer:
    def __init__(self, name, is_ai=False):
        self.name = name
        self.is_ai = is_ai
        self.hand = []
        self.ai = None


class TestGame:
    def __init__(self, players, discard_pile):
        self.players = players
        self.discard_pile = discard_pile


class SpikeMemoryTests(unittest.TestCase):

    def setUp(self):
        # Create cards.
        self.old_ai_card_1 = TestCard("Old AI Card 1")
        self.old_ai_card_2 = TestCard("Old AI Card 2")
        self.old_opponent_card = TestCard("Known Opponent Card")

        self.new_ai_card_1 = TestCard("New AI Card 1")
        self.new_ai_card_2 = TestCard("New AI Card 2")

        self.old_discard = TestCard("Old Top Discard")
        self.new_top_discard = TestCard("New Top Discard")

        self.other_cards = [
            TestCard(f"Unknown Card {i}")
            for i in range(5)
        ]

        # Create players.
        self.ai_player = TestPlayer("Hard AI", is_ai=True)
        self.opponent_1 = TestPlayer("Opponent 1")
        self.opponent_2 = TestPlayer("Opponent 2")

        # Give the AI its old hand.
        self.ai_player.hand = [
            self.old_ai_card_1,
            self.old_ai_card_2
        ]

        # Give opponents their hands.
        self.opponent_1.hand = [
            self.old_opponent_card,
            self.other_cards[0]
        ]

        self.opponent_2.hand = [
            self.other_cards[1],
            self.other_cards[2]
        ]

        # Create a HardAI without needing its normal initialization.
        self.ai_player.ai = HardAI.__new__(HardAI)
        self.ai_player.ai.memory = CardMemory()

        # Create the complete card inventory.
        all_cards = (
            self.ai_player.hand
            + self.opponent_1.hand
            + self.opponent_2.hand
            + [self.old_discard, self.new_top_discard]
            + self.other_cards[3:]
            + [self.new_ai_card_1, self.new_ai_card_2]
        )

        memory = self.ai_player.ai.memory
        memory.initialize_cards(all_cards)
        memory.initialize_opponent_hand_sizes(
            [self.ai_player, self.opponent_1, self.opponent_2],
            self.ai_player
        )

        # Establish what the AI knows before the spike.
        memory.remember_own_hand(self.ai_player)
        memory.update_card_location(
            self.old_opponent_card,
            "opponent_hand",
            self.opponent_1
        )
        memory.remember_top_discard(self.old_discard)

        self.game = TestGame(
            [self.ai_player, self.opponent_1, self.opponent_2],
            [self.old_discard]
        )

    def test_spike_start_moves_old_known_hands_to_discard(self):
        memory = self.ai_player.ai.memory

        notify_hard_ai_spike_start(self.game)

        # The AI's old hand should now be remembered as discarded.
        self.assertEqual(
            memory.cards[self.old_ai_card_1]["location"],
            "discard_pile"
        )
        self.assertEqual(
            memory.cards[self.old_ai_card_2]["location"],
            "discard_pile"
        )

        # The known opponent card should also be remembered as discarded.
        self.assertEqual(
            memory.cards[self.old_opponent_card]["location"],
            "discard_pile"
        )

        # The AI should no longer consider that card in the opponent's hand.
        self.assertEqual(
            len(memory.get_known_opponent_cards(self.opponent_1)),
            0
        )

    def test_spike_end_remembers_new_hands_and_top_discard(self):
        memory = self.ai_player.ai.memory

        # Simulate the game dealing new hands.
        self.ai_player.hand = [
            self.new_ai_card_1,
            self.new_ai_card_2
        ]

        self.opponent_1.hand = [
            self.other_cards[0],
            self.other_cards[1],
            self.other_cards[2]
        ]

        self.opponent_2.hand = [
            self.other_cards[3]
        ]

        self.game.discard_pile.append(self.new_top_discard)

        notify_hard_ai_spike_end(self.game)

        # The AI should know its new hand.
        self.assertEqual(
            memory.cards[self.new_ai_card_1]["location"],
            "own_hand"
        )
        self.assertEqual(
            memory.cards[self.new_ai_card_2]["location"],
            "own_hand"
        )

        # The AI should know the new opponent hand sizes.
        self.assertEqual(
            memory.opponent_hand_sizes[self.opponent_1],
            3
        )
        self.assertEqual(
            memory.opponent_hand_sizes[self.opponent_2],
            1
        )

        # The AI should remember the final top discard.
        self.assertEqual(
            memory.cards[self.new_top_discard]["location"],
            "discard_pile"
        )

    def test_spike_with_discard_shuffle_forgets_old_cards(self):
        memory = self.ai_player.ai.memory

        # Begin the spike.
        notify_hard_ai_spike_start(self.game)

        # Simulate the discard pile being shuffled into the draw pile.
        memory.forget_discard_pile()

        # The new top discard is revealed after the shuffle.
        memory.remember_top_discard(self.new_top_discard)

        # Simulate the new hands being dealt.
        self.ai_player.hand = [
            self.new_ai_card_1,
            self.new_ai_card_2
        ]

        self.game.discard_pile = [self.new_top_discard]

        notify_hard_ai_spike_end(self.game)

        # Old known cards should now be unknown.
        self.assertEqual(
            memory.cards[self.old_ai_card_1]["location"],
            "unknown"
        )
        self.assertEqual(
            memory.cards[self.old_ai_card_2]["location"],
            "unknown"
        )
        self.assertEqual(
            memory.cards[self.old_opponent_card]["location"],
            "unknown"
        )

        # The AI should still know its new hand.
        self.assertEqual(
            memory.cards[self.new_ai_card_1]["location"],
            "own_hand"
        )

        # The new top discard should still be known.
        self.assertEqual(
            memory.cards[self.new_top_discard]["location"],
            "discard_pile"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
