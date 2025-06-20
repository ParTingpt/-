import random
from dataclasses import dataclass, field

SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Card values used in Blackjack
VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

@dataclass
class Card:
    rank: str
    suit: str
    value: int

    def __str__(self):
        return f"{self.rank} of {self.suit}"

@dataclass
class Deck:
    cards: list[Card] = field(default_factory=list)

    def __post_init__(self):
        self.cards = [Card(rank, suit, VALUES[rank]) for suit in SUITS for rank in RANKS]
        random.shuffle(self.cards)

    def draw(self) -> Card:
        if not self.cards:
            raise ValueError("The deck is empty")
        return self.cards.pop()

@dataclass
class Hand:
    cards: list[Card] = field(default_factory=list)

    def add_card(self, card: Card):
        self.cards.append(card)

    @property
    def value(self):
        total = sum(card.value for card in self.cards)
        # Adjust for Aces
        aces = sum(1 for card in self.cards if card.rank == 'A')
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    def __str__(self):
        return ', '.join(str(card) for card in self.cards) + f" (Total: {self.value})"


def play_round(deck: Deck):
    player_hand = Hand()
    dealer_hand = Hand()

    # initial deal
    for _ in range(2):
        player_hand.add_card(deck.draw())
        dealer_hand.add_card(deck.draw())

    print("Dealer shows:", dealer_hand.cards[0])
    print("Your hand:", player_hand)

    # Player turn
    while player_hand.value < 21:
        move = input("Hit or stand? [h/s]: ").strip().lower()
        if move == 'h':
            player_hand.add_card(deck.draw())
            print("You drew:", player_hand.cards[-1])
            print("Your hand:", player_hand)
            if player_hand.value > 21:
                print("Bust! You lose.")
                return
        elif move == 's':
            break
        else:
            print("Invalid input. Please enter 'h' or 's'.")

    # Dealer turn
    print("Dealer's hand:", dealer_hand)
    while dealer_hand.value < 17:
        dealer_hand.add_card(deck.draw())
        print("Dealer drew:", dealer_hand.cards[-1])
        print("Dealer's hand:", dealer_hand)

    if dealer_hand.value > 21 or player_hand.value > dealer_hand.value:
        print("You win!")
    elif player_hand.value == dealer_hand.value:
        print("Push! It's a tie.")
    else:
        print("Dealer wins.")


def main():
    deck = Deck()
    while True:
        play_round(deck)
        again = input("Play again? [y/n]: ").strip().lower()
        if again != 'y':
            break
        if len(deck.cards) < 10:  # reshuffle if deck is running low
            deck = Deck()
    print("Thanks for playing!")


if __name__ == "__main__":
    main()
