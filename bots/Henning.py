import random
from typing import List, Optional

from bot import Bot
from card import Card, CardType
from game_handling.game_state import GameState


class Henning(Bot):
    def play(self, state: GameState) -> Optional[Card]:
        # Calculate the probability of drawing an Exploding Kitten
        exploding_kitten_probability = self.calculate_exploding_kitten_probability(state)

        # Use SEE THE FUTURE if available to assess risk
        see_the_future_cards = self.get_cards_by_type(CardType.SEE_THE_FUTURE)
        if see_the_future_cards:
            return see_the_future_cards[0]

        # Use SKIP if the probability of an Exploding Kitten is high
        if exploding_kitten_probability > 0.3:
            skip_cards = self.get_cards_by_type(CardType.SKIP)
            if skip_cards:
                return random.choice(skip_cards)

        # Play Normal cards only if no better option exists
        normal_cards = self.get_cards_by_type(CardType.NORMAL)
        if normal_cards:
            return random.choice(normal_cards)

        # Default to None if no cards are playable
        return None

    def handle_exploding_kitten(self, state: GameState) -> int:
        # Use DEFUSE card if available
        defuse_cards = self.get_cards_by_type(CardType.DEFUSE)
        if defuse_cards:
            self.hand.remove(defuse_cards[0])

            # Strategically place the Exploding Kitten to disrupt opponents
            # Place it towards the top (trap) or middle depending on game state
            if state.cards_left > 10:
                return random.randint(state.cards_left // 2, state.cards_left - 1)
            else:
                return random.randint(1, 3)

        # No DEFUSE means the bot loses
        return -1

    def see_the_future(self, state: GameState, top_three: List[Card]):
        # Check the top three cards and adjust strategy
        if any(card.card_type == CardType.EXPLODING_KITTEN for card in top_three):
            print("Exploding Kitten detected in the top three cards!")
            skip_cards = self.get_cards_by_type(CardType.SKIP)
            if skip_cards:
                return skip_cards[0]

        # Default behavior if no immediate risk detected
        print("No immediate threats detected in the top three cards.")
        return None

    def calculate_exploding_kitten_probability(self, state: GameState) -> float:
        # Probability calculation: Exploding Kittens left vs total cards
        total_kitten_cards = state.total_cards_in_deck.EXPLODING_KITTEN
        remaining_cards = state.cards_left
        return total_kitten_cards / remaining_cards if remaining_cards > 0 else 0

    def get_cards_by_type(self, card_type: CardType) -> List[Card]:
        """Helper method to filter cards by type."""
        return [card for card in self.hand if card.card_type == card_type]
